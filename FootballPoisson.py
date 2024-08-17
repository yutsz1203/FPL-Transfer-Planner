import sys

import pandas as pd
from openpyxl import load_workbook

import requests
from bs4 import BeautifulSoup

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

    #update excel
    wb = load_workbook("FootballPoisson.xlsx")
    sheet = wb.active

    for row in range(2,22):
        team_name = sheet[f"A{row}"].value
        for team in teams:
            if team["Team"] == team_name:
                sheet[f"B{row}"] = sheet[f"B{row}"].value + team["GF"]
                sheet[f"C{row}"] = sheet[f"C{row}"].value + team["GA"]
                sheet[f"D{row}"] = sheet[f"D{row}"].value + 1


    
    wb.save("FootballPoisson.xlsx")

if __name__ == "__main__":  
    if(sys.argv[1] == "update"):
        update_data()