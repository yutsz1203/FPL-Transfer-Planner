# url: https://fantasy.premierleague.com/api/entry/{team-id}/event/{GW}/picks/
# table schema: # Name, Pos, Team, Cost, Total Points, Points/Game, Points/Million, Goals, xG, Assists, xA, xGI, h_Goals, hxG, h_Assists, hxA, hxGI, a_Goals, axG, a_Assists, axA, axGI, GC, xGc, h_Gc, hxGc, a_Gc, axGc, Clean Sheets, Defensive Contribution, Saves, Bonus
# import player stats df
import pandas as pd
import requests
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from const import official_base_url, fpl_id

def get_myteam_season_stats():
    players_df = pd.read_csv("players/results/player_season_stats.csv")
    gw = int(input("Enter current gameweek number: "))
    response = requests.get(official_base_url + f"entry/{fpl_id}/event/{gw}/picks/")
    players = response.json()["picks"]
    player_ids = [player["element"] for player in players]
    new_df = players_df[players_df["Player ID"].isin(player_ids)] 
    new_df.to_csv("myteam/results/myteam_season_stats.csv", index=False)
    print(new_df.to_string(index=False))

if __name__ == "__main__":
    get_myteam_season_stats()