# May need to fetch again whenever there are bgw or dgw
import requests
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from const import base_url, matches_api, header, league_id, season_id, team_ids, team_id_map, wait

wait("fixtures")
print(f"Start fetching fixtures for all teams...")
print("*" * 90)

data = []

for team_id in team_ids:
    response = requests.get(
            base_url + matches_api,
            params={"team_id": team_id, "league_id": league_id, "season_id": season_id},
            headers=header)
    matches = response.json()["data"]
    team_name = team_id_map[team_id]
    fixtures = [team_name]
    print(f"Fetching fixtures for {team_name}...")
    for match in matches:
        opponent = match["opponent"]
        side = match["home_away"][-4]
        fixtures.append(f"{opponent}({side})")
        print(f"{opponent}({side})")
    data.append(fixtures)
    if team_name == "Wolves":
        print("Finished fetching fixtures of all teams")
    else:
        print("*" * 90)
        wait("fixtures of next team")
    print("*" * 90)
columns = ["team"] + [f"GW{i}" for i in range(1, 39)]
df = pd.DataFrame(data, columns=columns)
print(df)
df.to_csv("teams/data/fixtures.csv", index=False)
print("Fixtures saved to teams/data/fixtures.csv")
