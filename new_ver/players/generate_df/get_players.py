import requests
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from const import official_base_url, element_type_map, official_team_id_map

response = requests.get(official_base_url + "bootstrap-static/")
data = response.json()["elements"]

players = []
index = []

for player in data:
    index.append(player["id"])
    players.append({
        "Name": player["web_name"],
        "Pos": element_type_map[player["element_type"]],
        "Team": official_team_id_map[player["team"]],
        "Cost": player["now_cost"]/10.0,
        "Selected by": player["selected_by_percent"],
    })
df = pd.DataFrame(players, index=index)
df.sort_index(inplace=True)
df.index.name = "Player ID"
print(df)
df.to_csv("players/data/players.csv")