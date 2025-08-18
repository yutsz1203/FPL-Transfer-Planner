import requests
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from const import base_url, matches_api, header, league_id, season_id, team_ids, team_id_map, wait

gw = int(input("Enter gameweek number: "))
current_season_team = []

wait("current season team strengths")
print(f"{gw} down, {38-gw} to go. The league is {round(gw/38 * 100.0, 2)}% done.")
print(f"Start fetching team statistics for current season after gameweek {gw}...")
print("*" * 90)

for team_id in team_ids:
    response = requests.get(base_url + matches_api,
                        params={"team_id": team_id, "season_id": "2024-2025", "league_id": league_id},
                        headers=header)
    data = response.json()["data"]
    team_name = team_id_map[team_id]
    print(f"Fetching data for {team_name} as at Gameweek {gw}...")
    gf, ga, h_gf, h_ga, a_gf, a_ga, h_games, a_games = 0, 0, 0, 0, 0, 0, 0, 0
    for i in range(gw):
        match = data[i]
        # skipping bgw
        if not match["match_id"]:
             print(f"Blank gameweek for {team_name}")
             break
        if match["home_away"] == "Home":
            h_gf += match["gf"]
            h_ga += match["ga"]
            h_games += 1
        else:
            a_gf += match["gf"]
            a_ga += match["ga"]
            a_games += 1
        gf += match["gf"]
        ga += match["ga"]
    
    current_season_team.append({
        "team": team_name,
        "games": h_games + a_games,
        "gf": gf,
        "ga": ga,
        "h_games": h_games,
        "h_gf": h_gf,
        "h_ga": h_ga,
        "a_gf": a_gf,
        "a_ga": a_ga,
        "a_games": a_games
    })
    if team_name == "Wolves":
            print("Fetches statistics for all teams from Premier League in the last season.")
    else:
        print("*" * 90)
        wait("next team.")
    print(f"Fetched {team_name}. Fetching next team.")
    print("*" * 90)

df = pd.DataFrame(current_season_team)

# Strength Calculation
lod = df["gf"].sum() / df["games"].sum()
df["Oi"] = df["gf"] / df["games"] / lod
df["Oi"] = df["Oi"].round(2)
df["Di"] = df["ga"] / df["games"] / lod
df["Di"] = df["Di"].round(2)

h_lod = df["h_gf"].sum() / df["h_games"].sum()
df["h_Oi"] = df["h_gf"] / df["h_games"] / h_lod
df["h_Oi"] = df["h_Oi"].round(2)
df["h_Di"] = df["h_ga"] / df["h_games"] / h_lod
df["h_Di"] = df["h_Di"].round(2)

a_lod = df["a_gf"].sum() / df["a_games"].sum()
df["a_Oi"] = df["a_gf"] / df["a_games"] / a_lod
df["a_Oi"] = df["a_Oi"].round(2)
df["a_Di"] = df["a_ga"] / df["a_games"] / a_lod
df["a_Di"] = df["a_Di"].round(2)

print(df)
df.to_csv("teams/data/2526-prem-teams-last5games.csv", index=False)
        
