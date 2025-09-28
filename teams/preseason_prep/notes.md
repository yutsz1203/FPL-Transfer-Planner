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
