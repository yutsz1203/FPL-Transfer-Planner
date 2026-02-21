import os
import sys

import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from const import (  # noqa: E402
    TEAMS_DATA_DIR,
    TEAMS_RESULTS_DIR,
    TEAMS_PROJECTION_DIR,
    team_id_map,
    team_ids,
)

fixtures = pd.read_csv(TEAMS_DATA_DIR / "fixtures.csv")

# Only for first gameweek
# last_season_strengths = pd.read_csv("teams/data/2526-prem-teams-lastseason.csv")

# Current season
current_season_strengths = pd.read_csv(TEAMS_RESULTS_DIR / "teams_currentseason.csv")

# Rolling 5
last5games_strengths = pd.read_csv(TEAMS_RESULTS_DIR / "teams_last5games.csv")

# Augmented
# augmented_strengths = pd.read_csv("teams/data/2526-prem-teams-augmented.csv")


def get_next_gameweek(df, type, side_adjustment=True):
    coming_gameweek = int(input("Enter the coming gameweek number: "))
    next_gameweek = []
    gw = f"GW{coming_gameweek}"
    print(f"Projecting gameweek{coming_gameweek} for all teams using {type} stats...")
    print("*" * 90)
    for team_id in team_ids:
        team_name = team_id_map[team_id]
        opponent = fixtures[fixtures["team"] == team_name][gw].values[0][:-3]
        side = fixtures[fixtures["team"] == team_name][gw].values[0][-2]
        if side_adjustment:
            if side == "H":
                print(f"H: {team_name} vs A: {opponent}")
                team_Oi = df[df["team"] == team_name]["h_Oi"].values[0]
                team_Di = df[df["team"] == team_name]["h_Di"].values[0]
                opponent_Oi = df[df["team"] == opponent]["a_Oi"].values[0]
                opponent_Di = df[df["team"] == opponent]["a_Di"].values[0]
            else:
                print(f"H: {opponent} vs A: {team_name}")
                team_Oi = df[df["team"] == team_name]["a_Oi"].values[0]
                team_Di = df[df["team"] == team_name]["a_Di"].values[0]
                opponent_Oi = df[df["team"] == opponent]["h_Oi"].values[0]
                opponent_Di = df[df["team"] == opponent]["h_Di"].values[0]
        else:
            (
                print(f"H: {team_name} vs A: {opponent}")
                if side == "Home"
                else print(f"H: {opponent} vs A: {team_name}")
            )
            team_Oi = df[df["team"] == team_name]["Oi"].values[0]
            team_Di = df[df["team"] == team_name]["Di"].values[0]
            opponent_Oi = df[df["team"] == opponent]["Oi"].values[0]
            opponent_Di = df[df["team"] == opponent]["Di"].values[0]
        next_gameweek.append(
            {
                "team": team_name,
                "side": side,
                "team_Oi": team_Oi,
                "team_Di": team_Di,
                "opponent": opponent,
                "opponent_Oi": opponent_Oi,
                "opponent_Di": opponent_Di,
                "expected_gf": round(team_Oi * opponent_Di, 2),
                "expected_ga": round(team_Di * opponent_Oi, 2),
            }
        )
        if team_name == "Wolves":
            print("Finished fetching all teams for next gameweek.")
        else:
            print("*" * 90)
        print("*" * 90)
    next_gameweek_df = pd.DataFrame(next_gameweek)
    next_gameweek_df.sort_values(by=["expected_gf"], ascending=False, inplace=True)
    file_path = TEAMS_PROJECTION_DIR / f"teams_next_gameweek_{type}.csv"
    next_gameweek_df.to_csv(file_path, index=False)
    print(next_gameweek_df)
    print(f"Team projection of next gameweek using data of {type} saved to {file_path}")


# Uncomment to get the next gameweek opponents
# get_next_gameweek(last_season_strengths, "last_season")


def get_next_n_gameweek(df, type, side_adjustment=True, n=5):
    coming_gameweek = int(input("Enter the coming gameweek number: "))
    next_n_gameweek = []
    print(
        f"Projection gameweek{coming_gameweek}-gw{coming_gameweek+(n-1)} for all teams using {type} stats..."
    )
    print("*" * 90)
    for team_id in team_ids:
        team_name = team_id_map[team_id]
        team_fixtures = fixtures[fixtures["team"] == team_name]
        nextn_gws = [
            team_fixtures[f"GW{i}"].values[0]
            for i in range(coming_gameweek, coming_gameweek + n)
        ]
        opponents = []
        (
            total_team_Oi,
            total_team_Di,
            total_opponents_Oi,
            total_opponents_Di,
            expected_gf,
            expected_ga,
        ) = (0, 0, 0, 0, 0, 0)
        for gw in nextn_gws:
            side = gw[-2]
            opponent = gw[:-3]
            opponents.append(f"({side[0]}) {opponent}")
            if side_adjustment:
                if side == "H":
                    print(f"H: {team_name} vs A: {opponent}")
                    total_team_Oi += df[df["team"] == team_name]["h_Oi"].values[0]
                    total_team_Di += df[df["team"] == team_name]["h_Di"].values[0]
                    total_opponents_Oi += df[df["team"] == opponent]["a_Oi"].values[0]
                    total_opponents_Di += df[df["team"] == opponent]["a_Di"].values[0]
                    expected_gf += round(
                        df[df["team"] == team_name]["h_Oi"].values[0]
                        * df[df["team"] == opponent]["a_Di"].values[0],
                        2,
                    )
                    expected_ga += round(
                        df[df["team"] == team_name]["h_Di"].values[0]
                        * df[df["team"] == opponent]["a_Oi"].values[0],
                        2,
                    )
                else:
                    print(f"H: {opponent} vs A: {team_name}")
                    total_team_Oi += df[df["team"] == team_name]["a_Oi"].values[0]
                    total_team_Di += df[df["team"] == team_name]["a_Di"].values[0]
                    total_opponents_Oi += df[df["team"] == opponent]["h_Oi"].values[0]
                    total_opponents_Di += df[df["team"] == opponent]["h_Di"].values[0]
                    expected_gf += round(
                        df[df["team"] == team_name]["a_Oi"].values[0]
                        * df[df["team"] == opponent]["h_Di"].values[0],
                        2,
                    )
                    expected_ga += round(
                        df[df["team"] == team_name]["a_Di"].values[0]
                        * df[df["team"] == opponent]["h_Oi"].values[0],
                        2,
                    )
            else:
                print("Without side adjustment:")
                (
                    print(f"H: {team_name} vs A: {opponent}")
                    if side == "Home"
                    else print(f"H: {opponent} vs A: {team_name}")
                )
                total_team_Oi += df[df["team"] == team_name]["Oi"].values[0]
                total_team_Di += df[df["team"] == team_name]["Di"].values[0]
                total_opponents_Oi += df[df["team"] == opponent]["Oi"].values[0]
                total_opponents_Di += df[df["team"] == opponent]["Di"].values[0]
                expected_gf += round(
                    df[df["team"] == team_name]["Oi"].values[0]
                    * df[df["team"] == opponent]["Di"].values[0],
                    2,
                )
                expected_ga += round(
                    df[df["team"] == team_name]["Di"].values[0]
                    * df[df["team"] == opponent]["Oi"].values[0],
                    2,
                )
        next_n_gameweek.append(
            {
                "team": team_name,
                "team_Oi": round(total_team_Oi, 2),
                "team_Di": round(total_team_Di, 2),
                "opponents_Oi": round(total_opponents_Oi, 2),
                "opponents_Di": round(total_opponents_Di, 2),
                "expected_gf": round(expected_gf, 2),
                "expected_ga": round(expected_ga, 2),
                "opponents": ", ".join(nextn_gws),
            }
        )
        print(nextn_gws)
        print(f"Projected next {n} gameweeks for {team_name}.")
        if team_name == "Wolves":
            print(f"Finished projecting next {n} gameweeks for all teams.")
        else:
            print("*" * 90)
        print("*" * 90)
    next_n_gameweek_df = pd.DataFrame(next_n_gameweek)
    next_n_gameweek_df.sort_values(by=["expected_gf"], ascending=False, inplace=True)
    file_path = TEAMS_PROJECTION_DIR / f"teams_next{n}gameweeks_{type}.csv"
    next_n_gameweek_df.to_csv(file_path, index=False)
    print(next_n_gameweek_df)
    print(
        f"Team projection of next {n} gameweeks using data of {type} saved to {file_path}"
    )


# Next week opponents

# last season strengths, only for before first gameweek
# get_next_gameweek(last_season_strengths, "lastseason")


# current season strengths
# change the last argument to true if want to adjust for home/away
get_next_gameweek(current_season_strengths, "currentseason", False)

# last 5 gameweeks strengths
get_next_gameweek(last5games_strengths, "last5games", False)

# augmented strengths
# get_next_gameweek(augmented_strengths, "augmented")

# Next 5 weeks opponents

# last season strengths, only for before first gameweek
# get_next_n_gameweek(last_season_strengths, "lastseason")

# current season strengths
get_next_n_gameweek(current_season_strengths, "currentseason", False)

# last 5 gameweeks strengths
get_next_n_gameweek(last5games_strengths, "last5games", False)

# augmented strengths
# get_next_5_gameweek(augmented_strengths, "augmented")
