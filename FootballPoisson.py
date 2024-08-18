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

    team_dict = {team["Team"]: team for team in teams}
    #update excel
    wb = load_workbook("FootballPoisson.xlsx")
    sheet = wb["Team Data"]

    for row in range(2,22):
        team_name = sheet[f"A{row}"].value
        if team_name in team_dict:
            team = team_dict[team_name]
            sheet[f"B{row}"] = sheet[f"B{row}"].value + team["GF"]
            sheet[f"B{row}"].font = DEFAULT_FONT
            sheet[f"C{row}"] = sheet[f"C{row}"].value + team["GA"]
            sheet[f"C{row}"].font = DEFAULT_FONT
            sheet[f"D{row}"] = sheet[f"D{row}"].value + 1
            sheet[f"D{row}"].font = DEFAULT_FONT
    
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
    wb = load_workbook("FootballPoisson.xlsx")
    sheet = wb["Fixtures"]

    for col, gameweek in enumerate(gameweeks, start=2):
        cell = sheet.cell(row=1, column=col, value=gameweek)
        cell.font = DEFAULT_FONT_BOLD

    for row in range (2,22):
        sheet[f"A{row}"] = fixtures[row-2]["Team"]
        sheet[f"A{row}"].font = DEFAULT_FONT_BOLD
        for col, opponent in enumerate(fixtures[row - 2]["Next 5"], start=2):
            cell = sheet.cell(row=row, column=col, value=opponent)
            cell.font = DEFAULT_FONT
    print("Finished updating excel.")

    wb.save("FootballPoisson.xlsx")

if __name__ == "__main__":  
    if(sys.argv[1] == "update_data"):
        update_data()
    elif(sys.argv[1] == "update_fixture"):
        update_fixture()