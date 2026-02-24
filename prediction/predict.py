import ast
import json
import os
import sys
import time

import numpy as np
import pandas as pd
import soccerdata as sd
from scipy.stats import poisson

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from const import TEAMS_DATA_DIR, TEAMS_RESULTS_DIR, leagues, season  # noqa: E402
from utils import get_gameweek


def predict():
    gameweeks = get_gameweek()

    for league in leagues:
        league_code = league.split("-")[0]
        gw = gameweeks[league]

        fixtures_df = pd.read_csv(TEAMS_DATA_DIR / f"{league_code}_fixtures.csv")
        team_strengths_season = pd.read_csv(
            TEAMS_RESULTS_DIR / f"{league_code}_teams_currentseason.csv", index_col=0
        )
        team_strengths_last5 = pd.read_csv(
            TEAMS_RESULTS_DIR / f"{league_code}_teams_last5games.csv", index_col=0
        )

        # Use overall attacking / defending strength when less than half of games are played
        if int(gw) <= 19:
            lod = (
                team_strengths_season["gf"].sum() / team_strengths_season["games"].sum()
            ).round(2)
            h_lod = lod
            a_lod = lod
        else:
            h_lod = (
                team_strengths_last5["h_gf"].sum()
                / team_strengths_last5["h_games"].sum()
            ).round(2)
            a_lod = (
                team_strengths_last5["a_gf"].sum()
                / team_strengths_last5["a_games"].sum()
            ).round(2)
        gw_df = fixtures_df[["team", gw]].copy()

        gw_df[gw] = gw_df[gw].apply(ast.literal_eval)

        detailed, res = {}, {}

        for team in gw_df["team"].values:
            fixtures = gw_df.loc[gw_df["team"] == team, gw].item()

            for fixture in fixtures:
                # make it a list of dictionary of dictionary, e.g. [{"Man City":  {"Opponent": , "Outcome": , "2.5", "3.5"}}]
                fixture_info = {}
                res_info = {}

                opponent_name, side = fixture.split("-")
                if side == "H":
                    h_oi = team_strengths_last5.at[team, "h_Oi"]
                    h_di = team_strengths_last5.at[team, "h_Di"]
                    a_oi = team_strengths_last5.at[opponent_name, "a_Oi"]
                    a_di = team_strengths_last5.at[opponent_name, "a_Di"]

                    fixture_info["Home Strengths"] = f"{h_oi}, {h_di}"
                    fixture_info["Away Strengths"] = f"{a_oi}, {a_di}"
                    # expected goal for home team: h_oi * a_di * h_lod
                    # expected goal for away team: a_oi * h_di * a_lod
                    home_dist = np.array(
                        [poisson.pmf(i, h_oi * a_di * h_lod) for i in range(11)]
                    )
                    away_dist = np.array(
                        [poisson.pmf(i, a_oi * h_di * a_lod) for i in range(11)]
                    )

                    score_matrix = np.outer(home_dist, away_dist)
                    np.round(score_matrix)

                    home_prob = np.round(np.sum(np.tril(score_matrix, -1)), 4)
                    draw_prob = np.round(np.trace(score_matrix), 4)
                    away_prob = np.round(np.sum(np.triu(score_matrix, 1)), 4)

                    outcomes = np.array([home_prob, draw_prob, away_prob])
                    labels = np.array([team, "Draw", opponent_name])
                    prediction = labels[np.argmax(outcomes)]

                    fixture_info["Predicted Outcome"] = prediction

                    print(f"Prediction for the game between {team} and {opponent_name}")
                    print(f"{prediction} ({np.max(outcomes)})")
                    res_info["Outcome"] = f"{prediction} ({np.max(outcomes)})"

                    flat_idx = np.argmax(score_matrix)
                    row, col = np.unravel_index(flat_idx, score_matrix.shape)

                    fixture_info["Home Probability"] = home_prob
                    fixture_info["Away Probability"] = away_prob
                    fixture_info["Draw Probability"] = draw_prob
                    fixture_info["Most likely score"] = f"{row}-{col}"
                    fixture_info["Most likely score probability"] = float(
                        np.round(score_matrix[row, col], 4)
                    )

                    rows, cols = np.indices(score_matrix.shape)
                    total_goals_grid = rows + cols

                    thresholds = [2.5, 3.5]

                    for t in thresholds:
                        over_prob = score_matrix[total_goals_grid > t].sum()
                        under_prob = 1 - over_prob

                        fixture_info[f"Over {t}"] = float(np.round(over_prob, 4))
                        fixture_info[f"Under {t}"] = float(np.round(under_prob, 4))

                        if over_prob > under_prob:
                            res_info[t] = f"Over ({over_prob:.4f})"
                            print(f"Over {t} ({over_prob:.4f})")
                        else:
                            res_info[t] = f"Under ({under_prob:.4f})"
                            print(f"Under {t} ({under_prob:.4f})")

                    detailed[f"{team}-{opponent_name}"] = fixture_info
                    res[f"{team}-{opponent_name}"] = res_info

                    print("=" * 50)

        with open(
            f"prediction/{league_code}/{league_code}_gw{gw}_detailed.json", "w"
        ) as file:
            json.dump(detailed, file, indent=4)

        with open(
            f"prediction/{league_code}/{league_code}_gw{gw}_predict.json", "w"
        ) as file:
            json.dump(res, file, indent=4)


def calc_accuracy():
    sofascore = sd.Sofascore(leagues=leagues, seasons=season)
    results = sofascore.read_schedule(force_cache=True)
    gameweeks = get_gameweek()
    res = []

    for league in leagues:
        correct_outcome, correct_2_5, correct_3_5 = 0, 0, 0
        league_code, league_name = league.split("-")
        gw = int(gameweeks[league])

        result_df = results.query("league == @league and week == @gw").dropna()

        if result_df.empty:
            gw -= 1
            result_df = results.query("league == @league and week == @gw").dropna()

        with open(
            f"prediction/{league_code}/{league_code}_gw{gw}_detailed.json",
            "r",
            encoding="utf-8",
        ) as file:
            prediction = json.load(file)

        for match, match_info in prediction.items():
            match_result = result_df.loc[
                result_df.index.get_level_values("game").str.contains(match)
            ]
            if not match_result.empty:
                home_score = match_result["home_score"].values[0]
                away_score = match_result["away_score"].values[0]
                total_goals = home_score + away_score

                if home_score > away_score:
                    outcome = match_result["home_team"].values[0]
                elif away_score > home_score:
                    outcome = match_result["away_team"].values[0]
                else:
                    outcome = "Draw"

                if outcome == match_info["Predicted Outcome"]:
                    correct_outcome += 1

                if (
                    match_info["Over 2.5"] > match_info["Under 2.5"]
                    and total_goals > 2.5
                ) or (
                    match_info["Over 2.5"] < match_info["Under 2.5"]
                    and total_goals < 2.5
                ):
                    correct_2_5 += 1

                if (
                    match_info["Over 3.5"] > match_info["Under 3.5"]
                    and total_goals > 3.5
                ) or (
                    match_info["Over 3.5"] < match_info["Under 3.5"]
                    and total_goals < 3.5
                ):
                    correct_3_5 += 1

        total_matches = len(result_df)
        correct_outcome_rate = round(((correct_outcome / total_matches) * 100), 2)
        correct_2_5_rate = round(((correct_2_5 / total_matches) * 100), 2)
        correct_3_5_rate = round(((correct_3_5 / total_matches) * 100), 2)

        print(f"Results for {league_name}")
        print(f"Total matches: {total_matches}")
        print(f"Outcome: {correct_outcome_rate}")
        print(f"2.5: {correct_2_5_rate}")
        print(f"3.5: {correct_3_5_rate}")
        print("\n")

        res.append(
            {
                "league": league,
                "total_matches": total_matches,
                "correct_outcome": correct_outcome_rate,
                "correct_2_5": correct_2_5_rate,
                "correct_3_5": correct_3_5_rate,
            }
        )
    df = pd.DataFrame(res)
    df.sort_values(
        ["correct_2_5", "correct_3_5", "correct_outcome"], ascending=False, inplace=True
    )
    df.to_csv("prediction/accuracy.csv", index=False)


if __name__ == "__main__":
    t1 = time.perf_counter()
    # predict()
    calc_accuracy()
    t2 = time.perf_counter()

    print(f"Time elapsed: {t2 - t1:.2f}")
