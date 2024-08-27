import sys

import pandas as pd
import requests
from bs4 import BeautifulSoup
from openpyxl import load_workbook
from openpyxl.styles import Font
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

DEFAULT_FONT = Font(size=16)
DEFAULT_FONT_BOLD = Font(size=16, bold=True)

def update_data():
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
            
            teams.append({"Team": home_team, "GF": scores[0], "GA": scores[1]})
            teams.append({"Team": away_team, "GF": scores[1], "GA": scores[0]})

    print("Finished getting gameweek data")
    #update excel
    wb = load_workbook("FootballPoisson.xlsx")
    sheet = wb["Team Data"]

    df = pd.read_excel("FootballPoisson.xlsx", sheet_name="Team Data", usecols="A:H", header=0, nrows=20, dtype={"Team": str, "GF": int, "GA": int, "Games": int, "Avg.GF": float, "Avg.GA": float, "Oi": float, "Di": float})
    for team in teams:
        team_name = team["Team"]
        team_row = df.index[df["Team"] == team_name].tolist()[0]
        df.loc[team_row, "GF"] = df.loc[team_row, "GF"] + team["GF"]
        df.loc[team_row, "GA"] = df.loc[team_row, "GA"] + team["GA"]
        df.loc[team_row, "Games"] += 1
        df.loc[team_row, "Avg.GF"] = df.loc[team_row, "GF"] / df.loc[team_row, "Games"]
        df.loc[team_row, "Avg.GA"] = df.loc[team_row, "GA"] / df.loc[team_row, "Games"]
    lod = df["GF"].sum() / df["Games"].sum()
    df["Oi"] = df["Avg.GF"] / lod
    df["Di"] = df["Avg.GA"] / lod
    
    df["Avg.GF"] = df["Avg.GF"].round(2)
    df["Avg.GA"] = df["Avg.GA"].round(2)
    df["Oi"] = df["Oi"].round(2)
    df["Di"] = df["Di"].round(2)

    sheet["B23"] = df["GF"].sum()
    sheet["C23"] = df["GA"].sum()
    sheet["D23"] = df["Games"].sum()
    sheet["E23"] = df["Avg.GF"].mean()
    sheet["F23"] = df["Avg.GA"].mean()
    sheet["G23"] = df["Oi"].mean()
    sheet["H23"] = df["Di"].mean()

    sheet["B24"] = lod
    top_attacking = df.sort_values(by=["Oi"], ascending=False)["Team"].head(5).tolist()
    top_defending = df.sort_values(by=["Di"], ascending=True)["Team"].head(5).tolist()

    top_attacking.sort()
    top_defending.sort()

    columns = ["B", "C", "D", "E", "F"]

    for i, col in enumerate(columns):
        sheet[f"{col}26"] = top_attacking[i]
        sheet[f"{col}27"] = top_defending[i]

    for r_idx, row in enumerate(df.values, start=2):
        for c_idx, value in enumerate(row, start=1):
            sheet.cell(row=r_idx, column=c_idx, value=value)

    print("Finished updating team gameweek data.")    
    wb.save("FootballPoisson.xlsx")

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
    wb = load_workbook("FootballPoisson.xlsx", data_only=True)
    sheet = wb["Fixtures"]

    for col, gameweek in enumerate(gameweeks, start=2):
        cell = sheet.cell(row=1, column=col, value=gameweek)
        cell.font = DEFAULT_FONT_BOLD

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
    team_data_sheet = wb["Team Data"]
    for row in range (2,22):
        sheet[f"A{row}"] = fixtures[row-2]["Team"]
        sheet[f"A{row}"].font = DEFAULT_FONT_BOLD
        for col, opponent in enumerate(fixtures[row - 2]["Next 5"], start=2):
            #filling in opponents
            cell = sheet.cell(row=row, column=col, value=opponent)
            cell.font = DEFAULT_FONT

            #aggregating Oi and Di
            cleaned_opponent = opponent.split(" ")[0]
            team_row = team_map[cleaned_opponent]

            sheet[f"G{row}"] = sheet[f"G{row}"].value + team_data_sheet[f"G{team_row}"].value
            sheet[f"H{row}"] = sheet[f"H{row}"].value + team_data_sheet[f"H{team_row}"].value
    wb.save("FootballPoisson.xlsx")
    df = pd.read_excel("FootballPoisson.xlsx", sheet_name="Fixtures", usecols="G:H", header=0, nrows=20, dtype={"Oi": float, "Di": float})

    sheet["G22"].value = df["Oi"].mean()
    sheet["H22"].value = df["Di"].mean()
    
    low_oi_index = df.sort_values(by=["Oi"], ascending=True)["Oi"].head(5).index.tolist()
    high_di_index = df.sort_values(by=["Di"], ascending=False)["Di"].head(5).index.tolist()

    low_oi_index.sort()
    high_di_index.sort()
    for col, (low_oi_idx, high_di_idx) in enumerate(zip(low_oi_index, high_di_index), start=2):
        sheet.cell(row=24, column=col, value=sheet[f"A{high_di_idx + 2}"].value)
        sheet.cell(row=25, column=col, value=sheet[f"A{low_oi_idx + 2}"].value)

    print("Finished updating fixture data.")

    wb.save("FootballPoisson.xlsx")

if __name__ == "__main__":  
    if(sys.argv[1] == "update_data"):
        update_data()
    elif(sys.argv[1] == "update_fixture"):
        update_fixture()