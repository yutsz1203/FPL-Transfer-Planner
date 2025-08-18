import requests
import pandas as pd
import time
from rich.progress import Progress

#fbref api 
base_url = "https://fbrapi.com/"
generate_api_key = "generate_api_key"
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

# update every year to delete relegated teams and add promoted teams
team_ids = ["18bb7c10", "8602292d", "4ba7cbea", "cd051869", "d07537b9", "943e8050", "cff3d9bb", "47c64c55", "d3fd31cc", "fd962109", "5bfb9659", "822bd0ba", "b8fd03ef", "19538871", "b2b47a98", "e4a775cb", "8ef52968", "361ca564", "7c21e445", "8cec06e1"]

team_id_map = {
    "18bb7c10": "Arsenal",
    "8602292d": "Aston Villa",
    "4ba7cbea": "Bournemouth",
    "cd051869": "Brentford",
    "d07537b9": "Brighton",
    "943e8050": "Burnley",
    "cff3d9bb": "Chelsea",
    "47c64c55": "Crystal Palace",
    "d3fd31cc": "Everton",
    "fd962109": "Fulham",
    "5bfb9659": "Leeds United",
    "822bd0ba": "Liverpool",
    "b8fd03ef": "Manchester City",
    "19538871": "Manchester Utd",
    "b2b47a98": "Newcastle Utd",
    "e4a775cb": "Nott'ham Forest",
    "8ef52968": "Sunderland",
    "361ca564": "Tottenham",
    "7c21e445": "West Ham",
    "8cec06e1": "Wolves"
}

team_id_map_2223 = {'18bb7c10': 'Arsenal', '8602292d': 'Aston Villa', '4ba7cbea': 'Bournemouth', 'cd051869': 'Brentford', 'd07537b9': 'Brighton', 'cff3d9bb': 'Chelsea', '47c64c55': 'Crystal Palace', 'd3fd31cc': 'Everton', 'fd962109': 'Fulham', '5bfb9659': 'Leeds United', 'a2d435b3': 'Leicester City', '822bd0ba': 'Liverpool', 'b8fd03ef': 'Manchester City', '19538871': 'Manchester Utd', 'b2b47a98': 'Newcastle Utd', 'e4a775cb': "Nott'ham Forest", '33c895d4': 'Southampton', '361ca564': 'Tottenham', '7c21e445': 'West Ham', '8cec06e1': 'Wolves'}
team_id_map_2324 = {'18bb7c10': 'Arsenal', '8602292d': 'Aston Villa', '4ba7cbea': 'Bournemouth', 'cd051869': 'Brentford', 'd07537b9': 'Brighton', '943e8050': 'Burnley', 'cff3d9bb': 'Chelsea', '47c64c55': 'Crystal Palace', 'd3fd31cc': 'Everton', 'fd962109': 'Fulham', '822bd0ba': 'Liverpool', 'e297cd13': 'Luton Town', 'b8fd03ef': 'Manchester City', '19538871': 'Manchester Utd', 'b2b47a98': 'Newcastle Utd', 'e4a775cb': "Nott'ham Forest", '1df6b87e': 'Sheffield Utd', '361ca564': 'Tottenham', '7c21e445': 'West Ham', '8cec06e1': 'Wolves'}

# official api variables
official_base_url = "https://fantasy.premierleague.com/api/"
fpl_id = "157928"
official_team_id_map = {
    1: "Arsenal",
    2: "Aston Villa",
    3: "Burnley",
    4: "Bournemouth",
    5: "Brentford",
    6: "Brighton",
    7: "Chelsea",
    8: "Crystal Palace",
    9: "Everton",
    10: "Fulham",
    11: "Leeds",
    12: "Liverpool",
    13: "Man City",
    14: "Man Utd",
    15: "Newcastle",
    16: "Nott'm Forest",
    17: "Sunderland",
    18: "Spurs",
    19: "West Ham",
    20: "Wolves"
}
element_type_map = {
    1: "GK",
    2: "DEF",
    3: "MID",
    4: "FWD"
}

official_to_fbref_team_map = {
    "Arsenal": "Arsenal",
    "Aston Villa": "Aston Villa",
    "Bournemouth": "Bournemouth",
    "Brentford": "Brentford",
    "Brighton": "Brighton",
    "Burnley": "Burnley",
    "Chelsea": "Chelsea",
    "Crystal Palace": "Crystal Palace",
    "Everton": "Everton",
    "Fulham": "Fulham",
    "Leeds": "Leeds United",
    "Liverpool": "Liverpool",
    "Man City": "Manchester City",
    "Man Utd": "Manchester Utd",
    "Newcastle": "Newcastle Utd",
    "Nott'm Forest": "Nott'ham Forest",
    "Sunderland": "Sunderland",
    "Spurs": "Tottenham",
    "West Ham": "West Ham",
    "Wolves": "Wolves"
}

def wait(context):

    with Progress() as p:
        t = p.add_task(f"Waiting before fetching {context}...", total=200)
        for i in range(200,-1,-1):
            p.update(t, advance=1)
            time.sleep(0.05)

