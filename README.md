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

## Using the planner

After Gameweek ended

1. get new players: (get_players.py)
2. team_strengths: get team strengths of current season and last n games
3. (only for fixture changes)fixtures: get fixtures (get_fixtures.py)
4. team projection: get_next_gameweek and get_next_n_gameweek (fixture_projection.py)
5. player stats: get player stats of current season and last n games (player_stats.py)
6. player projection: get_next_gameweek and get_next_n_gameweek (player_projection.py)
7. myteam: get player stats and player projection from my team (myteam_stats, myteam_projection)

## Tasks

- file importing / exporting (use pathlib to add project path to const.py)
- fixture_projection.py: import data of teams from last n games
- next 5 gws projection (player_projection.py)
- change getting last 5 games of team strengths to last n games (team_strengths.py)
- calculate current gameweek player stats & team stats
- calculate augmented team strengths

## References

- fbref api: https://fbrapi.com/documentation
- official api guide: https://www.oliverlooney.com/blogs/FPL-APIs-Explained#how-to-use-authenticated-endpoints

## Note

- Please refer to the new_ver, as I won't be updating old_ver anymore
- official api and fbref api have name differences:
  Leeds -> Leeds United
  Man City -> Manchester City
  Man Utd -> Manchester United
  Newcastle -> Newcastle Utd
  Spurs -> Tottenham
