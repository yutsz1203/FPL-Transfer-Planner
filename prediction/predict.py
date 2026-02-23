import ast
import json
import os
import sys

import numpy as np
import pandas as pd
from scipy.stats import poisson

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from const import TEAMS_DATA_DIR, TEAMS_RESULTS_DIR  # noqa: E402

if __name__ == "__main__":
    gw = input("Enter coming gameweek number: ")
    fixtures_df = pd.read_csv(TEAMS_DATA_DIR / "fixtures.csv")
    team_strengths_season = pd.read_csv(
        TEAMS_RESULTS_DIR / "teams_currentseason.csv", index_col=0
    )
    team_strengths_last5 = pd.read_csv(
        TEAMS_RESULTS_DIR / "teams_last5games.csv", index_col=0
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
            team_strengths_last5["h_gf"].sum() / team_strengths_last5["h_games"].sum()
        ).round(2)
        a_lod = (
            team_strengths_last5["a_gf"].sum() / team_strengths_last5["a_games"].sum()
        ).round(2)

    gw_df = fixtures_df[["team", gw]].copy()

    gw_df[gw] = gw_df[gw].apply(ast.literal_eval)

    detailed = []
    res = []

    for team in gw_df["team"].values:
        fixtures = gw_df.loc[gw_df["team"] == team, gw].item()

        for fixture in fixtures:
            fixture_info = {}
            res_info = {}

            opponent_name, side = fixture.split("-")
            if side == "H":
                fixture_info["Home"] = team
                fixture_info["Away"] = opponent_name
                res_info["Home"] = team
                res_info["Away"] = opponent_name

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

                detailed.append(fixture_info)
                res.append(res_info)

                print("=" * 50)

    with open(f"prediction/gw{gw}_detailed.json", "w") as file:
        json.dump(detailed, file, indent=4)

    with open(f"prediction/gw{gw}_predict.json", "w") as file:
        json.dump(res, file, indent=4)
