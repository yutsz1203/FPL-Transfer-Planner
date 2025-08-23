# url: https://fantasy.premierleague.com/api/entry/{team-id}/event/{GW}/picks/
# Table schema: Name, Pos, Team, Cost, Expected returns (xGI * O_Di), Expected goal conced, team_Oi, team_Di, opponent_Oi, opponent_Di, opponents
# import player stats df

import pandas as pd
import requests
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from const import official_base_url, fpl_id

def get_myteam_projection_nextgw(gw, type, n=1):
    if type == "lastngames":
        players_df = pd.read_csv(f"players/projection/next_gameweek_last{n}games.csv")
    else:
        players_df = pd.read_csv(f"players/projection/next_gameweek_currentseason.csv")
    response = requests.get(official_base_url + f"entry/{fpl_id}/event/{gw}/picks/")
    players = response.json()["picks"]
    player_ids = [player["element"] for player in players]
    new_df = players_df[players_df["Player ID"].isin(player_ids)]
    if type == "lastngames":
        new_df.to_csv(f"myteam/projection/myteam_last{n}games_projection_nextgw.csv", index=False)
        print(f"Player stats of my teams using data from current season saved to myteam/results/myteam_currentseason_stats.csv")
    else:
        new_df.to_csv(f"myteam/projection/myteam_currentseason_projection_nextgw.csv", index=False)
        print(f"Player stats of my teams using data from current season saved to myteam/results/myteam_currentseason_stats.csv")
    print(new_df.to_string(index=False))

def get_myteam_projection_nextngw(gw, type, n=1, ngw=5):
    if type == "lastngames":
        players_df = pd.read_csv(f"players/projection/next_{ngw}_gameweeks_last{n}games.csv")
    else:
        players_df = pd.read_csv(f"players/projection/next_{ngw}_gameweeks_currentseason.csv")
    response = requests.get(official_base_url + f"entry/{fpl_id}/event/{gw}/picks/")
    players = response.json()["picks"]
    player_ids = [player["element"] for player in players]
    new_df = players_df[players_df["Player ID"].isin(player_ids)] 
    if type == "lastngames":
        new_df.to_csv(f"myteam/projection/myteam_next{ngw}gws_last{n}games.csv", index=False)
        print(f"Player stats of my teams using data from current season saved to myteam/results/myteam_currentseason_stats.csv")
    else:
        new_df.to_csv(f"myteam/projection/myteam_next{ngw}gws_currentseason.csv", index=False)
        print(f"Player stats of my teams using data from current season saved to myteam/results/myteam_currentseason_stats.csv")
    print(new_df.to_string(index=False))

if __name__ == "__main__":
    gw = int(input("Enter current gameweek number: "))
    n = int(input("Enter n, number of previous games taking into account: "))
    get_myteam_projection_nextgw(gw, "currentseason")
    get_myteam_projection_nextngw(gw, "currentseason")