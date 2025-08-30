## Repo Structure

```text
new_ver
├── myteam
│   └── projection
│   └── results
│   └── myteam_projection.py
│   └── myteam_stats.py
│
├── players
│   └── data
│   │      └── players.csv
│   └── generate_df
│   │      └── get_players.py
│   │      └── player_stats.py
│   └── projection
│   └── results
│   └── player_projection.py
│
├── Machine Learning
│   ├── Applications
│   │      └── Mixed
│   │      └── Supervised Learning
│   │      └── Regression
│   │
│   └── Models
│          └── Supervised Learning
│          └── Classification
│          └── Regression
│
├── OOP
│
└── Python
    ├── Built-in Modules
    │   └── datetime
    │   └── os
    │   └── pathlib
    │
    └── File Objects
```

## Using the planner

Only for any fixture changes (BGW / DGW)

1. get fixtures (get_fixtures.py)

After Gameweek ended

1. get new players: (get_players.py)
2. team_strengths: get team strengths of current season and last n games (team_strengths.py)
3. team projection: get_next_gameweek and get_next_n_gameweek (fixture_projection.py)
4. player stats: get player stats of current season and last n games (player_stats.py)
5. player projection: get_next_gameweek and get_next_n_gameweek (player_projection.py)
6. myteam: get player stats and player projection from my team (myteam_stats, myteam_projection)

## References

- fbref api: https://fbrapi.com/documentation
- official api guide: https://www.oliverlooney.com/blogs/FPL-APIs-Explained#how-to-use-authenticated-endpoints
