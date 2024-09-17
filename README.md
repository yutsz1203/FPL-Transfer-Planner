# FPL Transfer Planner

## Description

This program extracts Premier League data from [fpl.page](https://fpl.page) and **official FPL API** for assiting in planning transfers for FPL.

The program focus on getting data for the following time frames:

1. Current GW
2. Next GW
3. Last 5 GWs
4. Future 5 GWs
5. Season

Each time frame collects:

1. Teams Data
2. Fixtures / Results
3. Players Data
4. My FPL Team

## Data Calculation

### Teams Data

#### Mean Variable in the League $LOd$

$LOd = \text{Total Goals} / \text{Total Games Played}$

#### Offensive Strength of team i: $O_i$

$O_i = \text{Avg. GF} / LOd$

High $O_i$ means the team is likely to score more goals than other teams in the league.

- Good team has high $O_i$
- Bad team has low $O_i$

#### Defensive Strength of team i: $D_i$

$D_i = \text{Avg. GA} / LOd$

High $D_i$ means the team is likely to concede more goals than other teams in the league.

- Good team has low $D_i$
- Bad team has high $D_i$

### Fixtures / Results

$X, Y$ are two teams.

Team X has offensive strength of $O_x$ and defensive strength of $D_x$.

Team Y has offensive strength of $O_y$ and defensive strength of $D_y$.

Probability of team $X$ scoring $n$ goals $= \text{POISSON}(n, O_x * D_y * LOd)$

Probability of team $Y$ scoring $n$ goals $= \text{POISSON}(n, O_y * D_x * LOd)$

Suppose $LOd = 1.1$ Chelsea has $O_c$ of $2.5$, $D_c$ of $0.5$, Man U has $O_m$ of $1.4$, $D_m$ of $1.2$

- the probability of Chelsea scoring 0 goals is $\text{POISSON}(0, 2.5 * 1.2 * 1.1)$
- the probability of Man U scoring 0 goals is $\text{POISSON}(0, 1.4 * 0.5 * 1.1)$

### Players Data

#### GK

$\text{xG Prevented} = \text{xG Conceded} - \text{Goals Conceded}$

- Positive xG Prevented = Good GK

$\text{Projected Performance} = O_j * D_i * LOd - \text{xG Prevented}$,

where $O_j$ is the offensive strength of opponent, and $D_i$ is the defensive strength of the GK's team

#### DEF

$\text{Projected Performance} =  \text{xGI} * D_j * LOd - (O_j * D_i * LOd)$

#### MID, FWD

$\text{Projected Performance} =  \text{xGI} * D_j * LOd$

## Running the program

1. `$ pip install -r requirements.txt`
2. `$ python FootballPoisson.py`
3. choose timeframe
   1. Current GW
   2. Next GW
   3. Last 5 GWs
   4. Next 5 GWs
   5. Season
4. choose data
   1. Teams data
   2. Fixtures / Results
   3. Players data
   4. My FPL Team

### Update procedure

- 1.5 Get new players and add to season report
- 5.1 Season Teams
- 5.2 Season Players
- 5.3 Season MyTeam
- 4.2 Next 5 Fixtures
- 4.3 Next 5 Players
- 4.4 Next 5 MyTeam

## Features to work on

### Current GW

1. Player data
2. GW Result
3. My team

### Next GW

1. Fixture / Results

- Fetch odds from HKJC

### Last 5 GW

1. Teams data
2. Results

### All

1. Summary

### Others

FDR and coloring

## References

- [FPL API guide](https://www.game-change.co.uk/2023/02/10/a-complete-guide-to-the-fantasy-premier-league-fpl-api/)
- [Match Prediction Poisson Model](https://www.jhse.ua.es/article/view/2021-v16-n4-poisson-model-goal-prediction-european-football/remote)
