# url: https://fantasy.premierleague.com/api/element-summary/{player-id}/
# or try this: https://fantasy.premierleague.com/api/event/1/live/
import os
import sys

import pandas as pd
import requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from const import (  # noqa : E402
    PLAYERS_DATA_DIR,
    PLAYERS_RESULTS_DIR,
    official_base_url,
    official_to_fbref_team_map,
)


def stats_calculation(matches):
    (
        points,
        games,
        goals,
        assists,
        xG,
        xA,
        xGI,
        gc,
        xGc,
        clean_sheets,
        defensive_contribution,
        saves,
        bonus,
    ) = (
        0,
        0,
        0,
        0,
        0.0,
        0.0,
        0.0,
        0,
        0.0,
        0,
        0,
        0,
        0,
    )
    (
        h_games,
        h_goals,
        h_assists,
        hxG,
        hxA,
        hxGI,
        h_gc,
        hxGc,
    ) = (
        0,
        0,
        0,
        0.0,
        0.0,
        0.0,
        0,
        0.0,
    )
    a_games, a_goals, a_assists, axG, axA, axGI, a_gc, axGc = (
        0,
        0,
        0,
        0.0,
        0.0,
        0.0,
        0,
        0.0,
    )

    for match in matches:
        if match["minutes"] == 0:
            continue
        side = "Home" if match["was_home"] else "Away"
        points += match["total_points"]
        games += 1
        goals += match["goals_scored"]
        assists += match["assists"]
        xG += float(match["expected_goals"])
        xA += float(match["expected_assists"])
        xGI += float(match["expected_goal_involvements"])
        gc += match["goals_conceded"]
        xGc += float(match["expected_goals_conceded"])
        clean_sheets += match["clean_sheets"]
        defensive_contribution += match["defensive_contribution"]
        saves += match["saves"]
        bonus += match["bonus"]

        if side == "Home":
            h_games += 1
            h_goals += match["goals_scored"]
            h_assists += match["assists"]
            hxG += float(match["expected_goals"])
            hxA += float(match["expected_assists"])
            hxGI += float(match["expected_goal_involvements"])
            h_gc += match["goals_conceded"]
            hxGc += float(match["expected_goals_conceded"])
        else:
            a_games += 1
            a_goals += match["goals_scored"]
            a_assists += match["assists"]
            axG += float(match["expected_goals"])
            axA += float(match["expected_assists"])
            axGI += float(match["expected_goal_involvements"])
            a_gc += match["goals_conceded"]
            axGc += float(match["expected_goals_conceded"])

    return (
        points,
        games,
        goals,
        assists,
        xG,
        xA,
        xGI,
        gc,
        xGc,
        clean_sheets,
        defensive_contribution,
        saves,
        bonus,
        h_games,
        h_goals,
        h_assists,
        hxG,
        hxA,
        hxGI,
        h_gc,
        hxGc,
        a_games,
        a_goals,
        a_assists,
        axG,
        axA,
        axGI,
        a_gc,
        axGc,
    )


def build_dict(
    element_id,
    player,
    pos,
    team,
    cost,
    points,
    games,
    goals,
    assists,
    xG,
    xA,
    xGI,
    gc,
    xGc,
    clean_sheets,
    defensive_contribution,
    saves,
    bonus,
    h_games,
    h_goals,
    h_assists,
    hxG,
    hxA,
    hxGI,
    h_gc,
    hxGc,
    a_games,
    a_goals,
    a_assists,
    axG,
    axA,
    axGI,
    a_gc,
    axGc,
):
    return {
        "Player ID": element_id,
        "Name": player,
        "Pos": pos,
        "Team": official_to_fbref_team_map[team],
        "Cost": cost,
        "Total Points": points,
        "Bonus": bonus,
        "Points/$": round(points / cost, 2),
        "Games": games,
        "Goals": goals,
        "Assists": assists,
        "xG": round(xG, 2),
        "xA": round(xA, 2),
        "xGI": round(xGI, 2),
        "gc": gc,
        "xGc": round(xGc, 2),
        "clean_sheets": clean_sheets,
        "def_con": defensive_contribution,
        "Saves": saves,
        "h_Games": h_games,
        "h_Goals": h_goals,
        "h_Assists": h_assists,
        "h_xG": round(hxG, 2),
        "h_xA": round(hxA, 2),
        "h_xGI": round(hxGI, 2),
        "h_Gc": h_gc,
        "h_xGc": round(hxGc, 2),
        "a_Games": a_games,
        "a_Goals": a_goals,
        "a_Assists": a_assists,
        "a_xG": round(axG, 2),
        "a_xA": round(axA, 2),
        "a_xGI": round(axGI, 2),
        "a_Gc": a_gc,
        "a_xGc": round(axGc, 2),
    }


if __name__ == "__main__":
    gw = int(input("Enter current gameweek number: "))
    n = int(input("Enter number of last n games to include in calculation: "))

    player_basic_df = pd.read_csv(PLAYERS_DATA_DIR / "players.csv")
    player_ids = player_basic_df.index.tolist()
    df = []
    lastngamesdf = []
    for player_id in player_ids:
        player = player_basic_df.loc[player_id, "Name"]
        print(f"Fetching data for {player}...")
        element_id = player_id + 1
        response = requests.get(f"{official_base_url}/element-summary/{element_id}/")
        if "history" not in response.json():
            print(f"{player} has not played in the current season, skipping...")
            continue
        matches = response.json()["history"]
        (
            points,
            games,
            goals,
            assists,
            xG,
            xA,
            xGI,
            gc,
            xGc,
            clean_sheets,
            defensive_contribution,
            saves,
            bonus,
            h_games,
            h_goals,
            h_assists,
            hxG,
            hxA,
            hxGI,
            h_gc,
            hxGc,
            a_games,
            a_goals,
            a_assists,
            axG,
            axA,
            axGI,
            a_gc,
            axGc,
        ) = stats_calculation(matches)
        (
            lastn_points,
            lastn_games,
            lastn_goals,
            lastn_assists,
            lastn_xG,
            lastn_xA,
            lastn_xGI,
            lastn_gc,
            lastn_xGc,
            lastn_clean_sheets,
            lastn_defensive_contribution,
            lastn_saves,
            lastn_bonus,
            lastn_h_goals,
            lastn_h_assists,
            lastn_h_games,
            lastn_h_xG,
            lastn_h_xA,
            lastn_h_xGI,
            lastn_h_gc,
            lastn_h_xGc,
            lastn_a_games,
            lastn_a_goals,
            lastn_a_assists,
            lastn_a_xG,
            lastn_a_xA,
            lastn_a_xGI,
            lastn_a_gc,
            lastn_a_xGc,
        ) = stats_calculation(matches[-n:])

        df.append(
            build_dict(
                element_id,
                player,
                player_basic_df.loc[player_id, "Pos"],
                player_basic_df.loc[player_id, "Team"],
                player_basic_df.loc[player_id, "Cost"],
                points,
                games,
                goals,
                assists,
                xG,
                xA,
                xGI,
                gc,
                xGc,
                clean_sheets,
                defensive_contribution,
                saves,
                bonus,
                h_games,
                h_goals,
                h_assists,
                hxG,
                hxA,
                hxGI,
                h_gc,
                hxGc,
                a_games,
                a_goals,
                a_assists,
                axG,
                axA,
                axGI,
                a_gc,
                axGc,
            )
        )
        lastngamesdf.append(
            build_dict(
                element_id,
                player,
                player_basic_df.loc[player_id, "Pos"],
                player_basic_df.loc[player_id, "Team"],
                player_basic_df.loc[player_id, "Cost"],
                lastn_points,
                lastn_games,
                lastn_goals,
                lastn_assists,
                lastn_xG,
                lastn_xA,
                lastn_xGI,
                lastn_gc,
                lastn_xGc,
                lastn_clean_sheets,
                lastn_defensive_contribution,
                lastn_saves,
                lastn_bonus,
                lastn_h_games,
                lastn_h_goals,
                lastn_h_assists,
                lastn_h_xG,
                lastn_h_xA,
                lastn_h_xGI,
                lastn_h_gc,
                lastn_h_xGc,
                lastn_a_games,
                lastn_a_goals,
                lastn_a_assists,
                lastn_a_xG,
                lastn_a_xA,
                lastn_a_xGI,
                lastn_a_gc,
                lastn_a_xGc,
            )
        )

    df = pd.DataFrame(df)
    df.sort_values(by=["xGI", "Points/$"], ascending=False, inplace=True)
    file_path = PLAYERS_RESULTS_DIR / "players_currentseason.csv"
    df.to_csv(file_path, index=False)
    print(f"Player stats of current season saved to {file_path}")

    lastngamesdf = pd.DataFrame(lastngamesdf)
    lastngamesdf.sort_values(by=["xGI", "Points/$"], ascending=False, inplace=True)
    file_path = PLAYERS_RESULTS_DIR / f"players_last{n}games.csv"
    lastngamesdf.to_csv(file_path, index=False)
    print(f"Player stats of last {n} games saved to {file_path}")

    print(df.head())
    print(lastngamesdf.head())
