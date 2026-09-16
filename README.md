# Tennis Match Data Analysis — Bootcamp Project

A data analysis bootcamp project: cleaning and analyzing a raw tennis
match dataset, then answering a set of analytical
questions about players, matches, and betting/fan behavior.

## Team

A three-person team worked on separate branches (`@YasamanAghaei`, `@mehraty`, `name3`);
you can view each person's code in the respective branches.

## ⚠️ About the dataset

The dataset used in this project is private and is not included in this repository. All data files (`*.parquet`, `*.csv`) have been excluded via the `.gitignore` file. Due to the private nature of the data and out of respect for the database creator's privacy, the dataset file will not be made available here, in accordance with their request.

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
│   └── clean_tennis_data_en.py       # Creating 15 tables based on `tennis_dataset_schema.pdf` using the available data.
│   └── cleaning_7.ipynb
│                # statistics, pbp, power, odds, venue, votes, season
│   └── cleaning_8.ipynb
│                # event, home_team, away_team, home_team_score, away_team_score, time, tournament, round
│   └── final_join.py
│                # builds matches_clean.csv / players_clean.csv
|   └── Tennis_Scoring_Rule_Validator.ipynb
│                # flags matches with impossible
│                # set scores (tennis-rule check)
├──  keyvan_hajizadeh
|   └── Questions: 7, 8, 12, 16, 17 and 2 optional question
├──  yasaman_aghaei
|   └── Questions: 3, 4, 5, 6, 9, 11, 14 and 2 optional question
├──  mehrnoush_yaghoubi
|   └── Questions: 1, 2, 10, 13, 15 and 2 optional question
```

## Questions answered so far

**Part 1 (required questions):**
1. How many tennis players are included in the dataset? 
2. What is the average height of the players? 
3. Which player has the highest number of wins? 
4. What is the longest match recorded in terms of duration? 
5. How many sets are typically played in a tennis match? 
6. Which country has produced the most successful tennis players? 
7. What is the average number of aces per match? 
8. Is there a difference in the number of double faults based on gender? 
9. Which player has won the most tournaments in a single month? 
10. Is there a correlation between a player's height and their ranking? 
11. What is the average duration of matches? 
12. What is the average number of games per set in men's matches compared to women's matches?  
13. What is the distribution of left-handed versus right-handed players? 
14. What is the most common type of surface used in tournaments? 
15. How many distinct countries are represented in the dataset? 
16. Which player has the highest winning percentage against top 10 ranked opponents? 
17. What is the average number of breaks of serve per match? 

**Part 2 (bonus / self-designed questions):**
1. Does the winner usually hit more aces?
2. Does the court surface affect the number of aces?
3. Does the match duration depend on the court surface?
4. Do players' performances change with the court surface (e.g., clay vs. hard court)?
5. Is the voting share systematically biased toward the home player?
6. Comparing public/fan opinions with the betting market: which made better predictions?

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
  `cleaning/Tennis_Scoring_Rule_Validator.ipynb` for the full investigation.

## Tools

+Python 3.10, pandas, pyarrow/fastparquet, numpy, matplotlib, scipy
