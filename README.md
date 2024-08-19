# FootballPoisson

## Description

This program extracts Premier League data from [fpl.page](https://fpl.page) (thanks to FPL Focal) for assiting me in planning my transfers in Fantasy Premier League (FPL). It currently extracts (1) Gameweek Data (Goal for, Goal against) and (2) Fixture Data (future 5 gws).

### (1) Gameweek Data

The gameweek data is for calculating the Offensive Strength (Oi) and Defensive Strength (Di) of each team, and then predict the results of each match using a Poisson Predictive model.

### (2) Fixture Data

The fixture data provides the next 5 opponents of each team. Then, total Oi and total Di will be calculated. Teams that have opponents with the largest aggregated Di is favourable for attackes, and teams that have oponents with the smallest aggregated Oi is favourable for defenders.

## Running the program

Pass the following arguments to get respective data

### (1) Gameweek Data

`$update_data`

### (2) Fixture Data

`$update_fixture`

## Features to work on

- Expected Data of players
