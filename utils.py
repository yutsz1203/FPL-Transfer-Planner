import json

import requests

from const import official_base_url

"""
Documentation: https://fbrapi.com/documentation

Endpoints:
/countries: GET method to retrieve football-related meta-data for all available countries
/leagues: GET method to retrieve meta-data for all unique leagues associated with a specified country.
/league-seasons: GET method to retrieve all season ids for a specific league id
/league-season-details: GET method to retrieve meta-data for a specific league id and season id.
/league-standings: GET method to retrieve all standings tables for a given league and season id.
/teams: GET method to retrieve team roster and schedule data
/players: GET method to retrieve player meta-data
/matches: GET method to retrieve to retrieve match meta-data.
/team-season-stats: GET method to retrieve season-level team statistical data for a specified league and season.
/team-match-stats: GET method to retrieve match-level team statistical data for a specified team, league and season.
/player-season-stats: GET method to retrieve aggregate season stats for all players for a team-league-season
/player-match-stats: GET method to retrieve matchlog data for a given player-league-season
/all-players-match-stats: GET method to retrieve match stats for all players in a match
"""

season_id = "2025-2026"
league_id = 9

# api = requests.post(base_url + generate_api_key)
# api_key = api.json()['api_key']
# print("API Key:", api_key)

# header = {"X-API-Key": api_key}
# from pathlib import Path

# print(Path(__file__).parent)
# df = pd.read_csv("players/results/player_season_stats.csv")
# print(df.columns)


def get_team_id_mapping():
    response = requests.get(f"{official_base_url}/bootstrap-static")

    data = response.json()
    teams = data["teams"]
    team_map = {}

    for team in teams:
        # Adjust team name for MatchHistory api
        if team["name"] == "Man Utd":
            team_map[team["id"]] = "Man United"
        elif team["name"] == "Spurs":
            team_map[team["id"]] = "Tottenham"
        else:
            team_map[team["id"]] = team["name"]

    with open("data/team_mapping.json", "w", encoding="utf-8") as f:
        json.dump(team_map, f, indent=4)

    print("Output team mappings to data/team_mapping.json")


if __name__ == "__main__":
    get_team_id_mapping()
