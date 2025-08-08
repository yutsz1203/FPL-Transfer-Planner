import requests
import pandas as pd

base_url = "https://fbrapi.com/"
team_season_stats = "team-season-stats"
generate_api_key = "generate_api_key"

api = requests.post(base_url + generate_api_key)
api_key = api.json()['api_key']
print("API Key:", api_key)
header = {"X-API-Key": api_key}

# 2024-2025 season team stats
response = requests.get(base_url + team_season_stats, params={"league_id": 9, "season_id": "2024-2025"}, headers=header)
last_season_teams_data = response.json()["data"]


prem_teams = []

for team in last_season_teams_data:
    team_name = team["meta_data"]["team_name"]
    print(team_name)
    prem_teams.append({
        "team": team_name,
        "goals_scored": team["stats"]["stats"]["ttl_gls"],
        "xg": team["stats"]["stats"]["ttl_xg"],
        "goals_conceded": team["stats"]["keepers"]["ttl_gls_ag"],
        "post_shot_xg": team["stats"]["keepersadv"]["ttl_psxg"],
        "saves": team["stats"]["keepers"]["ttl_saves"]
    })
    print(f"{team_name}: {team['stats']['stats']['ttl_gls']} goals, {team['stats']['stats']['ttl_xg']} xG, {team['stats']['keepers']['ttl_gls_ag']} goals conceded, {team['stats']['keepersadv']['ttl_psxg']} post-shot xG, {team['stats']['keepers']['ttl_saves']} saves"
    )

last_season_prem_teams_df = pd.DataFrame(prem_teams)
print(last_season_prem_teams_df)
last_season_prem_teams_df.to_csv("data/2425-prem-teams.csv", index=False)

response = requests.get(base_url + team_season_stats, params={"league_id": 10, "season_id": "2024-2025"}, headers=header)
last_season_championship_data = response.json()["data"]

championship_teams = []

for team in last_season_championship_data:
    team_name = team["meta_data"]["team_name"]
    print(team_name)
    championship_teams.append({
        "team": team_name,
        "goals_scored": team["stats"]["stats"]["ttl_gls"],
        "xg": team["stats"]["stats"]["ttl_xg"],
        "goals_conceded": team["stats"]["keepers"]["ttl_gls_ag"],
        "post_shot_xg": team["stats"]["keepersadv"]["ttl_psxg"],
        "saves": team["stats"]["keepers"]["ttl_saves"]
    })
    print(f"{team_name}: {team['stats']['stats']['ttl_gls']} goals, {team['stats']['stats']['ttl_xg']} xG, {team['stats']['keepers']['ttl_gls_ag']} goals conceded, {team['stats']['keepersadv']['ttl_psxg']} post-shot xG, {team['stats']['keepers']['ttl_saves']} saves"
    )

last_season_championship_teams_df = pd.DataFrame(championship_teams)
print(last_season_championship_teams_df)
last_season_championship_teams_df.to_csv("data/2425-championship-teams.csv", index=False)

