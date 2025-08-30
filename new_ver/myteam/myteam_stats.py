# url: https://fantasy.premierleague.com/api/entry/{team-id}/event/{GW}/picks/
# table schema: # Name, Pos, Team, Cost, Total Points, Points/Game, Points/Million, Goals, xG, Assists, xA, xGI, h_Goals, hxG, h_Assists, hxA, hxGI, a_Goals, axG, a_Assists, axA, axGI, GC, xGc, h_Gc, hxGc, a_Gc, axGc, Clean Sheets, Defensive Contribution, Saves, Bonus
# import player stats df
import os
import sys

import pandas as pd
import requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from const import fpl_id, official_base_url, PLAYERS_RESULT_DIR, MYTEAM_RESULT_DIR  # noqa: E402


def get_myteam_season_stats(gw):
    players_df = pd.read_csv(PLAYERS_RESULT_DIR / "players_currentseason.csv")
    response = requests.get(official_base_url + f"entry/{fpl_id}/event/{gw}/picks/")
    players = response.json()["picks"]
    player_ids = [player["element"] for player in players]
    new_df = players_df[players_df["Player ID"].isin(player_ids)]
    file_path = MYTEAM_RESULT_DIR / "myteam_currentseason_stats.csv"
    new_df.to_csv(file_path, index=False)
    print(new_df.to_string(index=False))
    print(
        f"Player stats of my teams using data from current season saved to {file_path}"
    )


# change last5games to lastngames
def get_myteam_lastn_stats(gw, n):
    players_df = pd.read_csv(PLAYERS_RESULT_DIR / f"players_last{n}games.csv")
    response = requests.get(official_base_url + f"entry/{fpl_id}/event/{gw}/picks/")
    players = response.json()["picks"]
    player_ids = [player["element"] for player in players]
    new_df = players_df[players_df["Player ID"].isin(player_ids)]
    file_path = MYTEAM_RESULT_DIR / f"myteam_last{n}games_stats.csv"
    new_df.to_csv(file_path, index=False)
    print(new_df.to_string(index=False))
    print(
        f"Player stats of my teams using data from last {n} games saved to {file_path}"
    )


if __name__ == "__main__":
    gw = int(input("Enter current gameweek number: "))
    n = int(input("Enter the number of gameweeks to use in stats calculation: "))
    get_myteam_season_stats(gw)
    get_myteam_lastn_stats(gw, n)
