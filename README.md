# FPL Transfer Planner

Fantasy Premier League (FPL) is the official fantasy football game of the English Premier League (EPL). Currently, there are around 12 million players worldwide.

FPL Transfer Planner is a tool that automates data extraction and processing of match and player statistics from the EPL for actionable insights and player selection optimisation in FPL.

## Table of Contents

- [Description](#description)
  - [Teams](#1-teams)
    - [Statistics](#team-statistics)
    - [Projection](#team-projection)
  - [Players](#2-players)
    - [Statistics](#player-statistics)
    - [Projection](#player-projection)
  - [User's FPL Team](#3-users-fpl-team)
    - [Statistics](#users-fpl-team-statistics)
    - [Projection](#users-fpl-team-projection)
- [Getting Started](#getting-started)
  - [Dependencies](#dependencies)
  - [Usage](#usage)
    - [Update fixtures](#update-fixtures)
    - [Update players](#update-players)
    - [Calculate teams' strengths](#calculate-teams-strengths)
    - [Project teams' performances](#project-teams-performances)
    - [Calculate players' statistics](#calculate-players-statistics)
    - [Project players' performances](#project-players-performances)
    - [Evaluate your FPL team](#evaluate-your-fpl-team)
- [References and APIs](#references-and-apis)

## Description

The planner extracts and processes data of 3 main parties: Teams, Players, and the user's FPL team. For each party, the planner focuses on the statistics from past gameweeks and projections for future gameweeks. The planner calculates the statistics based on different time interval, such as all gameweeks in current season, and past 5 gameweeks only.

### 1. Teams

The planner measures each teams' "strength" and make projection based on it. The calculations are as follows.

- Offensive strength: $O_i = \text{Avg. GF} / LOd$
  - High $O_i$ means the team is likely to score more goals than other teams in the league.
- Defensive strength: $D_i = \text{Avg. GA} / LOd$
  - High $D_i$ means the team is likely to concede more goals than other teams in the league.

where

- $\text{Avg. GF} = \text{Goals For} / \text{Total Games Played for each team}$
- $\text{Avg. GA} = \text{Goals Against} / \text{Total Games Played for each team}$
- $LOd = \text{Total Goals} / \text{Total Games Played in the League}$

#### Team Statistics

Teams' statistics of current season and past 5 games are calculated and located in `teams/results`. Key metrics: Oi, Di.

#### Team Projection

Teams' performance in the future 1 and 5 gameweeks are projected based on the Oi and Di and teams and their opponents. It is located in `teams/projection`. Key metrics: Expected GF, Expected GA.

### 2. Players

#### Player Statistics

Players' statistics of current season and past 5 games are calculated and located in `players/results`. Key metrics: xGI, Points/$.

#### Player Projection

Players' performance in the future 1 and 5 gameweeks are projected based on their xGI, and Di of their opponents. It is located in `players/projection`

### 3. User's FPL team

The planner lets the user to view statistics and projection for the players in their own FPL team for evaluations.

#### User's FPL team Statistics

It is located in `myteam/results`.

#### User's FPL team Projection

It is located in `myteam/projection`.

## Getting Started

### Dependencies

Use the package manager pip to install the dependencies for this project.

`$ pip install -r requirements.txt`

### Usage

#### Update fixtures

Due to mid-week cup matches and various reason that leads to postponements (e.g. bad weather), PL games may be rearranged. It leads to the occurences of what we called Blank Gameweek (BGW) or Double Gameweek (DGW). Therefore, we need to update the fixtures for each team before proceeding.

`$ python teams/get_fixtures.py`

The fixture list for each team: stored at `teams/data/fixtures.csv`.

#### Update players

There may be new players in every gameweek, such as new signings and/or players promoted from the u-teams. Therefore, we need to update the player list as well.

`$ python players/generate_df/get_players.py`

The player list: stored at `players/data/players.csv`

#### Calculate teams' strengths

`$ python teams/generate_df/team_strengths.py`

Prompts:

`Enter gameweek number: `

- Enter the current gameweek number

`Enter number of last n gameweeks to include in calculation: `

- Enter number of gameweeks to include in calculation. It is recommended to use 5. (n must not be greater than current gameweek number).

Team strength of current season: stored at `teams/results/teams_currentseason.csv`

Team strength of last n gameweeks: stored at `teams/results/teams_last{n}games.csv`

#### Project teams' performances

`$ python teams/fixture_projection.py`

Prompts:

`Enter the coming gameweek number:  `

- Enter the upcoming gameweek's number.
- This prompt will appear twice. They are for the fixture projection for next and next 5 gameweeks respectively.

Fixture projection for next gameweek: stored at `teams/projection/teams_next_gameweek_currentseason.csv`

Fixture projection for next 5 gameweeks: stored at `teams/projection/teams_next5gameweeks_currentseason.csv`

#### Calculate players' statistics

`$ python players/generate_df/player_stats.py`

Prompts:

`Enter current gameweek number: `

- Enter the current gameweek number

`Enter number of last n gameweeks to include in calculation: `

- Enter number of gameweeks to include in calculation. It is recommended to use 5. (n must not be greater than current gameweek number).

Player statistics of current season: stored at `players/results/players_currentseason.csv`

Player statistics of last n games: stored at `players/results/players_last{n}games.csv`

#### Project players' performances

`$ python players/player_projection.py`

Prompts:

`"Please input n, number of previous games for calculation of player statistics: "`

- Use the same n as here: `players/results/players_last{n}games.csv`

`Enter the coming gameweek number:`

- Enter the upcoming gameweek's number.

Player projection for next gameweek: stored at `players/projection/players_next_gameweek_currentseason.csv`

Fixture projection for next 5 gameweeks: stored at `players/projection/players_next5gameweeks_currentseason.csv`

#### Evaluate your FPL team

Individual player statistics

`$ python myteam/myteam_stats.py`

Prompts:

`Enter current gameweek number: `

- Enter current gameweek number.

`Enter n, the number of gameweeks used in calculation: `

- Use the same n as here: `players/results/players_last{n}games.csv`

Your FPL team's individual player statistics: stored at `new_ver/myteam/results/myteam_currentseason_stats.csv` and `new_ver/myteam/results/myteam_last{n}games_stats.csv`

Player performance projection

`$ python myteam/myteam_projection.py`

Prompts:

`Enter current gameweek number: `

- Enter current gameweek number.

`Enter n, number of gameweek used in projection:`

- Use the same n as here: `players/results/players_last{n}games.csv`

Your FPL team's projection: stored at `new_ver/myteam/projection/myteam_nextgw_projection_currentseason.csv` and `new_ver/myteam/projection/myteam_next5gws_currentseason.csv`

## References and APIs

- fbref api: https://fbrapi.com/documentation
- official api: https://fantasy.premierleague.com/api/
- official api guide: https://www.oliverlooney.com/blogs/FPL-APIs-Explained#how-to-use-authenticated-endpoints
