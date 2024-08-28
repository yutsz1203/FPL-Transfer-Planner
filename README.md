# FootballPoisson

## Description

This program extracts Premier League data from [fpl.page](https://fpl.page) (thanks to FPL Focal) for assiting me in planning my transfers in Fantasy Premier League (FPL). It currently extracts (1) Gameweek Data (Goal for, Goal against) and (2) Fixture Data (future 5 gws).

### (1) Gameweek Data

The gameweek data is for calculating the Offensive Strength (Oi) and Defensive Strength (Di) of each team, and then predict the results of each match using a Poisson Predictive model.

### (2) Fixture Data

The fixture data provides the next 5 opponents of each team. Then, total Oi and total Di will be calculated. Teams that have opponents with the largest aggregated Di is favourable for attackes, and teams that have oponents with the smallest aggregated Oi is favourable for defenders.

### (3) Show summary

Showing summary of all the data gathered from the program, including (1) Gameweek Data (2) Fixture Data

## Running the program

Pass the following arguments to get respective data

### (1) Gameweek Data

`$ update_data`

### (2) Fixture Data

`$ update_fixture`

### (3) Show summary

`$ show_summary`

## Features to work on

### team data

- color lowest/highest oi & di
- Provide Home / Away data separately

### fixture data

- Colour fixture cells based on opponent's strength in offense and defense (two versions for attackers and defenders), separate teams in 5 different categories, 4 teams a group.

### fdr

- Create a sheet that displays fdr for attackers, and fdr for defenders

### fpl api
