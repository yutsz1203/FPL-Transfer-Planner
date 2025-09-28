import pandas as pd

def strength_calculation(df):
    lod = df["gf"].sum() / (38 * 20)
    df["Oi"] = df["gf"] / 38 / lod
    df["Oi"] = df["Oi"].round(2)
    df["Di"] = df["ga"] / 38 / lod
    df["Di"] = df["Di"].round(2)

    h_lod = df["h_gf"].sum() / (19 * 20)
    df["h_Oi"] = df["h_gf"] / 19 / h_lod
    df["h_Oi"] = df["h_Oi"].round(2)
    df["h_Di"] = df["h_ga"] / 19 / h_lod
    df["h_Di"] = df["h_Di"].round(2)

    a_lod = df["a_gf"].sum() / (19 * 20)
    df["a_Oi"] = df["a_gf"] / 19 / a_lod
    df["a_Oi"] = df["a_Oi"].round(2)
    df["a_Di"] = df["a_ga"] / 19 / a_lod
    df["a_Di"] = df["a_Di"].round(2)

    print(df)


prem_team_2223 = pd.read_csv("teams/data/2223-prem-teams.csv")
prem_team_2324 = pd.read_csv("teams/data/2324-prem-teams.csv")
prem_team_2425 = pd.read_csv("teams/data/2425-prem-teams.csv")

relegated_teams = ["Southampton", "Leicester City", "Ipswich Town"]

prem_team_2526 = prem_team_2425[~prem_team_2425["team"].isin(relegated_teams)]

strength_calculation(prem_team_2223)
print("*" * 90)
strength_calculation(prem_team_2324)
print("*" * 90)
strength_calculation(prem_team_2526)
print("*" * 90)

leeds = prem_team_2223[prem_team_2223["team"] == "Leeds United"]
burnley = prem_team_2324[prem_team_2324["team"] == "Burnley"]

avg_gf = (leeds["gf"].values[0] + burnley["gf"].values[0]) // 2
avg_ga = (leeds["ga"].values[0] + burnley["ga"].values[0]) // 2 
avg_h_gf = (leeds["h_gf"].values[0] + burnley["h_gf"].values[0]) // 2
avg_h_ga = (leeds["h_ga"].values[0] + burnley["h_ga"].values[0]) // 2
avg_a_gf = (leeds["a_gf"].values[0] + burnley["a_gf"].values[0]) // 2
avg_a_ga = (leeds["a_ga"].values[0] + burnley["a_ga"].values[0]) // 2
Oi = round((leeds["Oi"].values[0] + burnley["Oi"].values[0]) / 2, 2)
Di = round((leeds["Di"].values[0] + burnley["Di"].values[0]) / 2, 2)
h_Oi = round((leeds["h_Oi"].values[0] + burnley["h_Oi"].values[0]) / 2, 2)
h_Di = round((leeds["h_Di"].values[0] + burnley["h_Di"].values[0]) / 2, 2)
a_Oi = round((leeds["a_Oi"].values[0] + burnley["a_Oi"].values[0]) / 2, 2)
a_Di = round((leeds["a_Di"].values[0] + burnley["a_Di"].values[0]) / 2, 2)

sunderland = {
    "team": "Sunderland",
    "gf": avg_gf,
    "ga": avg_ga,
    "h_gf": avg_h_gf,
    "h_ga": avg_h_ga,
    "a_gf": avg_a_gf,
    "a_ga": avg_a_ga,
    "Oi": Oi,
    "Di": Di,
    "h_Oi": h_Oi,
    "h_Di": h_Di,
    "a_Oi": a_Oi,
    "a_Di": a_Di
}

prem_team_2526 = pd.concat([prem_team_2526, leeds, burnley, pd.DataFrame([sunderland])], ignore_index=True)
prem_team_2526 = prem_team_2526.sort_values(by=["team"])
print(prem_team_2526)

prem_team_2526.to_csv("teams/data/2526-prem-teams-lastseason.csv", index=False)

