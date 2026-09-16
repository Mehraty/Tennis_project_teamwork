import re
import zipfile
from pathlib import Path

import pandas as pd

# input zip path
RAW_ZIP = Path("Tennis Schema.zip")

# working directories
BASE = Path("tennis_project")
OUTER_DIR = BASE / "01_outer_extracted"
DAILY_ZIPS_DIR = BASE / "02_daily_zips"
FLAT_PARQUET_DIR = BASE / "03_raw_parquet_flat"
CLEAN_TABLES_DIR = BASE / "04_clean_tables"
FINAL_DIR = BASE / "05_final"

for d in (OUTER_DIR, DAILY_ZIPS_DIR, FLAT_PARQUET_DIR, CLEAN_TABLES_DIR, FINAL_DIR):
    d.mkdir(parents=True, exist_ok=True)


def step1_extract_outer():
    with zipfile.ZipFile(RAW_ZIP) as z:
        z.extractall(OUTER_DIR)
    inner_zip_path = next(OUTER_DIR.rglob("tennis_data.zip"))
    return inner_zip_path

def step2_extract_daily_zips(inner_zip_path: Path):
    with zipfile.ZipFile(inner_zip_path) as z:
        z.extractall(DAILY_ZIPS_DIR)
    return sorted(DAILY_ZIPS_DIR.glob("*.zip"))


def step3_flatten_parquet(daily_zip_files):
    for dz in daily_zip_files:
        with zipfile.ZipFile(dz) as z:
            for member in z.namelist():
                fname = Path(member).name
                if not fname.endswith(".parquet"):
                    continue
                target = FLAT_PARQUET_DIR / fname
                if target.exists():
                    continue
                with z.open(member) as src, open(target, "wb") as dst:
                    dst.write(src.read())
    return list(FLAT_PARQUET_DIR.glob("*.parquet"))


PATTERN = re.compile(r"^(?P<table>.+)_(?P<match_id>\d+)\.parquet$")


def step4_build_clean_tables(all_files):
    groups = {}
    for f in all_files:
        m = PATTERN.match(f.name)
        if not m:
            continue
        groups.setdefault(m.group("table"), []).append(f)

    tables = {}
    for table_name, files in sorted(groups.items()):
        dfs = [pd.read_parquet(f) for f in files]
        full = pd.concat(dfs, ignore_index=True)
        tables[table_name] = full
        full.to_parquet(CLEAN_TABLES_DIR / f"{table_name}.parquet", index=False)
    return tables


def step5_sanity_checks(tables):
    event = tables.get("event")
    if event is not None and "winner_code" in event.columns:
        print("winner_code values:", sorted(event["winner_code"].dropna().unique().tolist()))

    home_team = tables.get("home_team")
    if home_team is not None and "plays" in home_team.columns:
        print("plays values:", home_team["plays"].dropna().unique().tolist())

    tournament = tables.get("tournament")
    if tournament is not None and "ground_type" in tournament.columns:
        print("ground_type values:", tournament["ground_type"].dropna().unique().tolist())

    stats = tables.get("statistics")
    if stats is not None and "statistic_name" in stats.columns:
        names = stats["statistic_name"].dropna().unique().tolist()
        print(f"statistic_name count: {len(names)} | sample: {names[:20]}")
        if "period" in stats.columns:
            print("period values:", stats["period"].dropna().unique().tolist())


def step6_build_matches_table(tables):
    matches = tables["event"].copy()

    def left_join(base, table_name, prefix):
        if table_name not in tables:
            return base
        other = tables[table_name].add_prefix(f"{prefix}_")
        other = other.rename(columns={f"{prefix}_match_id": "match_id"})
        return base.merge(other, on="match_id", how="left", suffixes=("", f"_{prefix}"))

    matches = left_join(matches, "tournament", "tourn")
    matches = left_join(matches, "season", "season")
    matches = left_join(matches, "venue", "venue")
    matches = left_join(matches, "round", "round")
    matches = left_join(matches, "time", "time")
    matches = left_join(matches, "home_team_score", "hscore")
    matches = left_join(matches, "away_team_score", "ascore")
    matches = left_join(matches, "home_team", "home")
    matches = left_join(matches, "away_team", "away")

    matches.to_csv(FINAL_DIR / "matches_clean.csv", index=False)
    return matches


def step7_build_players_table(tables, matches):
    if "home_team" not in tables or "away_team" not in tables:
        return None

    home_p = tables["home_team"].copy()
    away_p = tables["away_team"].copy()
    players_long = pd.concat([home_p, away_p], ignore_index=True)

    key_col = "player_id" if "player_id" in players_long.columns else "name_code"

    keep_cols = [c for c in [
        key_col, "name", "full_name", "slug", "gender", "country",
        "residence", "birthplace", "height", "weight", "plays", "turned_pro",
    ] if c in players_long.columns]

    players_unique = (
        players_long[keep_cols]
        .dropna(subset=[key_col])
        .drop_duplicates(subset=[key_col], keep="first")
        .reset_index(drop=True)
    )

    home_id_col = f"home_{key_col}"
    away_id_col = f"away_{key_col}"
    if {"winner_code", home_id_col, away_id_col}.issubset(matches.columns):
        winner_id = matches.apply(
            lambda r: r[home_id_col] if r["winner_code"] == 1
            else (r[away_id_col] if r["winner_code"] == 2 else None),
            axis=1,
        )
        wins = winner_id.value_counts().rename_axis(key_col).reset_index(name="wins")
        players_unique = players_unique.merge(wins, on=key_col, how="left")
        players_unique["wins"] = players_unique["wins"].fillna(0).astype(int)

    players_unique.to_csv(FINAL_DIR / "players_clean.csv", index=False)
    return players_unique


def main():
    inner_zip = step1_extract_outer()
    daily_zips = step2_extract_daily_zips(inner_zip)
    all_files = step3_flatten_parquet(daily_zips)
    tables = step4_build_clean_tables(all_files)
    step5_sanity_checks(tables)
    matches = step6_build_matches_table(tables)
    step7_build_players_table(tables, matches)
    print("Done. Final files in:", FINAL_DIR.resolve())


if __name__ == "__main__":
    main()
