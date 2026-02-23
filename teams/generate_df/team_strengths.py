import json
import os
import sys

import pandas as pd
import soccerdata as sd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from const import (  # noqa: E402
    TEAMS_DATA_DIR,
    TEAMS_RESULTS_DIR,
    season,
)


def strength_calculation(df):
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


if __name__ == "__main__":
    n = int(input("Enter number of last n gameweeks to include in calculation: "))

    leagues = sd.MatchHistory.available_leagues()
    for league in leagues:
        league_code, league_name = league.split("-")
        gw = int(input(f"Enter gameweek number for {league_name}: "))
        current_season_team = []
        lastngames_team = []

        mh = sd.MatchHistory(leagues=league, seasons=season)
        hist = mh.read_games()
        cols = ["home_team", "away_team", "FTHG", "FTAG"]
        hist_df = hist[cols]
        hist_df.reset_index(drop=True, inplace=True)

        with open(TEAMS_DATA_DIR / "teams.json", "r", encoding="utf-8") as file:
            teams = json.load(file)

        for team in teams[league_name]:
            season_df = hist_df.loc[
                (hist_df["home_team"] == team) | (hist_df["away_team"] == team)
            ]
            season_home_df = season_df.loc[season_df["home_team"] == team]
            season_away_df = season_df.loc[season_df["away_team"] == team]

            h_games = len(season_home_df)
            h_gf = season_home_df["FTHG"].sum()
            h_ga = season_home_df["FTAG"].sum()

            a_games = len(season_away_df)
            a_gf = season_away_df["FTAG"].sum()
            a_ga = season_away_df["FTHG"].sum()

            current_season_team.append(
                {
                    "team": team,
                    "games": len(season_df),
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

            lastn_df = season_df.tail(min(n, gw))
            lastn_home_df = lastn_df.loc[lastn_df["home_team"] == team]
            lastn_away_df = lastn_df.loc[lastn_df["away_team"] == team]

            lastn_h_games = len(lastn_home_df)
            lastn_h_gf = lastn_home_df["FTHG"].sum()
            lastn_h_ga = lastn_home_df["FTAG"].sum()

            lastn_a_games = len(lastn_away_df)
            lastn_a_gf = lastn_away_df["FTAG"].sum()
            lastn_a_ga = lastn_away_df["FTHG"].sum()

            lastngames_team.append(
                {
                    "team": team,
                    "games": len(lastn_df),
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

        current_season_df = pd.DataFrame(current_season_team)
        strength_calculation(current_season_df)
        current_season_df.sort_values(by=["Oi"], ascending=False, inplace=True)
        current_season_df.set_index("team", inplace=True)
        file_path = TEAMS_RESULTS_DIR / f"{league_code}_teams_currentseason.csv"
        current_season_df.to_csv(file_path)
        print(f"Team strengths of current season saved to {file_path}")

        lastngames_df = pd.DataFrame(lastngames_team)
        strength_calculation(lastngames_df)
        lastngames_df.sort_values(by=["Oi"], ascending=False, inplace=True)
        lastngames_df.set_index("team", inplace=True)
        file_path = TEAMS_RESULTS_DIR / f"{league_code}_teams_last{n}games.csv"
        lastngames_df.to_csv(file_path)
        print(f"Team strengths of last {n} games saved to {file_path}")
