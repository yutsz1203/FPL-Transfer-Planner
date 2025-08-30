# Project next game week and next 5 gameweeks using current season stats and last 5 games stats
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from const import PLAYERS_RESULT_DIR, PLAYERS_PROJECTION_DIR, TEAMS_DATA_DIR  # noqa: E402


def get_next_gameweek(fixtures, player_df, team_df, type, gw, side_adjustment=True):
    gameweek = f"GW{gw}"
    print(f"Projecting {gameweek} for all players using {type} stats...")
    print("*" * 90)

    player_df["xGI/Game"] = player_df["xGI"] / player_df["Games"]
    player_df["xGc/Game"] = player_df["xGc"] / player_df["Games"]
    player_df["h_xGI/Game"] = player_df["h_xGI"] / player_df["h_Games"]
    player_df["h_xGc/Game"] = player_df["h_xGc"] / player_df["h_Games"]
    player_df["a_xGI/Game"] = player_df["a_xGI"] / player_df["a_Games"]
    player_df["a_xGc/Game"] = player_df["a_xGc"] / player_df["a_Games"]

    player_df = player_df[
        [
            "Player ID",
            "Name",
            "Pos",
            "Team",
            "Cost",
            "xGI/Game",
            "xGc/Game",
            "h_xGI/Game",
            "h_xGc/Game",
            "a_xGI/Game",
            "a_xGc/Game",
        ]
    ]
    players = player_df.to_dict(orient="records")

    for player in players:
        team_name = player["Team"]
        opponent = fixtures[fixtures["team"] == team_name][gameweek].values[0][:-3]
        side = fixtures[fixtures["team"] == team_name][gameweek].values[0][-2]

        if side_adjustment:
            if side == "H":
                xGI = player["h_xGI/Game"]
                xGc = player["h_xGc/Game"]
                team_Oi = team_df[team_df["team"] == team_name]["h_Oi"].values[0]
                team_Di = team_df[team_df["team"] == team_name]["h_Di"].values[0]
                opponent_Oi = team_df[team_df["team"] == opponent]["a_Oi"].values[0]
                opponent_Di = team_df[team_df["team"] == opponent]["a_Di"].values[0]
            else:
                xGI = player["a_xGI/Game"]
                xGc = player["a_xGc/Game"]
                team_Oi = team_df[team_df["team"] == team_name]["a_Oi"].values[0]
                team_Di = team_df[team_df["team"] == team_name]["a_Di"].values[0]
                opponent_Oi = team_df[team_df["team"] == opponent]["h_Oi"].values[0]
                opponent_Di = team_df[team_df["team"] == opponent]["h_Di"].values[0]
        else:
            xGI = player["xGI/Game"]
            xGc = player["xGc/Game"]
            team_Oi = team_df[team_df["team"] == team_name]["Oi"].values[0]
            team_Di = team_df[team_df["team"] == team_name]["Di"].values[0]
            opponent_Oi = team_df[team_df["team"] == opponent]["Oi"].values[0]
            opponent_Di = team_df[team_df["team"] == opponent]["Di"].values[0]

        player["opponent"] = opponent
        player["team_Oi"] = team_Oi
        player["team_Di"] = team_Di
        player["opponent_Oi"] = opponent_Oi
        player["opponent_Di"] = opponent_Di
        player["xGI"] = xGI
        player["projected GI"] = round(xGI * opponent_Di, 2)
        player["xGc"] = xGc
        player["projected Gc"] = round(xGc * opponent_Oi, 2)

    next_gameweek_df = pd.DataFrame(players)
    next_gameweek_df = next_gameweek_df.drop(
        columns=[
            "xGI/Game",
            "xGc/Game",
            "h_xGI/Game",
            "h_xGc/Game",
            "a_xGI/Game",
            "a_xGc/Game",
        ]
    )
    next_gameweek_df["projected net goals"] = round(
        next_gameweek_df["projected GI"] - next_gameweek_df["projected Gc"], 2
    )
    next_gameweek_df = next_gameweek_df.reindex(
        columns=[
            "Player ID",
            "Name",
            "Pos",
            "Team",
            "Cost",
            "opponent",
            "team_Oi",
            "opponent_Di",
            "xGI",
            "projected GI",
            "team_Di",
            "opponent_Oi",
            "xGc",
            "projected Gc",
            "projected net goals",
        ]
    )
    next_gameweek_df.sort_values(by=["projected GI"], ascending=False, inplace=True)
    file_path = PLAYERS_PROJECTION_DIR / f"players_next_gameweek_{type}.csv"
    next_gameweek_df.to_csv(file_path, index=False)
    print(next_gameweek_df.head())
    print(
        f"Player projection of next gameweek using data of {type} saved to {file_path}"
    )


def get_next_n_gameweek(
    fixtures, player_df, team_df, type, gw, side_adjustment=True, n=5
):
    print(f"Projection gw{gw}-gw{gw+(n-1)} for all teams using {type} stats...")
    print("*" * 90)

    player_df["xGI/Game"] = player_df["xGI"] / player_df["Games"]
    player_df["xGc/Game"] = player_df["xGc"] / player_df["Games"]
    player_df["h_xGI/Game"] = player_df["h_xGI"] / player_df["h_Games"]
    player_df["h_xGc/Game"] = player_df["h_xGc"] / player_df["h_Games"]
    player_df["a_xGI/Game"] = player_df["a_xGI"] / player_df["a_Games"]
    player_df["a_xGc/Game"] = player_df["a_xGc"] / player_df["a_Games"]

    player_df = player_df[
        [
            "Player ID",
            "Name",
            "Pos",
            "Team",
            "Cost",
            "xGI/Game",
            "xGc/Game",
            "h_xGI/Game",
            "h_xGc/Game",
            "a_xGI/Game",
            "a_xGc/Game",
        ]
    ]
    players = player_df.to_dict(orient="records")

    for player in players:
        team_name = player["Team"]
        team_fixtures = fixtures[fixtures["team"] == team_name]
        nextn_gws = [team_fixtures[f"GW{i}"].values[0] for i in range(gw, gw + n)]
        opponents = []
        (
            total_team_Oi,
            total_team_Di,
            total_opponents_Oi,
            total_opponents_Di,
            total_player_xGI,
            total_player_xGc,
            projected_GI,
            projected_Gc,
        ) = (0, 0, 0, 0, 0, 0, 0, 0)
        for oppo in nextn_gws:
            side = oppo[-2]
            opponent = oppo[:-3]
            opponents.append(f"({side}) {opponent}")
            if side_adjustment:
                if side == "H":
                    total_player_xGI += player["h_xGI/Game"]
                    total_player_xGc += player["h_xGc/Game"]
                    total_team_Oi += team_df[team_df["team"] == team_name][
                        "h_Oi"
                    ].values[0]
                    total_team_Di += team_df[team_df["team"] == team_name][
                        "h_Di"
                    ].values[0]
                    total_opponents_Oi += team_df[team_df["team"] == opponent][
                        "a_Oi"
                    ].values[0]
                    total_opponents_Di += team_df[team_df["team"] == opponent][
                        "a_Di"
                    ].values[0]
                    projected_GI += round(
                        player["h_xGI/Game"]
                        * team_df[team_df["team"] == opponent]["a_Di"].values[0],
                        2,
                    )
                    projected_Gc += round(
                        player["h_xGc/Game"]
                        * team_df[team_df["team"] == opponent]["a_Oi"].values[0],
                        2,
                    )
                else:
                    total_player_xGI += player["a_xGI/Game"]
                    total_player_xGc += player["a_xGc/Game"]
                    total_team_Oi += team_df[team_df["team"] == team_name][
                        "a_Oi"
                    ].values[0]
                    total_team_Di += team_df[team_df["team"] == team_name][
                        "a_Di"
                    ].values[0]
                    total_opponents_Oi += team_df[team_df["team"] == opponent][
                        "h_Oi"
                    ].values[0]
                    total_opponents_Di += team_df[team_df["team"] == opponent][
                        "h_Di"
                    ].values[0]
                    projected_GI += round(
                        player["a_xGI/Game"]
                        * team_df[team_df["team"] == opponent]["h_Di"].values[0],
                        2,
                    )
                    projected_Gc += round(
                        player["a_xGc/Game"]
                        * team_df[team_df["team"] == opponent]["h_Oi"].values[0],
                        2,
                    )
            else:
                print(f"{player["Name"]} will play against {opponent}.")
                total_player_xGI += player["xGI/Game"]
                total_player_xGc += player["xGc/Game"]
                total_team_Oi += team_df[team_df["team"] == team_name]["Oi"].values[0]
                total_team_Di += team_df[team_df["team"] == team_name]["Di"].values[0]
                total_opponents_Oi += team_df[team_df["team"] == opponent]["Oi"].values[
                    0
                ]
                total_opponents_Di += team_df[team_df["team"] == opponent]["Di"].values[
                    0
                ]
                projected_GI += round(
                    player["xGI/Game"]
                    * team_df[team_df["team"] == opponent]["Di"].values[0],
                    2,
                )
                projected_Gc += round(
                    player["xGc/Game"]
                    * team_df[team_df["team"] == opponent]["Oi"].values[0],
                    2,
                )

        player["opponents"] = ",".join(opponents)
        player["team_Oi"] = round(total_team_Oi, 2)
        player["team_Di"] = round(total_team_Di, 2)
        player["opponent_Oi"] = round(total_opponents_Oi, 2)
        player["opponent_Di"] = round(total_opponents_Di, 2)
        player["xGI"] = round(total_player_xGI, 2)
        player["projected_GI"] = round(projected_GI, 2)
        player["xGc"] = round(total_player_xGc, 2)
        player["projected_Gc"] = round(projected_Gc, 2)

    next_n_gameweek_df = pd.DataFrame(players)
    next_n_gameweek_df = next_n_gameweek_df.drop(
        columns=[
            "xGI/Game",
            "xGc/Game",
            "h_xGI/Game",
            "h_xGc/Game",
            "a_xGI/Game",
            "a_xGc/Game",
        ]
    )
    next_n_gameweek_df["projected_net_goals"] = round(
        next_n_gameweek_df["projected_GI"] - next_n_gameweek_df["projected_Gc"], 2
    )
    next_n_gameweek_df = next_n_gameweek_df.reindex(
        columns=[
            "Player ID",
            "Name",
            "Pos",
            "Team",
            "Cost",
            "team_Oi",
            "opponent_Di",
            "xGI",
            "projected_GI",
            "team_Di",
            "opponent_Oi",
            "xGc",
            "projected_Gc",
            "projected_net_goals",
            "opponents",
        ]
    )
    next_n_gameweek_df.sort_values(by=["projected_GI"], ascending=False, inplace=True)
    file_path = PLAYERS_PROJECTION_DIR / f"players_next{n}gameweeks_{type}.csv"
    next_n_gameweek_df.to_csv(file_path, index=False)
    print(next_n_gameweek_df.head())
    print(
        f"Player projection of next {n} gameweeks using data of {type} saved to {file_path}"
    )


if __name__ == "__main__":
    fixtures = pd.read_csv(TEAMS_DATA_DIR / "fixtures.csv")

    # Current season
    team_current_season = pd.read_csv(TEAMS_DATA_DIR / "teams_currentseason.csv")
    player_current_season = pd.read_csv(
        PLAYERS_RESULT_DIR / "players_currentseason.csv"
    )

    # Last n games
    n = int(
        input(
            "Please input n, number of previous games for calculation of player statistics: "
        )
    )
    player_lastngames = pd.read_csv(PLAYERS_RESULT_DIR / f"players_last{n}games.csv")

    # Augmented
    # augmented_strengths = pd.read_csv("teams/data/2526-prem-teams-augmented.csv")

    # Next week player projection
    gw = int(input("Enter the coming gameweek number: "))
    # current season strengths
    # change the last argument to true if want to adjust for home/away
    get_next_gameweek(
        fixtures, player_current_season, team_current_season, "currentseason", gw, False
    )

    # last 5 gameweeks strengths
    # get_next_gameweek(last5games_strengths, "last5games")

    # augmented strengths
    # get_next_gameweek(augmented_strengths, "augmented")

    # Next 5 weeks player projections

    # current season strengths
    get_next_n_gameweek(
        fixtures, player_current_season, team_current_season, "currentseason", gw, False
    )

    # last 5 gameweeks strengths
    # get_next_5_gameweek(last5games_strengths, "last5games")

    # augmented strengths
    # get_next_5_gameweek(augmented_strengths, "augmented")
