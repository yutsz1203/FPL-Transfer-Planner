import pandas as pd
from pandas import Series, DataFrame
import numpy as np

import requests

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

base_url = "https://fbrapi.com/"
generate_api_key = "generate_api_key"
countries = "countries"
leagues = "leagues"
league_seasons = "league-seasons"  
league_season_details = "league-season-details"  
league_standings = "league-standings"
teams_api = "teams"
players_api = "players"
matches_api = "matches" 
team_season_stats = "team-season-stats"
team_match_stats = "team-match-stats"
player_season_stats = "player-season-stats"  
player_match_stats = "player-match-stats"  
all_players_match_stats = "all-players-match-stats"

season_id = "2025-2026"
league_id = 9

api = requests.post(base_url + generate_api_key)
api_key = api.json()['api_key']
print("API Key:", api_key)

header = {"X-API-Key": api_key}

team_id_map = {
    "Arsenal": "18bb7c10",
    "Aston Villa": "8602292d",
    "Bournemouth": "4ba7cbea",
    "Brentford": "cd051869",
    "Brighton": "d07537b9",
    "Burnley": "943e8050",
    "Chelsea": "cff3d9bb",
    "Crystal Palace": "47c64c55",
    "Everton": "d3fd31cc",
    "Fulham": "fd962109",
    "Leeds United": "5bfb9659",
    "Liverpool": "822bd0ba",
    "Manchester City": "b8fd03ef",
    "Manchester Utd": "19538871",
    "Newcastle Utd": "b2b47a98",
    "Nott'ham Forest": "e4a775cb",
    "Sunderland": "8ef52968",
    "Tottenham": "361ca564",
    "West Ham": "7c21e445",
    "Wolves": "8cec06e1"
}













