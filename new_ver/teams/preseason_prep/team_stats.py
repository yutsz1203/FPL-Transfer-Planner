import time
import requests
import pandas as pd
import sys
import os

# Add the new_ver directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from const import base_url, header, matches_api, league_id, team_ids, team_id_map, team_id_map_2223, team_id_map_2324, wait

prem_teams = []
# season_id = "2024-2025"
# season_id = "2022-2023" #for leeds
season_id = "2023-2024" # for burnley
for i in range(10,-1,-1):
        print(f"Waiting for {i} seconds before starting data fetch...")
        time.sleep(1)

for team_id in team_id_map_2324.keys():
    # skip promoted teams
    team_name = team_id_map_2324[team_id]
    # Skip promoted teams
    # if team_id in ["943e8050", "5bfb9659", "8ef52968"]:
    #      continue
    print(f"Fetching data for {team_name}...")
    response = requests.get(base_url + matches_api,
                        params={"team_id": team_id, "season_id": season_id, "league_id": league_id},
                        headers=header)
    data = response.json()["data"]
    gf, ga, h_gf, h_ga, a_gf, a_ga = 0, 0, 0, 0, 0, 0
    for match in data:
        if match["home_away"] == "Home":
            h_gf += match["gf"]
            h_ga += match["ga"]
        else:
            a_gf += match["gf"]
            a_ga += match["ga"]
        gf += match["gf"]
        ga += match["ga"]

    prem_teams.append({
        "team": team_name,
        "gf": gf,
        "ga": ga,
        "h_gf": h_gf,
        "h_ga": h_ga,
        "a_gf": a_gf,
        "a_ga": a_ga
    })
    if team_name == "Wolves":
            print("Fetches statistics for all teams from Premier League in the last season.")
    else:
        wait("team")
    print(f"Fetched {team_name}. Fetching next team.")
    print("*" * 90)

last_season_prem_teams_df = pd.DataFrame(prem_teams)
print(last_season_prem_teams_df)
last_season_prem_teams_df.to_csv("teams/data/2324-prem-teams.csv", index=False)

