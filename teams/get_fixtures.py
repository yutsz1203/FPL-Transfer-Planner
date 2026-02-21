# May need to fetch again whenever there are bgw or dgw
import json
import os
import sys

import pandas as pd
import requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from const import (  # noqa: E402
    TEAMS_DATA_DIR,
)

if __name__ == "__main__":
    official_api = "https://fantasy.premierleague.com/api/fixtures"
    flat_data = []
    with open("data/team_mapping.json", "r", encoding="utf-8") as f:
        team_map = json.load(f)

    try:
        print("Fetching fixtures from official api...")
        response = requests.get(official_api)
        data = response.json()

        for match in data:
            if match["event"]:

                home_team = team_map[str(match["team_h"])]
                away_team = team_map[str(match["team_a"])]
                flat_data.append(
                    {
                        "team": home_team,
                        "opponent": f"{away_team}-H",
                        "gw": match["event"],
                    }
                )
                # Away perspective
                flat_data.append(
                    {
                        "team": away_team,
                        "opponent": f"{home_team}-A",
                        "gw": match["event"],
                    }
                )

        df = pd.DataFrame(flat_data)

        fixture_df = df.pivot_table(
            index="team", columns="gw", values="opponent", aggfunc=list
        ).reset_index()

        file_path = TEAMS_DATA_DIR / "fixtures.csv"
        fixture_df.to_csv(file_path, index=False)

        print(f"Exported fixture.csv at {file_path}")

    except requests.exceptions.RequestException as e:
        print(e)
