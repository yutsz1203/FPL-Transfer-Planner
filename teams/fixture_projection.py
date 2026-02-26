import ast
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from const import (  # noqa: E402
    TEAMS_DATA_DIR,
    TEAMS_PROJECTION_DIR,
    TEAMS_RESULTS_DIR,
    teams,
)

fixtures = pd.read_csv(TEAMS_DATA_DIR / "ENG_fixtures.csv")
fixtures.set_index("team", inplace=True)
# Only for first gameweek
# last_season_strengths = pd.read_csv("teams/data/2526-prem-teams-lastseason.csv")

current_season_strengths = pd.read_csv(
    TEAMS_RESULTS_DIR / "ENG_teams_currentseason.csv"
)

last5games_strengths = pd.read_csv(TEAMS_RESULTS_DIR / "ENG_teams_last5games.csv")

all_teams = teams["Premier League"]


def get_next_gameweek(df, type, gw):
    side_adjust = True if int(gw) > 15 else False
    next_gameweek = []
    print(f"Projecting gameweek{gw} for all teams using {type} stats...")
    print("*" * 90)
    for team in all_teams:
        curr_fixtures = ast.literal_eval(fixtures.at[team, gw])
        for curr_fixture in curr_fixtures:
            opponent, side = curr_fixture.split("-")

            if side_adjust:
                if side == "H":
                    print(f"H: {team} vs A: {opponent}")
                    team_Oi = df[df["team"] == team]["h_Oi"].values[0]
                    team_Di = df[df["team"] == team]["h_Di"].values[0]
                    opponent_Oi = df[df["team"] == opponent]["a_Oi"].values[0]
                    opponent_Di = df[df["team"] == opponent]["a_Di"].values[0]
                else:
                    print(f"H: {opponent} vs A: {team}")
                    team_Oi = df[df["team"] == team]["a_Oi"].values[0]
                    team_Di = df[df["team"] == team]["a_Di"].values[0]
                    opponent_Oi = df[df["team"] == opponent]["h_Oi"].values[0]
                    opponent_Di = df[df["team"] == opponent]["h_Di"].values[0]
            else:
                (
                    print(f"H: {team} vs A: {opponent}")
                    if side == "Home"
                    else print(f"H: {opponent} vs A: {team}")
                )
                team_Oi = df[df["team"] == team]["Oi"].values[0]
                team_Di = df[df["team"] == team]["Di"].values[0]
                opponent_Oi = df[df["team"] == opponent]["Oi"].values[0]
                opponent_Di = df[df["team"] == opponent]["Di"].values[0]
            next_gameweek.append(
                {
                    "team": team,
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
        if team == all_teams[-1]:
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


def get_next_n_gameweek(df, type, gw, n=5):
    side_adjust = True if int(gw) > 15 else False
    next_n_gameweek = []
    print(
        f"Projection gameweek{gw}-gw{int(gw)+n-1} for all teams using {type} stats..."
    )
    print("*" * 90)
    nextn_gws = range(int(gw), int(gw) + n)
    for team in all_teams:
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
            val = fixtures.at[team, str(gw)]
            if pd.isna(val):
                print(f"Blank GW for {team} on gw {gw}")
                continue
            curr_fixtures = ast.literal_eval(val)
            for curr_fixture in curr_fixtures:
                opponent, side = curr_fixture.split("-")
                opponents.append(f"{opponent}-{side}")
                if side_adjust:
                    if side == "H":
                        print(f"H: {team} vs A: {opponent}")
                        total_team_Oi += df[df["team"] == team]["h_Oi"].values[0]
                        total_team_Di += df[df["team"] == team]["h_Di"].values[0]
                        total_opponents_Oi += df[df["team"] == opponent]["a_Oi"].values[
                            0
                        ]
                        total_opponents_Di += df[df["team"] == opponent]["a_Di"].values[
                            0
                        ]
                        expected_gf += round(
                            df[df["team"] == team]["h_Oi"].values[0]
                            * df[df["team"] == opponent]["a_Di"].values[0],
                            2,
                        )
                        expected_ga += round(
                            df[df["team"] == team]["h_Di"].values[0]
                            * df[df["team"] == opponent]["a_Oi"].values[0],
                            2,
                        )
                    else:
                        print(f"H: {opponent} vs A: {team}")
                        total_team_Oi += df[df["team"] == team]["a_Oi"].values[0]
                        total_team_Di += df[df["team"] == team]["a_Di"].values[0]
                        total_opponents_Oi += df[df["team"] == opponent]["h_Oi"].values[
                            0
                        ]
                        total_opponents_Di += df[df["team"] == opponent]["h_Di"].values[
                            0
                        ]
                        expected_gf += round(
                            df[df["team"] == team]["a_Oi"].values[0]
                            * df[df["team"] == opponent]["h_Di"].values[0],
                            2,
                        )
                        expected_ga += round(
                            df[df["team"] == team]["a_Di"].values[0]
                            * df[df["team"] == opponent]["h_Oi"].values[0],
                            2,
                        )
                else:
                    print("Without side adjustment:")
                    (
                        print(f"H: {team} vs A: {opponent}")
                        if side == "H"
                        else print(f"H: {opponent} vs A: {team}")
                    )
                    total_team_Oi += df[df["team"] == team]["Oi"].values[0]
                    total_team_Di += df[df["team"] == team]["Di"].values[0]
                    total_opponents_Oi += df[df["team"] == opponent]["Oi"].values[0]
                    total_opponents_Di += df[df["team"] == opponent]["Di"].values[0]
                    expected_gf += round(
                        df[df["team"] == team]["Oi"].values[0]
                        * df[df["team"] == opponent]["Di"].values[0],
                        2,
                    )
                    expected_ga += round(
                        df[df["team"] == team]["Di"].values[0]
                        * df[df["team"] == opponent]["Oi"].values[0],
                        2,
                    )
        next_n_gameweek.append(
            {
                "team": team,
                "team_Oi": round(total_team_Oi, 2),
                "team_Di": round(total_team_Di, 2),
                "opponents_Oi": round(total_opponents_Oi, 2),
                "opponents_Di": round(total_opponents_Di, 2),
                "expected_gf": round(expected_gf, 2),
                "expected_ga": round(expected_ga, 2),
                "opponents": ", ".join(opponents),
            }
        )
        print(opponents)
        print(f"Projected next {n} gameweeks for {team}.")
        if team == "Wolves":
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


if __name__ == "__main__":
    gw = input("Enter the coming gameweek number: ")

    get_next_gameweek(current_season_strengths, "currentseason", gw)
    get_next_gameweek(last5games_strengths, "last5games", gw)

    get_next_n_gameweek(current_season_strengths, "currentseason", gw)
    get_next_n_gameweek(last5games_strengths, "last5games", gw)
