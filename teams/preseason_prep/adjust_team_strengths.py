import requests
import pandas as pd

base_url = "https://fbrapi.com/"
team_season_stats = "team-season-stats"
generate_api_key = "generate_api_key"

api = requests.post(base_url + generate_api_key)
api_key = api.json()['api_key']
print("API Key:", api_key)
header = {"X-API-Key": api_key}

prem_team_df = pd.read_csv("data/2526-prem-teams-pastseason.csv")
prem_team_df = prem_team_df[~prem_team_df["team"].isin(["Burnley", "Leeds United"])]

response = requests.get(base_url + team_season_stats, params={"league_id": 9, "season_id": "2022-2023"}, headers=header)
season_teams_data = response.json()["data"]

leeds = []

for team in season_teams_data:
    team_name = team["meta_data"]["team_name"]
    print(team_name)
    leeds.append({
        "team": team_name,
        "goals_scored": team["stats"]["stats"]["ttl_gls"],
        "xg": team["stats"]["stats"]["ttl_xg"],
        "goals_conceded": team["stats"]["keepers"]["ttl_gls_ag"],
        "post_shot_xg": team["stats"]["keepersadv"]["ttl_psxg"],
        "saves": team["stats"]["keepers"]["ttl_saves"]
    })

leeds_df = pd.DataFrame(leeds)
lod = leeds_df["goals_scored"].sum() / (38 * 20)
leeds_df["Oi"] = leeds_df["goals_scored"] / 38 / lod
leeds_df["Oi"] = leeds_df["Oi"].round(2)
leeds_df["Di"] = leeds_df["goals_conceded"] / 38 / lod
leeds_df["Di"] = leeds_df["Di"].round(2)
leeds_df = leeds_df[leeds_df["team"] == "Leeds United"]

prem_team_df = pd.concat([prem_team_df, leeds_df], ignore_index=True)

response = requests.get(base_url + team_season_stats, params={"league_id": 9, "season_id": "2023-2024"}, headers=header)
season_teams_data = response.json()["data"]

burnley = []

for team in season_teams_data:
    team_name = team["meta_data"]["team_name"]
    print(team_name)
    burnley.append({
        "team": team_name,
        "goals_scored": team["stats"]["stats"]["ttl_gls"],
        "xg": team["stats"]["stats"]["ttl_xg"],
        "goals_conceded": team["stats"]["keepers"]["ttl_gls_ag"],
        "post_shot_xg": team["stats"]["keepersadv"]["ttl_psxg"],
        "saves": team["stats"]["keepers"]["ttl_saves"]
    })

burnley_df = pd.DataFrame(burnley)
lod = burnley_df["goals_scored"].sum() / (38 * 20)
burnley_df["Oi"] = burnley_df["goals_scored"] / 38 / lod
burnley_df["Oi"] = burnley_df["Oi"].round(2)
burnley_df["Di"] = burnley_df["goals_conceded"] / 38 / lod
burnley_df["Di"] = burnley_df["Di"].round(2)
burnley_df = burnley_df[burnley_df["team"] == "Burnley"]

prem_team_df = pd.concat([prem_team_df, burnley_df], ignore_index=True)

# Use .loc for proper assignment
prem_team_df.loc[prem_team_df["team"] == "Sunderland", "Oi"] = (prem_team_df[prem_team_df["team"] == "Burnley"]["Oi"].values[0] + prem_team_df[prem_team_df["team"] == "Leeds United"]["Oi"].values[0]) / 2
prem_team_df.loc[prem_team_df["team"] == "Sunderland", "Di"] = (prem_team_df[prem_team_df["team"] == "Burnley"]["Di"].values[0] + prem_team_df[prem_team_df["team"] == "Leeds United"]["Di"].values[0]) / 2

print(prem_team_df)
prem_team_df.to_csv("data/2526-prem-teams-pastseason.csv", index=False)
