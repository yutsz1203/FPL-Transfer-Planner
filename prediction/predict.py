import ast
import json
import os
import sys
import time

import numpy as np
import pandas as pd
import soccerdata as sd
import statsmodels
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy.stats import poisson


sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from const import TEAMS_DATA_DIR, TEAMS_RESULTS_DIR, leagues, season  # noqa: E402
from utils import get_gameweek

import os
import sys
import numpy as np
import pandas as pd
import soccerdata as sd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from const import TEAMS_DATA_DIR, TEAMS_RESULTS_DIR, season, leagues, teams


def create_model_data(df):
    home_df = pd.DataFrame(
        {
            "date": df["date"].dt.tz_localize(None),
            "team": df["home_team"],
            "opponent": df["away_team"],
            "goals": df["home_score"],
            "home": 1,
        }
    )

    away_df = pd.DataFrame(
        {
            "date": df["date"].dt.tz_localize(None),
            "team": df["away_team"],
            "opponent": df["home_team"],
            "goals": df["away_score"],
            "home": 0,
        }
    )

    return pd.concat([home_df, away_df])


def fit_model(df, T, lam=0.01):
    model_df = df.copy()
    model_df["days_ago"] = (T - model_df["date"]).dt.days
    model_df["weight"] = np.exp(-lam * model_df["days_ago"])

    model = smf.glm(
        formula="goals ~ home + team + opponent",
        data=model_df,
        family=sm.families.Poisson(),
        freq_weights=model_df["weight"],
    ).fit()

    return model


def _predict(
    model: statsmodels.genmod.generalized_linear_model.GLMResultsWrapper,
    team: str,
    opponent: str,
) -> tuple[str, str]:
    home_mean = model.predict(
        pd.DataFrame(
            data={"team": team, "opponent": opponent, "home": 1},
            index=[1],
        )
    ).values[0]

    away_mean = model.predict(
        pd.DataFrame(
            data={"team": opponent, "opponent": team, "home": 0},
            index=[1],
        )
    ).values[0]

    return home_mean, away_mean


def process_predict(proba: list, home: str, away: str) -> tuple[dict, dict]:

    long_info, short_info = {}, {}

    score_matrix = np.outer(proba[0], proba[1])
    np.round(score_matrix)

    home_prob = np.round(np.sum(np.tril(score_matrix, -1)), 4)
    draw_prob = np.round(np.trace(score_matrix), 4)
    away_prob = np.round(np.sum(np.triu(score_matrix, 1)), 4)

    outcomes = np.array([home_prob, draw_prob, away_prob])
    labels = np.array([home, "Draw", away])
    prediction = labels[np.argmax(outcomes)]

    long_info["Predicted Outcome"] = prediction

    print(f"{prediction} ({np.max(outcomes)})")
    short_info["Outcome"] = f"{prediction} ({np.max(outcomes)})"

    flat_idx = np.argmax(score_matrix)
    row, col = np.unravel_index(flat_idx, score_matrix.shape)

    long_info["Home Probability"] = home_prob
    long_info["Away Probability"] = away_prob
    long_info["Draw Probability"] = draw_prob
    long_info["Most likely score"] = f"{row}-{col}"
    long_info["Most likely score probability"] = float(
        np.round(score_matrix[row, col], 4)
    )

    rows, cols = np.indices(score_matrix.shape)
    total_goals_grid = rows + cols

    thresholds = [2.5, 3.5]

    for t in thresholds:
        over_prob = score_matrix[total_goals_grid > t].sum()
        under_prob = 1 - over_prob

        long_info[f"Over {t}"] = float(np.round(over_prob, 4))
        long_info[f"Under {t}"] = float(np.round(under_prob, 4))

        if over_prob > under_prob:
            short_info[t] = f"Over ({over_prob:.4f})"
            print(f"Over {t} ({over_prob:.4f})")
        else:
            short_info[t] = f"Under ({under_prob:.4f})"
            print(f"Under {t} ({under_prob:.4f})")

    print("=" * 50)

    return long_info, short_info


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
    # t1 = time.perf_counter()
    # predict()
    # # calc_accuracy()
    # t2 = time.perf_counter()

    # print(f"Time elapsed: {t2 - t1:.2f}")
    gameweeks = get_gameweek()
    for league in leagues:
        league_code, league_name = league.split("-")

        ss = sd.Sofascore(leagues=league, seasons=season, proxy="tor")
        hist = ss.read_schedule(force_cache=True)
        gw = gameweeks[league]
        T = hist.loc[hist["week"] == int(gw), "date"].values[0]
        hist.dropna(inplace=True)
        hist.reset_index(drop=True, inplace=True)
        cols = ["date", "home_team", "away_team", "home_score", "away_score"]
        league_df = create_model_data(hist[cols].copy())
        model = fit_model(league_df, T)

        fixtures_df = pd.read_csv(TEAMS_DATA_DIR / f"{league_code}_fixtures.csv")
        fixtures_df.set_index("team", inplace=True)

        long, short = {}, {}

        for team in teams[league_name]:
            curr_fixtures = ast.literal_eval(fixtures_df.at[team, gw])
            for curr_fixture in curr_fixtures:
                opponent, side = curr_fixture.split("-")
                if side == "A":
                    continue

                home_mean, away_mean = _predict(model, team, opponent)

                max_goals = 6
                proba = [
                    [poisson.pmf(i, team_mean) for i in range(0, max_goals)]
                    for team_mean in [home_mean, away_mean]
                ]

                print(
                    f"Prediction for the game between {team} ({home_mean:.2f}) and {opponent} ({away_mean:.2f}))"
                )

                long_info, short_info = process_predict(proba, team, opponent)

                long[f"{team}-{opponent}"] = long_info
                short[f"{team}-{opponent}"] = short_info

        with open(
            f"prediction/{league_code}/{league_code}_gw{gw}_long.json", "w"
        ) as file:
            json.dump(long, file, indent=4)

        with open(
            f"prediction/{league_code}/{league_code}_gw{gw}_short.json", "w"
        ) as file:
            json.dump(short, file, indent=4)
