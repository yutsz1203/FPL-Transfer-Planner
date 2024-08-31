import math
import sys
from functools import partial

import pandas as pd
import requests, json
import numpy as np
from bs4 import BeautifulSoup
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from pprint import pprint

#region Constants
COL_A = 1
COL_B = 2
COL_C = 3
COL_D = 4
COL_E = 5
COL_F = 6
COL_G = 7
COL_H = 8
COL_I = 9
COL_J = 10
COL_K = 11
COL_L = 12
COL_M = 13
COL_N = 14
COL_O = 15
COL_P = 16
COL_Q = 17
COL_R = 18
COL_S = 19
COL_T = 20
COL_U = 21
COL_V = 22

redFill = PatternFill(start_color='FFFF0000',end_color='FFFF0000', fill_type='solid')
yellowFill = PatternFill(start_color='FFFFFF00', end_color='FFFFFF00',fill_type='solid')
greenFill = PatternFill(start_color='ff00b050',end_color='ff00b050',fill_type='solid')
lightGreenFill = PatternFill(start_color='ffc6e0b4',end_color='ffc6e0b4',fill_type='solid')
blueFill = PatternFill(start_color='ff2f75b5',end_color='ff2f75b5',fill_type='solid')
lightBlueFill = PatternFill(start_color='ffbdd7ee',end_color='ffbdd7ee',fill_type='solid')

BASE_URL = "https://fantasy.premierleague.com/api/bootstrap-static/"
ID = 1185677
EXCEL_FILE = "FootballPoisson.xlsx"
GAME_THRESHOLD = 0

team_map = {
        "ARS": 2,
        "AVL": 3,
        "BOU": 4,
        "BRE": 5,
        "BHA": 6,
        "CHE": 7,
        "CRY": 8,
        "EVE": 9,
        "FUL": 10,
        "IPS": 11,
        "LEI": 12,
        "LIV": 13,
        "MCI": 14,
        "MUN": 15,
        "NEW": 16,
        "NFO": 17,
        "SOU": 18,
        "TOT": 19,
        "WHU": 20,
        "WOL": 21
        }

teams = {
        1: "Arsenal",
        2: "Aston Villa",
        3: "Bournemouth",
        4: "Brentford",
        5: "Brighton",
        6: "Chelsea",
        7: "Crystal Palace",
        8: "Everton",
        9: "Fulham",
        10: "Ipswich",
        11: "Leicester",
        12: "Liverpool",
        13: "Man City",
        14: "Man Utd",
        15: "Newcastle",
        16: "Nott'm Forest",
        17: "Southampton",
        18: "Spurs",
        19: "West Ham",
        20: "Wolves"
    }
position = {
        1: "GK",
        2: "DEF",
        3: "MID",
        4: "FWD"
    }
#region Helper functions
def get_fmt_str(x, fill):
        return "{message: >{fill}}".format(message=x, fill=fill)

def format_columns(df):
    s = df.astype(str).agg(lambda x: x.str.len()).max() 

    pad = 6  
    fmts = {}
    for idx, c_len in s.items():
        if isinstance(idx, tuple):
            lab_len = max([len(str(x)) for x in idx])
        else:
            lab_len = len(str(idx))

        fill = max(lab_len, c_len) + pad - 1
        fmts[idx] = partial(get_fmt_str, fill=fill)
    return fmts

def write_df_to_sheet(df, sheet):
    for row, value in enumerate(df.values, start=2):
        for col, cell in enumerate(value, start=1):
            sheet.cell(row=row, column=col, value=cell)

#region Get data functions
def get_gameweek():
    gws = requests.get(BASE_URL).json()["events"]
    for gw in gws:
        if gw["is_current"]:
            return gw["id"]

#region Main functions
def update_teams():
    #web scrapping
    url = "https://fpl.page/bonus"
    page = requests.get(url)

    soup = BeautifulSoup(page.text, "html.parser")
    
    fixtures = soup.find_all("li", class_="fixture-item")
    
    teams = []

    for fixture in fixtures:
        home_team = fixture.find("span", class_="home-text").text.strip()
        away_team = fixture.find("span", class_="away-text").text.strip()
        score_box = fixture.find("span", class_="score-box")
        if score_box:
            scores = score_box.text.split("-")
            scores = list(map(int, scores))
            
            teams.append({"Team": home_team, "Side": "H", "GF": scores[0], "GA": scores[1]})
            teams.append({"Team": away_team, "Side": "A", "GF": scores[1], "GA": scores[0]})

    print("Finished getting gameweek data")
    #update excel
    wb = load_workbook(EXCEL_FILE)
    sheet = wb["Team Data"]

    df = pd.read_excel(EXCEL_FILE, sheet_name="Team Data", usecols="A:V", header=0, nrows=20, dtype={"Team": str, "H_GF": int, "H_GA": int, "A_GF": int, "A_GA": int, "GF": int, "GA": int, "H_Games": int, "A_Games": int, "Games": int, "H_Avg.GF": float, "H_Avg.GA": float, "A_Avg.GF": float, "A_Avg.GA": float,  "Avg.GF": float,  "Avg.GA": float, "H_Oi": float, "H_Di": float, "A_Oi": float, "A_Di": float, "Oi": float, "Di": float})
    for team in teams:
        team_name = team["Team"]
        team_row = df.index[df["Team"] == team_name].tolist()[0]
        df.loc[team_row, "GF"] += team["GF"]
        df.loc[team_row, "GA"] += team["GA"]
        df.loc[team_row, "Games"] += 1
        df.loc[team_row, "Avg.GF"] = df.loc[team_row, "GF"] / df.loc[team_row, "Games"]
        df.loc[team_row, "Avg.GA"] = df.loc[team_row, "GA"] / df.loc[team_row, "Games"]

        #update home side
        if team["Side"] == "H":
            df.loc[team_row, "H_GF"] += team["GF"]
            df.loc[team_row, "H_GA"] += team["GA"]
            df.loc[team_row, "H_Games"] += 1
        #update away side
        elif team["Side"] == "A":
            df.loc[team_row, "A_GF"] += team["GF"]
            df.loc[team_row, "A_GA"] += team["GA"]
            df.loc[team_row, "A_Games"] += 1

    df["H_Avg.GF"] = df["H_GF"] / df["H_Games"]
    df["H_Avg.GA"] = df["H_GA"] / df["H_Games"]
    df["A_Avg.GF"] = df["A_GF"] / df["A_Games"]
    df["A_Avg.GA"] = df["A_GA"] / df["A_Games"]
    df["Avg.GF"] = df["GF"] / df["Games"]
    df["Avg.GA"] = df["GA"] / df["Games"]

    lod = df["GF"].sum() / df["Games"].sum()
    df["Oi"] = df["Avg.GF"] / lod
    df["Di"] = df["Avg.GA"] / lod

    h_lod = df["H_GF"].sum() / df["H_Games"].sum()
    df["H_Oi"] = df["H_Avg.GF"] / h_lod
    df["H_Di"] = df["H_Avg.GA"] / h_lod

    a_lod = df["A_GF"].sum() / df["A_Games"].sum()
    df["A_Oi"] = df["A_Avg.GF"] / a_lod
    df["A_Di"] = df["A_Avg.GA"] / a_lod

    cols = ["H_Avg.GF", "H_Avg.GA", "H_Oi", "H_Di", "A_Avg.GF", "A_Avg.GA", "A_Oi", "A_Di", "Avg.GF", "Avg.GA", "Oi", "Di"]
    for col in cols:
        df[col] = df[col].round(2)

    sheet["B23"] = df["H_GF"].sum()
    sheet["C23"] = df["H_GA"].sum()
    sheet["D23"] = df["A_GF"].sum()
    sheet["E23"] = df["A_GA"].sum()
    sheet["F23"] = df["GF"].sum()
    sheet["G23"] = df["GA"].sum()
    sheet["H23"] = df["H_Games"].sum()
    sheet["I23"] = df["A_Games"].sum()
    sheet["J23"] = df["Games"].sum()

    sheet["K23"] = df["H_Avg.GF"].mean()
    sheet["L23"] = df["H_Avg.GA"].mean()
    sheet["M23"] = df["A_Avg.GF"].mean()
    sheet["N23"] = df["A_Avg.GA"].mean()
    sheet["O23"] = df["Avg.GF"].mean()
    sheet["P23"] = df["Avg.GA"].mean()
    sheet["Q23"] = df["H_Oi"].mean()
    sheet["R23"] = df["H_Di"].mean()
    sheet["S23"] = df["A_Oi"].mean()
    sheet["T23"] = df["A_Di"].mean()
    sheet["U23"] = df["Oi"].mean()
    sheet["V23"] = df["Di"].mean()

    sheet["B24"] = h_lod
    sheet["E24"] = a_lod
    sheet["H24"] = lod

    home_top_attacking = df.sort_values(by=["H_Oi"], ascending=False)["Team"].head(5).tolist()
    away_top_attacking = df.sort_values(by=["A_Oi"], ascending=False)["Team"].head(5).tolist()
    top_attacking = df.sort_values(by=["Oi"], ascending=False)["Team"].head(5).tolist()

    home_top_defending = df.sort_values(by=["H_Di"], ascending=True)["Team"].head(5).tolist()
    away_top_defending = df.sort_values(by=["A_Di"], ascending=True)["Team"].head(5).tolist()
    top_defending = df.sort_values(by=["Di"], ascending=True)["Team"].head(5).tolist()

    home_top_attacking.sort()
    away_top_attacking.sort()
    top_attacking.sort()

    home_top_defending.sort()
    away_top_defending.sort()
    top_defending.sort()

    low_oi_index = df.sort_values(by=["Oi"], ascending=True)["Oi"].head(5).index.tolist()
    high_oi_index = df.sort_values(by=["Oi"], ascending=False)["Oi"].head(5).index.tolist()
    high_di_index = df.sort_values(by=["Di"], ascending=False)["Di"].head(5).index.tolist()
    low_di_index = df.sort_values(by=["Di"], ascending=True)["Di"].head(5).index.tolist()

    columns = ["B", "C", "D", "E", "F"]

    for i, col in enumerate(columns):
        sheet[f"{col}26"] = home_top_attacking[i]
        sheet[f"{col}27"] = away_top_attacking[i]
        sheet[f"{col}28"] = top_attacking[i]

        sheet[f"{col}30"] = home_top_defending[i]
        sheet[f"{col}31"] = away_top_defending[i]
        sheet[f"{col}32"] = top_defending[i]

    for r_idx, row in enumerate(df.values, start=2):
        for c_idx, value in enumerate(row, start=1):
            sheet.cell(row=r_idx, column=c_idx, value=value)

    for high_oi_idx, low_oi_idx, high_di_idx, low_di_idx in zip(high_oi_index, low_oi_index, high_di_index, low_di_index):
        sheet.cell(row=low_oi_idx + 2, column=COL_U).fill = redFill
        sheet.cell(row=high_di_idx + 2, column=COL_V).fill = redFill

        sheet.cell(row=high_oi_idx + 2, column=COL_U).fill = blueFill
        sheet.cell(row=high_oi_idx + 2, column=COL_A).fill = blueFill

        sheet.cell(row=low_di_idx + 2, column=COL_V).fill = greenFill
        sheet.cell(row=low_di_idx + 2, column=COL_A).fill = greenFill

        if high_oi_idx in low_di_index:
            sheet.cell(row=high_oi_idx + 2, column=COL_A).fill = yellowFill
        
        if low_di_idx in high_oi_index:
            sheet.cell(row=low_di_idx + 2, column=COL_A).fill = yellowFill
        
        if low_oi_idx in high_di_index:
            sheet.cell(row=low_oi_idx + 2, column=COL_A).fill = redFill
        
        if high_di_idx in low_oi_index:
            sheet.cell(row=high_di_idx + 2, column=COL_A).fill = redFill

    print("Finished updating team gameweek data.")    
    wb.save(EXCEL_FILE)
    print(df)

def update_fixture():
    #web scrapping
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://fpl.page/fixtureTicker")

    #get gameweeks
    headers = driver.find_elements(By.CSS_SELECTOR, "th.fdr-teamNames")
    combined_headers = "".join([header.get_attribute("innerHTML") for header in headers[0:5]])
    header_soup = BeautifulSoup(combined_headers, "html.parser")
    gameweeks = ["GW" + text.strip("GW") for text in header_soup.stripped_strings if text != "GW"]
    print("Finished getting gameweeks.")

    #get fixtures
    table = driver.find_element(By.CSS_SELECTOR, ".transfers-body") 
    table_soup = BeautifulSoup(table.get_attribute("innerHTML"), "html.parser")
    teams = table_soup.find_all("tr")

    fixtures = []

    for team in teams:
        team_name = team.find("td", class_="fdr-teamNames").text
        tds = team.find_all("td")[1:6]
        opponents = [td.find("span").text for td in tds if td.find("span")]
        fixtures.append({"Team": team_name, "Next 5": opponents})
    print("Finished getting fixtures.")

    driver.quit()

    #update excel
    wb = load_workbook(EXCEL_FILE, data_only=True)
    sheet = wb["Fixtures"]

    for col, gameweek in enumerate(gameweeks, start=2):
        cell = sheet.cell(row=1, column=col, value=gameweek)

    team_data_sheet = wb["Team Data"]
    for row in range (2,22):
        sheet[f"A{row}"] = fixtures[row-2]["Team"]
        sheet[f"G{row}"] = 0
        sheet[f"H{row}"] = 0
        for col, opponent in enumerate(fixtures[row - 2]["Next 5"], start=2):
            #filling in opponents
            cell = sheet.cell(row=row, column=col, value=opponent)

            #aggregating Oi and Di
            cleaned_opponent = opponent.split(" ")[0]
            team_row = team_map[cleaned_opponent]

            #gets opponent's Away Oi, Di
            if(cleaned_opponent[1] == "(H)"):
                sheet[f"G{row}"] = sheet[f"G{row}"].value + team_data_sheet[f"S{team_row}"].value
                sheet[f"H{row}"] = sheet[f"H{row}"].value + team_data_sheet[f"T{team_row}"].value
            else:
                sheet[f"G{row}"] = sheet[f"G{row}"].value + team_data_sheet[f"Q{team_row}"].value
                sheet[f"H{row}"] = sheet[f"H{row}"].value + team_data_sheet[f"R{team_row}"].value

    wb.save(EXCEL_FILE)
    df = pd.read_excel(EXCEL_FILE, sheet_name="Fixtures", usecols="G:H", header=0, nrows=20, dtype={"Oi": float, "Di": float})

    sheet["G23"].value = df["Oi"].mean()
    sheet["H23"].value = df["Di"].mean()

    low_oi_index = df.sort_values(by=["Oi"], ascending=True)["Oi"].head(5).index.tolist()
    high_oi_index = df.sort_values(by=["Oi"], ascending=False)["Oi"].head(5).index.tolist()
    high_di_index = df.sort_values(by=["Di"], ascending=False)["Di"].head(5).index.tolist()
    low_di_index = df.sort_values(by=["Di"], ascending=True)["Di"].head(5).index.tolist()

    low_oi_index.sort()
    high_di_index.sort()
    for col, (low_oi_idx, high_di_idx) in enumerate(zip(low_oi_index, high_di_index), start=2):
        sheet.cell(row=24, column=col, value=sheet[f"A{high_di_idx + 2}"].value)
        sheet.cell(row=25, column=col, value=sheet[f"A{low_oi_idx + 2}"].value)
    
    for high_oi_idx, low_oi_idx, high_di_idx, low_di_idx in zip(high_oi_index, low_oi_index, high_di_index, low_di_index):
        sheet.cell(row=high_oi_idx + 2, column=COL_G).fill = redFill
        sheet.cell(row=low_di_idx + 2, column=COL_H).fill = redFill

        sheet.cell(row=low_oi_idx + 2, column=COL_G).fill = greenFill
        sheet.cell(row=low_oi_idx + 2, column=COL_A).fill = greenFill

        sheet.cell(row=high_di_idx + 2, column=COL_H).fill = blueFill
        sheet.cell(row=high_di_idx + 2, column=COL_A).fill = blueFill

        if low_oi_idx in high_di_index:
            sheet.cell(row=low_oi_idx + 2, column=COL_A).fill = yellowFill
        
        if high_di_idx in low_oi_index:
            sheet.cell(row=high_di_idx + 2, column=COL_A).fill = yellowFill
        
        if high_oi_idx in low_di_index:
            sheet.cell(row=high_oi_idx + 2, column=COL_A).fill = redFill
        
        if low_di_idx in high_oi_index:
            sheet.cell(row=low_di_idx + 2, column=COL_A).fill = redFill


    print("Finished updating fixture data.")
    print(df)
    wb.save(EXCEL_FILE)

def show_summary():
    wb = load_workbook(EXCEL_FILE)
    team_data_sheet = wb["Team Data"]
    fixture_sheet = wb["Fixtures"]

    team_df = pd.read_excel(EXCEL_FILE, sheet_name="Team Data", usecols="A:H", header=0, nrows=20, dtype={"Team": str, "GF": int, "GA": int, "Games": int, "Avg.GF": float, "Avg.GA": float, "Oi": float, "Di": float})
    top_attacking_team = []
    top_defending_team = []

    columns = ["B", "C", "D", "E", "F"]

    for col in columns:
        attack_team = team_data_sheet[f"{col}26"].value
        defend_team = team_data_sheet[f"{col}27"].value 
        top_attacking_team.append({"Team": attack_team, "Oi": team_df.loc[team_df["Team"] == attack_team, "Oi"].values[0], "Di": team_df.loc[team_df["Team"] == attack_team, "Di"].values[0]})
        top_defending_team.append({"Team": defend_team, "Oi": team_df.loc[team_df["Team"] == defend_team, "Oi"].values[0], "Di": team_df.loc[team_df["Team"] == defend_team, "Di"].values[0]})

    fixture_df = pd.read_excel(EXCEL_FILE, sheet_name="Fixtures", usecols="A:H", header=0, nrows=20, dtype={"Oi": float, "Di": float})
    favourable_attacking_teams = []
    favourable_defending_teams = []

    gameweeks = fixture_df.columns[1:6]

    for col in columns:
        attack_team = fixture_sheet[f"{col}24"].value
        defend_team = fixture_sheet[f"{col}25"].value
        favourable_attacking_teams.append(
            {"Team": attack_team, 
             gameweeks[0]: fixture_df.loc[fixture_df["Team"] == attack_team, gameweeks[0]].values[0],
             gameweeks[1]: fixture_df.loc[fixture_df["Team"] == attack_team, gameweeks[1]].values[0],
             gameweeks[2]: fixture_df.loc[fixture_df["Team"] == attack_team, gameweeks[2]].values[0],
             gameweeks[3]: fixture_df.loc[fixture_df["Team"] == attack_team, gameweeks[3]].values[0],
             gameweeks[4]: fixture_df.loc[fixture_df["Team"] == attack_team, gameweeks[4]].values[0],
             "Oi": fixture_df.loc[fixture_df["Team"] == attack_team, "Oi"].values[0], 
             "Di": fixture_df.loc[fixture_df["Team"] == attack_team, "Di"].values[0],
            }
            )
        favourable_defending_teams.append(
            {"Team": defend_team, 
             gameweeks[0]: fixture_df.loc[fixture_df["Team"] == defend_team, gameweeks[0]].values[0],
             gameweeks[1]: fixture_df.loc[fixture_df["Team"] == defend_team, gameweeks[1]].values[0],
             gameweeks[2]: fixture_df.loc[fixture_df["Team"] == defend_team, gameweeks[2]].values[0],
             gameweeks[3]: fixture_df.loc[fixture_df["Team"] == defend_team, gameweeks[3]].values[0],
             gameweeks[4]: fixture_df.loc[fixture_df["Team"] == defend_team, gameweeks[4]].values[0],
             "Oi": fixture_df.loc[fixture_df["Team"] == defend_team, "Oi"].values[0], 
             "Di": fixture_df.loc[fixture_df["Team"] == defend_team, "Di"].values[0],
             }
            )

    gameweek = team_df["Games"].max()
    separator = "--------------------"
    print(f"Summary as at GW {gameweek}")
    print(separator)
    
    # team
    print(f"Average Oi: {math.floor(team_data_sheet['G23'].value * 100)/100}\n")
    print("Top 5 attacking teams")
    top_attacking_team_df = pd.DataFrame(top_attacking_team)
    print(top_attacking_team_df.sort_values(by=["Oi"], ascending=False).to_string(index=False, formatters=format_columns(top_attacking_team_df)))
    
    print(separator)
    print(f"Average Di: {math.floor(team_data_sheet['H23'].value * 100)/100}\n")
    print("Top 5 defending teams")
    top_defending_team_df = pd.DataFrame(top_defending_team)
    print(top_defending_team_df.sort_values(by=["Di"], ascending=True).to_string(index=False, formatters=format_columns(top_defending_team_df)))
    print(separator)

    # fixture
    print("Top 5 favourable attacking teams")
    print(f"Average aggregated Di: {math.floor(fixture_sheet['H23'].value * 100)/100}\n")
    favourable_attacking_teams_df = pd.DataFrame(favourable_attacking_teams)
    print(favourable_attacking_teams_df.sort_values(by=["Di"], ascending=False).to_string(index=False, formatters=format_columns(favourable_attacking_teams_df)))   
    print(separator)
    
    print("Top 5 favourable defending teams")
    print(f"Average aggregated Oi: {math.floor(fixture_sheet['G23'].value * 100)/100}\n" )
    favourable_defending_teams_df = pd.DataFrame(favourable_defending_teams)
    print(favourable_defending_teams_df.sort_values(by=["Oi"], ascending=True).to_string(index=False, formatters=format_columns(favourable_defending_teams_df)))

def update_player_season():
    gk_df = pd.read_excel(EXCEL_FILE, sheet_name="GK-Season", usecols="A:AB", header=0, nrows=23)
    def_df = pd.read_excel(EXCEL_FILE, sheet_name="DEF-Season", usecols="A:AI", header=0, nrows=100)
    mid_df = pd.read_excel(EXCEL_FILE, sheet_name="MID-Season", usecols="A:AI", header=0, nrows=120)
    fwd_df = pd.read_excel(EXCEL_FILE, sheet_name="FWD-Season", usecols="A:AI", header=0, nrows=30)

    r = requests.get(BASE_URL).json() 
    players = r["elements"] # 1 to 567
    gw = [get_gameweek()-1]
    #gw = range(0,2) set certain range when i forgot to update the data after a gw
    for player in players:
        if player["starts"] > GAME_THRESHOLD:
            print(player["web_name"])
            if player["element_type"] == 1:
                df = gk_df
                player_row = gk_df.index[gk_df["Name"] == player["web_name"]].tolist()[0]
            elif player["element_type"] == 2:
                df = def_df
                player_row = def_df.index[def_df["Name"] == player["web_name"]].tolist()[0]
            elif player["element_type"] == 3:
                df = mid_df
                player_row = mid_df.index[mid_df["Name"] == player["web_name"]].tolist()[0]
            elif player["element_type"] == 4:
                df = fwd_df
                player_row = fwd_df.index[fwd_df["Name"] == player["web_name"]].tolist()[0]
            for i in gw:
                id = player["id"]
                individual = requests.get(f"https://fantasy.premierleague.com/api/element-summary/{id}/").json()["history"]
                gw_stat = individual[i]
                side = "H" if gw_stat["was_home"] else "A"
                if player["element_type"] == 1:
                    df.iloc[player_row, df.columns.get_loc(f"{side}_Points")] += gw_stat["total_points"]
                    df.iloc[player_row, df.columns.get_loc(f"{side}_CS")] += gw_stat["clean_sheets"]
                    df.iloc[player_row, df.columns.get_loc(f"{side}_Goals Conceded")] += gw_stat["goals_conceded"]
                    df.iloc[player_row, df.columns.get_loc(f"{side}_xG Conceded")] += float(gw_stat["expected_goals_conceded"])
                    df.iloc[player_row, df.columns.get_loc(f"{side}_xG Prevented")] = df.iloc[player_row, df.columns.get_loc(f"{side}_xG Conceded")] - df.iloc[player_row, df.columns.get_loc(f"{side}_Goals Conceded")]
                    df.iloc[player_row, df.columns.get_loc(f"{side}_Saves")] += gw_stat["saves"]
                    df.iloc[player_row, df.columns.get_loc(f"{side}_Bonus")] += gw_stat["bonus"]
                else:
                    df.iloc[player_row, df.columns.get_loc(f"{side}_Points")] += gw_stat["total_points"]
                    df.iloc[player_row, df.columns.get_loc(f"{side}_G")] += gw_stat["goals_scored"]
                    df.iloc[player_row, df.columns.get_loc(f"{side}_xG")] += float(gw_stat["expected_goals"])
                    df.iloc[player_row, df.columns.get_loc(f"{side}_xGDiff")] = df.iloc[player_row, df.columns.get_loc(f"{side}_xG")] - df.iloc[player_row, df.columns.get_loc(f"{side}_G")]
                    df.iloc[player_row, df.columns.get_loc(f"{side}_A")] += gw_stat["assists"]
                    df.iloc[player_row, df.columns.get_loc(f"{side}_xA")] += float(gw_stat["expected_assists"])
                    df.iloc
                    df.iloc[player_row, df.columns.get_loc(f"{side}_xGI")] += float(gw_stat["expected_goal_involvements"])
                    df.iloc[player_row, df.columns.get_loc(f"{side}_Bonus")] += gw_stat["bonus"]
            if player["element_type"] == 1:
                df.iloc[player_row, df.columns.get_loc("Points")] = df.iloc[player_row, df.columns.get_loc("H_Points")] + df.iloc[player_row, df.columns.get_loc("A_Points")]
                df.iloc[player_row, df.columns.get_loc("CS")] = df.iloc[player_row, df.columns.get_loc("H_CS")] + df.iloc[player_row, df.columns.get_loc("A_CS")]
                df.iloc[player_row, df.columns.get_loc("Goals Conceded")] = df.iloc[player_row, df.columns.get_loc("H_Goals Conceded")] + df.iloc[player_row, df.columns.get_loc("A_Goals Conceded")]
                df.iloc[player_row, df.columns.get_loc("xG Conceded")] = df.iloc[player_row, df.columns.get_loc("H_xG Conceded")] + df.iloc[player_row, df.columns.get_loc("A_xG Conceded")]
                df.iloc[player_row, df.columns.get_loc("Saves")] = df.iloc[player_row, df.columns.get_loc("H_Saves")] + df.iloc[player_row, df.columns.get_loc("A_Saves")]
                df.iloc[player_row, df.columns.get_loc("Bonus")] = df.iloc[player_row, df.columns.get_loc("H_Bonus")] + df.iloc[player_row, df.columns.get_loc("A_Bonus")]
            else: 
                df.iloc[player_row, df.columns.get_loc("Points")] = df.iloc[player_row, df.columns.get_loc("H_Points")] + df.iloc[player_row, df.columns.get_loc("A_Points")]
                df.iloc[player_row, df.columns.get_loc("G")] = df.iloc[player_row, df.columns.get_loc("H_G")] + df.iloc[player_row, df.columns.get_loc("A_G")]
                df.iloc[player_row, df.columns.get_loc("xG")] = df.iloc[player_row, df.columns.get_loc("H_xG")] + df.iloc[player_row, df.columns.get_loc("A_xG")]
                df.iloc[player_row, df.columns.get_loc("A")] = df.iloc[player_row, df.columns.get_loc("H_A")] + df.iloc[player_row, df.columns.get_loc("A_A")]

def update_player_last5():
    r = requests.get(BASE_URL).json() 
    players = r["elements"] # 1 to 567
    gw = get_gameweek()
    #gameweeks = range(gw-1, gw+4) if gw >= 5 else range(0, gw)
    gameweeks = range(0,2)

    gks, defs, mids, fwds = [], [], [], []
    for player in players:
        points, starts, games, cs,  goals_conceded, xg_conceded, saves, bonus, xg, g, xa, a, xgi = [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]
        if player["starts"] > GAME_THRESHOLD:
            id = player["id"]
            individual = requests.get(f"https://fantasy.premierleague.com/api/element-summary/{id}/").json()["history"]
            if len(individual) == 1:
                gameweeks = [0]
            for i in gameweeks:
                gw_stat = individual[i]
                index = 0 if gw_stat["was_home"] else 1
                points[index] += gw_stat["total_points"]
                starts[index] += gw_stat["starts"]
                games[index] += 1 if gw_stat["minutes"] > 0 else 0
                cs[index] += gw_stat["clean_sheets"]
                goals_conceded[index] += gw_stat["goals_conceded"]
                xg_conceded[index] += float(gw_stat["expected_goals_conceded"])
                saves[index] += gw_stat["saves"]
                bonus[index] += gw_stat["bonus"]
                xg[index] += float(gw_stat["expected_goals"])
                g[index] += gw_stat["goals_scored"]
                xa[index] += float(gw_stat["expected_assists"])
                a[index] += gw_stat["assists"]
                xgi[index] += float(gw_stat["expected_goal_involvements"])
            total_points = points[0] + points[1]
            total_starts = starts[0] + starts[1]
            total_games = games[0] + games[1]
            total_cs = cs[0] + cs[1]    
            total_goals_conceded = goals_conceded[0] + goals_conceded[1]
            total_xg_conceded = xg_conceded[0] + xg_conceded[1]
            total_saves = saves[0] + saves[1]
            total_bonus = bonus[0] + bonus[1]
            total_xg = xg[0] + xg[1]
            total_g = g[0] + g[1]
            total_xa = xa[0] + xa[1]
            total_a = a[0] + a[1]
            total_xgi = xgi[0] + xgi[1]
            outfield_list = [player["web_name"],
                    teams[player["team"]],
                    (player["now_cost"] / 10.0),
                    position[player["element_type"]],
                    player["form"],
                    total_starts,
                    total_games,
                    points[0],
                    points[1],
                    total_points,
                    round(points[0] / (player["now_cost"] / 10.0), 2),
                    round(points[1] / (player["now_cost"] / 10.0), 2),
                    round(total_points / (player["now_cost"] / 10.0), 2),
                    g[0],
                    float(xg[0]),
                    float(xg[0] - g[0]),
                    g[1],
                    float(xg[1]),
                    float(xg[1] - g[1]),
                    total_g,
                    float(total_xg),
                    float(total_xg - total_g),
                    a[0],
                    float(xa[0]),
                    float(xa[0] - a[0]),
                    a[1],
                    float(xa[1]),
                    float(xa[1] - a[1]),
                    total_a,
                    float(total_xa),
                    float(total_xa - total_a),
                    float(xgi[0]),
                    float(xgi[0] - g[0] - a[0]),
                    float(xgi[1]),
                    float(xgi[1] - g[1] - a[1]),
                    float(total_xgi),
                    float(total_xgi - total_g - total_a),
                    bonus[0],
                    bonus[1],
                    total_bonus,]
            if player["element_type"] == 1:
                gks.append([
                    player["web_name"],
                    teams[player["team"]],
                    (player["now_cost"] / 10.0),
                    position[player["element_type"]],
                    total_starts,
                    total_games,
                    points[0],
                    points[1],
                    total_points,
                    round(points[0] / (player["now_cost"] / 10.0), 2),
                    round(points[1] / (player["now_cost"] / 10.0), 2),
                    round(total_points / (player["now_cost"] / 10.0), 2),
                    int(cs[0]),
                    int(cs[1]),
                    int(total_cs),
                    goals_conceded[0],
                    float(xg_conceded[0]),
                    float(xg_conceded[0] - goals_conceded[0]),
                    goals_conceded[1],
                    float(xg_conceded[1]),
                    float(xg_conceded[1] - goals_conceded[1]),
                    total_goals_conceded,
                    float(total_xg_conceded),
                    float(total_xg_conceded - total_goals_conceded),
                    saves[0],
                    saves[1],
                    total_saves,
                    bonus[0],
                    bonus[1],
                    total_bonus,    
                ])
            elif player["element_type"] == 2:
                defs.append(outfield_list)
            elif player["element_type"] == 3:
                mids.append(outfield_list)
            elif player["element_type"] == 4:
                fwds.append(outfield_list)
        print("Updated " + player["web_name"])

    gk_column = ["Name", "Team", "Price", "Pos", "Starts", "Games", "H_Points", "A_Points", "Points", "H_Points/$", "A_Points/$", "Points/$",
    "H_CS", "A_CS", "CS", "H_Goals Conceded", "H_xG Conceded", "H_xG Prevented", "A_Goals Conceded", "A_xG Conceded",
    "A_xG Prevented", "Goals Conceded", "xG Conceded", "xGoals Prevented", "H_Saves", "A_Saves", "Saves", "H_Bonus",
    "A_Bonus", "Bonus"]

    column = [
    "Name", "Team", "Price", "Pos", "Form", "Starts", "Games", "H_Points", "A_Points", "Points", "H_Points/$", "A_Points/$", "Points/$",
    "H_G", "H_xG", "H_xGDiff", "A_G", "A_xG", "A_xGDiff", "G", "xG", "xGDiff", "H_A", "H_xA", "H_xADiff", "A_A", "A_xA",
    "A_xADiff", "A", "xA", "xADiff", "H_xGI", "H_xGIDIFF", "A_xGI", "A_xGIDIFF", "xGI", "xGIDIFF", "H_Bonus", "A_Bonus", "Bonus"
    ]

    gk_df = pd.DataFrame(gks, columns=gk_column)
    def_df = pd.DataFrame(defs, columns=column)
    mid_df = pd.DataFrame(mids, columns=column)
    fwd_df = pd.DataFrame(fwds, columns=column)
    
    wb = load_workbook(EXCEL_FILE)
    gk_sheet = wb["GK-Last5"]
    def_sheet = wb["DEF-Last5"]
    mid_sheet = wb["MID-Last5"]
    fwd_sheet = wb["FWD-Last5"]

    write_df_to_sheet(gk_df, gk_sheet)
    write_df_to_sheet(def_df, def_sheet)
    write_df_to_sheet(mid_df, mid_sheet)
    write_df_to_sheet(fwd_df, fwd_sheet)
    print("Finished updated player data.")
    wb.save(EXCEL_FILE)


def update_my_team():
    gw = get_gameweek()
    url = f"https://fantasy.premierleague.com/api/entry/{ID}/event/{gw}/picks/"
    team = requests.get(url).json()["picks"]
    player_ids = [player["element"] for player in team]
    r = requests.get(BASE_URL).json()["elements"]
    players = [player for player in r if player["id"] in player_ids]

    wb = load_workbook(EXCEL_FILE)
    gk_df = pd.read_excel(EXCEL_FILE, sheet_name="GK", usecols="A:M", header=0, nrows=25, dtype={"Name": str, "Team": str, "Price": float, "Pos": str, "GW Points": int, "Total Points": int, "Points/$": float, "CS": int, "Goals Conceded": int, "xG Conceded": float, "xGoals Prevented": float, "Saves": int, "Bonus": int})
    def_df = pd.read_excel(EXCEL_FILE, sheet_name="DEF", usecols="A:P", header=0, nrows=150, dtype={"Name": str, "Team": str, "Price": float, "Pos": str, "Form": float, "GW Points": int, "Total Points": int, "Points/$": float, "xG": float, "G": int, "xG+-": float, "xA": float, "A": int, "xA+-": float, "xGI": float, "Bonus": int})
    mid_df = pd.read_excel(EXCEL_FILE, sheet_name="MID", usecols="A:P", header=0, nrows=150, dtype={"Name": str, "Team": str, "Price": float, "Pos": str, "Form": float, "GW Points": int, "Total Points": int, "Points/$": float, "xG": float, "G": int, "xG+-": float, "xA": float, "A": int, "xA+-": float, "xGI": float, "Bonus": int})
    fwd_df = pd.read_excel(EXCEL_FILE, sheet_name="FWD", usecols="A:P", header=0, nrows=50, dtype={"Name": str, "Team": str, "Price": float, "Pos": str, "Form": float, "GW Points": int, "Total Points": int, "Points/$": float, "xG": float, "G": int, "xG+-": float, "xA": float, "A": int, "xA+-": float, "xGI": float, "Bonus": int})

    team_gk_rows = []
    team_def_rows = []
    team_mid_rows = []
    team_fwd_rows = []

    for player in players:
        if player["element_type"] == 1:
            team_gk_rows.append(gk_df.loc[gk_df["Name"] == player["web_name"]])
        elif player["element_type"] == 2:
            team_def_rows.append(def_df.loc[def_df["Name"] == player["web_name"]])
        elif player["element_type"] == 3:
            team_mid_rows.append(mid_df.loc[mid_df["Name"] == player["web_name"]])
        elif player["element_type"] == 4:
            team_fwd_rows.append(fwd_df.loc[fwd_df["Name"] == player["web_name"]])

    team_gk_df = pd.concat(team_gk_rows, ignore_index=True)
    team_def_df = pd.concat(team_def_rows, ignore_index=True)
    team_mid_df = pd.concat(team_mid_rows, ignore_index=True)
    team_fwd_df = pd.concat(team_fwd_rows, ignore_index=True)

    team_df = pd.concat([team_gk_df, team_def_df, team_mid_df, team_fwd_df], ignore_index=True, sort=False)
    Na_cols = team_df.columns[team_df.isna().any()].tolist()
    Int_cols = ["CS", "Goals Conceded", "Saves", "Form", "G", "A"]
    for col in Na_cols:
        team_df[col] = team_df[col].replace({np.nan: 0})
        if col in Int_cols:
            team_df[col] = team_df[col].astype(int)

    team_season = wb["My Team - Season"]

    for col, header in enumerate(team_df.columns, start=1):
        team_season.cell(row=1, column=col, value=header)
    for row, value in enumerate(team_df.values, start=2):
        for col, cell in enumerate(value, start=1):
            team_season.cell(row=row, column=col, value=cell)

    wb.save(EXCEL_FILE)
    print("Finished updating my team - season")
#region System arguments
if __name__ == "__main__":  
    if(sys.argv[1] == "update_teams"):
        update_teams()
    elif(sys.argv[1] == "update_fixture"):
        update_fixture()
    elif(sys.argv[1] == "show_summary"):
        show_summary()
    elif(sys.argv[1] == "update_player_season"):
        update_player_season()  
    elif(sys.argv[1] == "update_player_last5"):
        update_player_last5()
    elif(sys.argv[1] == "update_my_team"):
        update_my_team()   
