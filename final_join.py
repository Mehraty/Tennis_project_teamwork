"""
ساخت جدول‌های نهاییِ تحلیل‌پذیر از روی جدول‌های تمیزشده در cleaned_Yasi.
"""

import pandas as pd
from pathlib import Path

CLEAN_TABLES_DIR = Path(r"tennis_project/cleaned_Yasi")   # مسیر واقعی خودت را جایگزین کن
FINAL_DIR = Path(r"tennis_project/05_final")
FINAL_DIR.mkdir(parents=True, exist_ok=True)

# فقط جدول‌های "یک‌ردیف‌به‌ازای‌هر‌مسابقه" را می‌خوانیم.
# statistics / pbp / power / odds / votes عمداً اینجا join نمی‌شوند چون
# چند ردیف به‌ازای هر match_id دارند (فرمت long)؛ آن‌ها را جدا و فقط
# هنگام نیاز (مثلاً استخراج آس‌ها) فیلتر می‌کنیم.
WIDE_TABLES = [
    "event", "tournament", "season", "venue", "round",
    "time", "home_team_score", "away_team_score", "home_team", "away_team",
]

tables = {name: pd.read_parquet(CLEAN_TABLES_DIR / f"{name}.parquet") for name in WIDE_TABLES}

# ---------------------------------------------------------------------
# matches_clean.csv
# ---------------------------------------------------------------------
matches = tables["event"].copy()


def left_join(base, table_name, prefix):
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
print("matches_clean.csv ساخته شد. شکل:", matches.shape)

# ---------------------------------------------------------------------
# players_clean.csv
# ---------------------------------------------------------------------
home_p = tables["home_team"].copy()
away_p = tables["away_team"].copy()
players_long = pd.concat([home_p, away_p], ignore_index=True)

key_col = "player_id" if "player_id" in players_long.columns else "name_code"

keep_cols = [c for c in [
    key_col, "name", "full_name", "slug", "gender", "country",
    "residence", "birthplace", "height", "weight", "weight_flag",
    "plays", "turned_pro",'current_rank',
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
print("players_clean.csv ساخته شد. شکل:", players_unique.shape)

print("\nتمام شد. فایل‌های نهایی در:", FINAL_DIR.resolve())