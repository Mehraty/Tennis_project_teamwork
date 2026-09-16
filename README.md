# Tennis Match Data Analysis — Bootcamp Project

A data analysis bootcamp project: cleaning and analyzing a raw tennis
match dataset (season 2024), then answering a set of analytical
questions about players, matches, and betting/fan behavior.

## Team

Three-person team, working on separate branches (`name1`, `name2`,
`name3` — rename to actual usernames) and merging into `main` via
Pull Requests.

## ⚠️ About the dataset

**The dataset used in this project is private and is NOT included in
this repository.** All data files (`*.parquet`, `*.csv`, and the
working folders `data/`, `tennis_project/`, `cleaned_Yasi/`) are
excluded via `.gitignore`. To run this project's code, each team
member must obtain the dataset separately (from the bootcamp/course
source) and place it locally according to the folder structure below
— it will never be pushed to this repository.

The dataset consists of 15 parquet tables linked by `match_id`,
covering match results, player info, set scores, tournament/venue
details, point-by-point data, betting odds, and fan votes.

## Repository structure

```
tennis-data-analysis/
├── README.md
├── .gitignore
├── docs/
│   └── tennis_dataset_schema.pdf       # full schema documentation
├── cleaning/
│   ├── cleaning_Yasi.ipynb             # cleans event, home/away_team,
│   │                                    # home/away_team_score, time,
│   │                                    # tournament, round
│   ├── cleaning_7_Yasi.ipynb           # cleans statistics, pbp, power,
│   │                                    # odds, venue, votes, season
│   ├── final_join.py                   # builds matches_clean.csv /
│   │                                    # players_clean.csv
│   └── rules_check_scores.py           # flags matches with impossible
│                                        # set scores (tennis-rule check)
├── analysis/
│   ├── part1_questions_1_2_3_10_12_13_15.ipynb
│   ├── part1_questions_...ipynb        # remaining part-1 questions
│   └── part2_bonus_questions.ipynb     # fan votes vs betting market,
│                                        # aces vs surface/winner, etc.
└── data/                               # gitignored — place the raw
                                         # dataset here locally
```

## How to run

1. Place the raw dataset (15 parquet files) under `data/`.
2. Run the notebooks in `cleaning/` in order to produce cleaned tables.
3. Run `cleaning/final_join.py` to build `matches_clean.csv` and
   `players_clean.csv`.
4. Run `cleaning/rules_check_scores.py` to flag matches with invalid
   set scores (used by several downstream analyses).
5. Run the notebooks in `analysis/` — each answers a specific set of
   questions and is independent of the others.

## Questions answered so far

**Part 1 (required questions):**
- Q1 — Number of unique players, plus an investigation into whether
  the home/away label is systematically biased for individual players
- Q2 — Average player height, broken down by gender
- Q3 — Player with the most wins
- Q10 — Correlation between height and current ranking
- Q12 — Average games per set, men vs women (filtered to matches with
  valid, complete set scores)
- Q13 — Distribution of right-handed vs left-handed players
- Q15 — Number of distinct player countries

**Part 2 (bonus / self-designed questions):**
- Does the match winner tend to hit more aces than the loser?
- Does court surface affect the number of aces per match?
- Do fan votes or the betting market predict the winner more
  accurately?
- Is fan vote share systematically biased toward the "home" label, or
  does it reflect genuine ranking differences?

## Known data-quality findings

- ~27–31% of matches lack player info rows (`home_team`/`away_team`) —
  a structural gap in the source data, not a cleaning error.
- The `round` table only covers ~55% of matches.
- `current_rank` reflects a player's ranking at data-collection time,
  not their ranking at the time of each specific match.
- ~2.2% of matches have an impossible set score (fewer than 6 total
  games in a set); investigation traced this to genuine retirements
  concentrated at lower tournament tiers (ITF/Challenger), not a data
  collection bug — see `docs/tennis_dataset_schema.pdf` and
  `cleaning/rules_check_scores.py` for the full investigation.

## Tools

Python 3.12, pandas, pyarrow/fastparquet, numpy, matplotlib, scipy
