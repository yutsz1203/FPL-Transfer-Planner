# FootballPoisson

## Description

This program extracts Premier League data from [fpl.page](https://fpl.page) (thanks to FPL Focal) for assiting me in planning my transfers in Fantasy Premier League (FPL). It currently extracts (a) Gameweek Data (Goal for, Goal against),(b) Fixture Data (future 5 gws), (c) Player Data , (d) My Fantasy Team, and (e) Summary .

I focus on getting data of the following time frames:

1. Current GW
2. Next GW
3. Last 5 GW
4. Future 5 GW
5. Season

### (a) Gameweek Data

The gameweek data is for calculating the Offensive Strength (Oi) and Defensive Strength (Di) of each team, separated by Home and Away, and then predict the results of each match using a Poisson Predictive model.

### (b) Fixture Data

The fixture data provides the next 5 opponents of each team. Then, total Oi and total Di will be calculated. Teams that have opponents with the largest aggregated Di is favourable for attackes, and teams that have oponents with the smallest aggregated Oi is favourable for defenders.

### (c) Player Data

It extracts all players data (for those who played more than one match) and write to excel.
It is separated by position:

1. GK
   It tracks "Name", "Team", "Price", "GW Points", "Total Points", "Points/$", "CS", "Goals Conceded", "xG Conceded", "xGoals Prevented", "Saves", "Bonus"

2. Outfield players: DEF, MID, FWD
   It tracks "Name", "Team", "Price", "Form", "GW Points", "Total Points", "Points/$", "xG", "G", "xG+-","xA", "A", "xA+-", "xGI", "Bonus".

### (d) My FPL Team

Showing data of players in my FPL Team.

### (e) Show summary

Showing summary of all the data gathered from the program, including (1) Gameweek Data (2) Fixture Data

## Data Provided

### 1. Current GW

- (b) Results
- (c) Player Data
- (d) My FPL Team
- (e) Summary

### 2. Next GW

- (b) Fixture
- (c) Player Data
- (d) My FPL Team

### 3. Last 5 GW

- (a) Team Data
- (b) Results
- (c) Player Data
- (d) My FPL Team
- (e) Summary

### 4. Next 5 GW

- (b) Fixtures
- (c) Player Data
- (d) My FPL Team
- (e) Summary

### 5. Season

- (a) Team Data
- (c) Player Data
- (d) My FPL Team
- (e) Summary

## Running the program

1. Update Season Data (5)
2. Update next 5 fixtures (4, 1)
3. Update desired data range.

## Features to work on

2. get all players past 5 gw records (update player)
3. calculate players projected goals and assists by using their expected data, and opponent's offensive and defensive strength
4. get my team past 5 gw records (update_my_team)
5. Colour fixture cells based on opponent's strength in offense and defense (two versions for attackers and defenders), separate teams in 5 different categories, 4 teams a group (fixture data)
6. Create a sheet that displays fdr for attackers, and fdr for defenderss (fdr)
7. (1) show players with best points / $, per position (2) allow user to choose what summary to print (summary)
