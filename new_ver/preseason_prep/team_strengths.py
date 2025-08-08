import pandas as pd

prem_team = pd.read_csv("data/2425-prem-teams.csv")

prem_lod = prem_team["goals_scored"].sum() / (38 * 10)
prem_team["Oi"] = prem_team["goals_scored"] / 38 / prem_lod
prem_team["Oi"] = prem_team["Oi"].round(2)

prem_team["Di"] = prem_team["goals_conceded"] / 38 / prem_lod
prem_team["Di"] = prem_team["Di"].round(2)

championship_team = pd.read_csv("data/2425-championship-teams.csv")

championship_lod = championship_team["goals_scored"].sum() / (46 * 10)
championship_team["Oi"] = championship_team["goals_scored"] / 46 / championship_lod
championship_team["Oi"] = championship_team["Oi"].round(2)

championship_team["Di"] = championship_team["goals_conceded"] / 46 / championship_lod
championship_team["Di"] = championship_team["Di"].round(2)

promoted_teams = ["Burnley", "Sunderland", "Leeds United"]
relegated_teams = ["Southampton", "Leicester City", "Ipswich Town"]

prem_team = prem_team[~prem_team["team"].isin(relegated_teams)]
promoted_teams = championship_team[championship_team["team"].isin(promoted_teams)]

prem_team = pd.concat([prem_team, promoted_teams], ignore_index=True)
prem_team = prem_team.sort_values(by=["team"])
print(prem_team)

prem_team.to_csv("data/2526-prem-teams.csv", index=False)

