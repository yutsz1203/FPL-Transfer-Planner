# url: https://fantasy.premierleague.com/api/entry/{team-id}/event/{GW}/picks/
# Table schema: Name, Pos, Team, Cost, Expected returns (xGI * O_Di), Expected goal conced, team_Oi, team_Di, opponent_Oi, opponent_Di, opponents
# import player stats df

import os
import sys

import pandas as pd
import requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from const import (  # noqa: E402
    PLAYERS_PROJECTION_DIR,
    MYTEAM_PROJECTION_DIR,
    fpl_id,
    official_base_url,
)


def get_myteam_projection_nextgw(gw, type, n=1):
    if type == "lastngames":
        players_df = pd.read_csv(
            PLAYERS_PROJECTION_DIR / f"players_next_gameweek_last{n}games.csv"
        )
    else:
        players_df = pd.read_csv(
            PLAYERS_PROJECTION_DIR / "players_next_gameweek_currentseason.csv"
        )
    response = requests.get(official_base_url + f"entry/{fpl_id}/event/{gw}/picks/")
    players = response.json()["picks"]
    player_ids = [player["element"] for player in players]
    new_df = players_df[players_df["Player ID"].isin(player_ids)]
    if type == "lastngames":
        file_path = MYTEAM_PROJECTION_DIR / f"myteam_nextgw_projection_last{n}games.csv"
        new_df.to_csv(file_path, index=False)
        print(
            f"Player projection of next gameweek from my team using data from last {n} games saved to {file_path}"
        )
    else:
        file_path = MYTEAM_PROJECTION_DIR / "myteam_nextgw_projection_currentseason.csv"
        new_df.to_csv(file_path, index=False)
        print(
            f"Player projection of next gameweek from my team using data from current season saved to {file_path}"
        )
    print(new_df.to_string(index=False))


def get_myteam_projection_nextngw(gw, type, n=1, ngw=5):
    if type == "lastngames":
        players_df = pd.read_csv(
            PLAYERS_PROJECTION_DIR / f"players_next{ngw}gameweeks_last{n}games.csv"
        )
    else:
        players_df = pd.read_csv(
            PLAYERS_PROJECTION_DIR / f"players_next{ngw}gameweeks_currentseason.csv"
        )
    response = requests.get(official_base_url + f"entry/{fpl_id}/event/{gw}/picks/")
    players = response.json()["picks"]
    player_ids = [player["element"] for player in players]
    new_df = players_df[players_df["Player ID"].isin(player_ids)]
    if type == "lastngames":
        file_path = MYTEAM_PROJECTION_DIR / f"myteam_next{ngw}gws_last{n}games.csv"
        new_df.to_csv(file_path, index=False)
        print(
            f"Player projection of next {ngw} gameweeks from my team using data from current season saved to {file_path}"
        )
    else:
        file_path = MYTEAM_PROJECTION_DIR / f"myteam_next{ngw}gws_currentseason.csv"
        new_df.to_csv(file_path, index=False)
        print(
            f"Player projection of next {ngw} gameweeks from my team using data from current season saved to {file_path}"
        )
    print(new_df.to_string(index=False))


if __name__ == "__main__":
    gw = int(input("Enter current gameweek number: "))
    n = int(input("Enter n, number of previous games taking into account: "))
    get_myteam_projection_nextgw(gw, "currentseason")
    get_myteam_projection_nextngw(gw, "currentseason")
