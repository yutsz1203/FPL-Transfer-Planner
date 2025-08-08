import requests

base_url = "https://fbrapi.com/"
generate_api_key = "generate_api_key"

api = requests.post(base_url + generate_api_key)
api_key = api.json()['api_key']
print("API Key:", api_key)
header = {"X-API-Key": api_key}

league_id = 9 # 9 for Premier League, 10 for Championship
season_id = "2024-2025"
team_id_map = {}
# For extracting team IDs, get promoted teams every year
response = requests.get(f"{base_url}team-season-stats", params={"league_id": league_id, "season_id": season_id} ,headers=header)
print(response.json())
teams = response.json()["data"]
for team in teams:
    team_name = team["meta_data"]["team_name"]
    team_id = team["meta_data"]["team_id"]
    team_id_map[team_name] = team_id