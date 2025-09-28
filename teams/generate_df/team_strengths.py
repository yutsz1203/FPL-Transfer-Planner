import os
import sys

import pandas as pd
import requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from const import (  # noqa: E402
    base_url,
    header,
    league_id,
    matches_api,
    season_id,
    team_id_map,
    team_ids,
    wait,
    TEAMS_RESULTS_DIR,
)


def strength_calculation(df):
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


gw = int(input("Enter gameweek number: "))
n = int(input("Enter number of last n gameweeks to include in calculation: "))
current_season_team = []
lastngames_team = []

wait("match statistics")
print(f"{gw} down, {38-gw} to go. The league is {round(gw/38 * 100.0, 2)}% done.")
print(f"Start fetching team statistics after gameweek {gw}...")
print("*" * 90)

for team_id in team_ids:
    response = requests.get(
        base_url + matches_api,
        params={"team_id": team_id, "season_id": season_id, "league_id": league_id},
        headers=header,
    )
    data = response.json()["data"]
    team_name = team_id_map[team_id]
    print(f"Fetching data for {team_name} as at Gameweek {gw}...")
    h_gf, h_ga, a_gf, a_ga, h_games, a_games = 0, 0, 0, 0, 0, 0
    lastn_h_gf, lastn_h_ga, lastn_a_gf, lastn_a_ga, lastn_h_games, lastn_a_games = (
        0,
        0,
        0,
        0,
        0,
        0,
    )
    for i in range(gw):
        match = data[i]
        # skipping bgw
        if not match["match_id"]:
            print(f"Blank gameweek for {team_name}")
            break
        # i = 4 for gw 5, 0-4 are last 5
        if i >= gw - n:  # changed here, if have bug check out this line
            if match["home_away"] == "Home":
                lastn_h_gf += match["gf"]
                lastn_h_ga += match["ga"]
                lastn_h_games += 1
                h_gf += match["gf"]
                h_ga += match["ga"]
                h_games += 1
            else:
                lastn_a_gf += match["gf"]
                lastn_a_ga += match["ga"]
                lastn_a_games += 1
                a_gf += match["gf"]
                a_ga += match["ga"]
                a_games += 1
            print(f"Gameweek{i+1}")
        else:
            if match["home_away"] == "Home":
                h_gf += match["gf"]
                h_ga += match["ga"]
                h_games += 1
            else:
                a_gf += match["gf"]
                a_ga += match["ga"]
                a_games += 1

    current_season_team.append(
        {
            "team": team_name,
            "games": h_games + a_games,
            "gf": h_gf + a_gf,
            "ga": h_ga + a_ga,
            "h_games": h_games,
            "h_gf": h_gf,
            "h_ga": h_ga,
            "a_gf": a_gf,
            "a_ga": a_ga,
            "a_games": a_games,
        }
    )

    lastngames_team.append(
        {
            "team": team_name,
            "games": lastn_h_games + lastn_a_games,
            "gf": lastn_h_gf + lastn_a_gf,
            "ga": lastn_h_ga + lastn_a_ga,
            "h_games": lastn_h_games,
            "h_gf": lastn_h_gf,
            "h_ga": lastn_h_ga,
            "a_gf": lastn_a_gf,
            "a_ga": lastn_a_ga,
            "a_games": lastn_a_games,
        }
    )
    if team_name == "Wolves":
        print(
            "Fetches statistics for all teams from Premier League in the last season."
        )
    else:
        print("*" * 90)
        wait("next team.")
    print(f"Fetched {team_name}. Fetching next team.")
    print("*" * 90)

current_season_df = pd.DataFrame(current_season_team)
strength_calculation(current_season_df)
current_season_df.sort_values(by=["Oi"], ascending=False, inplace=True)
print(current_season_df)
file_path = TEAMS_RESULTS_DIR / "teams_currentseason.csv"
current_season_df.to_csv(file_path, index=False)
print(f"Team strengths of current season saved to {file_path}")

lastngames_df = pd.DataFrame(lastngames_team)
strength_calculation(lastngames_df)
lastngames_df.sort_values(by=["Oi"], ascending=False, inplace=True)
print(lastngames_df)
file_path = TEAMS_RESULTS_DIR / f"teams_last{n}games.csv"
lastngames_df.to_csv(file_path, index=False)
print(f"Team strengths of last {n} games saved to {file_path}")
