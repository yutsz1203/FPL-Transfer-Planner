# FootballPoisson

## Description

This program extracts Premier League data from [fpl.page](https://fpl.page) (thanks to FPL Focal) for assiting me in planning my transfers in Fantasy Premier League (FPL). It currently extracts (1) Gameweek Data (Goal for, Goal against) and (2) Fixture Data (future 5 gws) (4) Player Data.

### (1) Gameweek Data

The gameweek data is for calculating the Offensive Strength (Oi) and Defensive Strength (Di) of each team, and then predict the results of each match using a Poisson Predictive model.

### (2) Fixture Data

The fixture data provides the next 5 opponents of each team. Then, total Oi and total Di will be calculated. Teams that have opponents with the largest aggregated Di is favourable for attackes, and teams that have oponents with the smallest aggregated Oi is favourable for defenders.

### (3) Player Data

It extracts all players data (for those who played more than one match) and write to excel.
It is separated by position:

1. GK
   It tracks "Name", "Team", "Price", "GW Points", "Total Points", "Points/$", "CS", "Goals Conceded", "xG Conceded", "xGoals Prevented", "Saves", "Bonus"

2. Outfield players: DEF, MID, FWD
   It tracks "Name", "Team", "Price", "Form", "GW Points", "Total Points", "Points/$", "xG", "G", "xG+-","xA", "A", "xA+-", "xGI", "Bonus".

### (4) Show summary

Showing summary of all the data gathered from the program, including (1) Gameweek Data (2) Fixture Data

## Running the program

Pass the following arguments to get respective data

### (1) Gameweek Data

`$ update_data`

### (2) Fixture Data

`$ update_fixture`

### (3) Player Data

`$ update_player`

### (4) Show summary

`$ show_summary`

## Features to work on

### team data

- Provide Home / Away data separately

### fixture data

- Colour fixture cells based on opponent's strength in offense and defense (two versions for attackers and defenders), separate teams in 5 different categories, 4 teams a group.

### fdr

- Create a sheet that displays fdr for attackers, and fdr for defenders

### update player

- get all players past 5 gw records

### update team

- get team past 5 gw records

### summary

- show players with best points / $, per position
- allow user to choose what summary to print

### projected goals, assists

- calculate players projected goals and assists by using their expected data, and opponent's offensive and defensive strength
