## Preseason Preperation

1. team_id.py

- Get team_id of promoted teams, and add to team_id_map
- Remove team_id of relegated teams from team_id_map

2. team_stats.py

- Purpose:
  - Get team data of Premier League and Championship from last season.
- Output:
  - {previous-season}-prem-teams.csv
  - {previous-season}-championship-teams.csv

3. team_strengths.py

- Purpose:
  - Calculate offensive strength (Oi) and defensive strength (Di) of each team, and mean variable (lod) for the league.
  - Remove relegated team, add promoted team, and form new df for the current season.
- Input:
  - {previous-season}-prem-teams.csv
  - {previous-season}-championship-teams.csv
- Output:
  - {current-season}-prem-teams-pastseason.csv

4. adjust_team_strengths.py

- Purpose:
  - Adjust the Oi and Di for newly promoted teams
  - For teams that were in the prem within the last two years, we search for that particular year
  - Input:
    - {current-season}-prem-teams-pastseason.csv
- Output:
  - {current-season}-prem-teams-pastseason.csv

## Functions

1. Project the next 5 gameweek of every team
2. Project best players for each team according to the projection at (2)
3. Players (last 5)
4. Next game week calculation.
   - opponent projection
   - gambling matrix

## Calculation timeframe

1. Current season (update every week)
2. Rolling 5 (starts at gw5)
3. Incorporate with last season (always maintain 38 gameweeks)
   - do teams that were in prem last season
   - then think about promoted teams

## References

- fbref api: https://fbrapi.com/documentation

## Note

- Please refer to the new_ver, as I won't be updating old_ver anymore
