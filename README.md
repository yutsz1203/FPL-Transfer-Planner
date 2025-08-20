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
4. Last season (only used for first draft of the season)

## Using the planner

After Gameweek ended

1. team_strengths: get team strengths of current season and last n games
2. (only for fixture changes)fixtures: get fixtures (get_fixtures.py)
3. team projection: get_next_gameweek and get_next_n_gameweek (fixture_projection.py)
4. player stats: get player stats of current season and last n games (player_stats.py)
5. player projection: get_next_gameweek and get_next_n_gameweek (player_projection.py)
6. myteam: get player stats and player projection from my team (myteam_stats, myteam_projection)
7. get new players: (get_players.py)

## Tasks

- fixture_projection.py: import data of teams from last n games
- next 5 gws projection (player_projection.py)
- change getting last 5 games of team strengths to last n games (team_strengths.py)
- calculate augmented team strengths

## Finished

- Fetch fixtures (Need adjust for double gameweek)
- Last season team strengths
- Current season team strength
- Next gameweek projections (team strength)
- Next n gameweeks projections (team strength)
- calculate last 5 games team strengths
- get players basic information (id, team, pos, price, selected by)
- calculate player current season stats, calculate player last 5 games stats (use official api) (player_stats.py)
- season stats and last 5 games stats of my own team (myteam_stats.py)
- next gameweek projection

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
