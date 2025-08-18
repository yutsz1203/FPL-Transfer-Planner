# Project next game week and next 5 gameweeks using current season stats and last 5 games stats

# Table schema: Name, Pos, Team, Cost, Expected returns (xGI * O_Di), Expected goal concede, opponents
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from const import team_ids, team_id_map

def get_next_gameweek(fixtures, player_df, team_df, type, gw, side_adjustment=True):
    gw = f"GW{gw}"
    print(f"Projecting {gw} for all players using {type} stats...")
    print("*" * 90)

    player_df["xGI/Game"] = player_df["xGI"] / player_df["Games"]
    player_df["xGc/Game"] = player_df["xGc"] / player_df["Games"]
    player_df["h_xGI/Game"] = player_df["h_xGI"] / player_df["h_Games"]
    player_df["h_xGc/Game"] = player_df["h_xGc"] / player_df["h_Games"]
    player_df["a_xGI/Game"] = player_df["a_xGI"] / player_df["a_Games"]
    player_df["a_xGc/Game"] = player_df["a_xGc"] / player_df["a_Games"]


    player_df = player_df[["Player ID", "Name", "Pos", "Team", "Cost", "xGI/Game", "xGc/Game", "h_xGI/Game", "h_xGc/Game", "a_xGI/Game", "a_xGc/Game"]]
    players = player_df.to_dict(orient="records")

    for player in players:
        team_name = player["Team"]
        opponent = fixtures[fixtures["team"] == team_name][gw].values[0][:-3]
        side = fixtures[fixtures["team"] == team_name][gw].values[0][-2]

        if side_adjustment:
            if side == "H":
                xGI = player["h_xGI/Game"]
                xGc = player["h_xGc/Game"]
                team_Oi = team_df[team_df["team"] == team_name]["h_Oi"].values[0]
                team_Di = team_df[team_df["team"] == team_name]["h_Di"].values[0]
                opponent_Oi = team_df[team_df["team"] == opponent]["a_Oi"].values[0]
                opponent_Di = team_df[team_df["team"] == opponent]["a_Di"].values[0]
            else:
                xGI = player["a_xGI/Game"]
                xGc = player["a_xGc/Game"]
                team_Oi = team_df[team_df["team"] == team_name]["a_Oi"].values[0]
                team_Di = team_df[team_df["team"] == team_name]["a_Di"].values[0]
                opponent_Oi = team_df[team_df["team"] == opponent]["h_Oi"].values[0]
                opponent_Di = team_df[team_df["team"] == opponent]["h_Di"].values[0]
        else:
            xGI = player["xGI/Game"]
            xGc = player["xGc/Game"]
            team_Oi = team_df[team_df["team"] == team_name]["Oi"].values[0]
            team_Di = team_df[team_df["team"] == team_name]["Di"].values[0]
            opponent_Oi = team_df[team_df["team"] == opponent]["Oi"].values[0]
            opponent_Di = team_df[team_df["team"] == opponent]["Di"].values[0]

        player["opponent"] = opponent
        player["team_Oi"] = team_Oi
        player["team_Di"] = team_Di
        player["opponent_Oi"] = opponent_Oi
        player["opponent_Di"] = opponent_Di
        player["xGI"] = xGI
        player["projected GI"] = round(xGI * opponent_Di, 2)
        player["xGc"] = xGc
        player["projected Gc"] = round(xGc * opponent_Oi, 2)

    next_gameweek_df = pd.DataFrame(players)
    next_gameweek_df = next_gameweek_df.drop(columns=["xGI/Game", "xGc/Game", "h_xGI/Game", "h_xGc/Game", "a_xGI/Game", "a_xGc/Game"])
    next_gameweek_df["projected net goals"] = round(next_gameweek_df["projected GI"] - next_gameweek_df["projected Gc"], 2)
    next_gameweek_df = next_gameweek_df.reindex(columns=["Player ID", "Name", "Pos", "Team", "Cost", "opponent", "team_Oi", "opponent_Di", "xGI", "projected GI", "team_Di", "opponent_Oi", "xGc", "projected Gc", "projected net goals"])
    next_gameweek_df.sort_values(by=["projected GI"], ascending=False, inplace=True)
    next_gameweek_df.to_csv(f"players/projection/next_gameweek_{type}.csv", index=False)
    print(next_gameweek_df)

# Uncomment to get the next gameweek opponents
# get_next_gameweek(last_season_strengths, "last_season")

def get_next_n_gameweek(fixtures, df, type, gw, side_adjustment=True, n=5):
    next_n_gameweek = []
    print(f"Projection gw{gw}-gw{gw+(n-1)} for all teams using {type} stats...")
    print("*" * 90)
    for team_id in team_ids:
        team_name = team_id_map[team_id]
        team_fixtures = fixtures[fixtures["team"] == team_name]
        nextn_gws = [team_fixtures[f"GW{i}"].values[0] for i in range(gw, gw + n)]
        opponents = []
        total_team_Oi, total_team_Di, total_opponents_Oi, total_opponents_Di, expected_gf, expected_ga = 0, 0, 0, 0, 0, 0
        for gw in nextn_gws:
            side = gw[-2]
            opponent = gw[:-3]
            opponents.append(f"({side[0]}) {opponent}")
            if side_adjustment:
                if side == "H":
                    print(f"H: {team_name} vs A: {opponent}")
                    total_team_Oi += df[df["team"] == team_name]["h_Oi"].values[0]
                    total_team_Di += df[df["team"] == team_name]["h_Di"].values[0]
                    total_opponents_Oi += df[df["team"] == opponent]["a_Oi"].values[0]
                    total_opponents_Di += df[df["team"] == opponent]["a_Di"].values[0]
                    expected_gf += round(df[df["team"] == team_name]["h_Oi"].values[0] * df[df["team"] == opponent]["a_Di"].values[0], 2)
                    expected_ga += round(df[df["team"] == team_name]["h_Di"].values[0] * df[df["team"] == opponent]["a_Oi"].values[0], 2)
                else:
                    print(f"H: {opponent} vs A: {team_name}")
                    total_team_Oi += df[df["team"] == team_name]["a_Oi"].values[0]
                    total_team_Di += df[df["team"] == team_name]["a_Di"].values[0]
                    total_opponents_Oi += df[df["team"] == opponent]["h_Oi"].values[0]
                    total_opponents_Di += df[df["team"] == opponent]["h_Di"].values[0]
                    expected_gf += round(df[df["team"] == team_name]["a_Oi"].values[0] * df[df["team"] == opponent]["h_Di"].values[0], 2)
                    expected_ga += round(df[df["team"] == team_name]["a_Di"].values[0] * df[df["team"] == opponent]["h_Oi"].values[0], 2)
            else:
                print("Without side adjustment:")
                print(f"H: {team_name} vs A: {opponent}") if side == "Home" else print(f"H: {opponent} vs A: {team_name}")
                total_team_Oi += df[df["team"] == team_name]["Oi"].values[0]
                total_team_Di = df[df["team"] == team_name]["Di"].values[0]
                total_opponents_Oi = df[df["team"] == opponent]["Oi"].values[0]
                total_opponents_Di = df[df["team"] == opponent]["Di"].values[0]
                expected_gf += round(df[df["team"] == team_name]["Oi"].values[0] * df[df["team"] == opponent]["Di"].values[0], 2)
                expected_ga += round(df[df["team"] == team_name]["Di"].values[0] * df[df["team"] == opponent]["Oi"].values[0], 2)
        next_n_gameweek.append({
            "team": team_name,
            "team_Oi": round(total_team_Oi,2),
            "team_Di": round(total_team_Di,2),
            "opponents_Oi": round(total_opponents_Oi,2),
            "opponents_Di": round(total_opponents_Di,2),
            "expected_gf": round(expected_gf, 2),
            "expected_ga": round(expected_ga, 2),
            "opponents": ", ".join(nextn_gws),
        })
        print(nextn_gws)
        print(f"Projected gw{gw}-gw{gw+(n-1)} gameweeks for {team_name}.")
        if team_name == "Wolves":
            print(f"Finished projecting next gw{gw}-gw{gw+(n-1)} gameweeks for all teams.")
        else:
            print("*" * 90)
        print("*" * 90)
    next_n_gameweek_df = pd.DataFrame(next_n_gameweek)
    next_n_gameweek_df.sort_values(by=["expected_gf"], ascending=False, inplace=True)
    next_n_gameweek_df.to_csv(f"teams/opponents/next_{n}_gameweek_{type}.csv", index=False)
    print(next_n_gameweek_df)

if __name__ == "__main__":
    fixtures = pd.read_csv("teams/data/fixtures.csv")

    # Current season
    team_current_season = pd.read_csv("teams/data/2526-prem-teams-currentseason.csv")
    player_current_season = pd.read_csv("players/results/player_season_stats.csv")

    # Last n games
    n = int(input("Please input n, number of previous games for calculation of player statistics: "))
    player_lastngames = pd.read_csv(f"players/results/player_last{n}games_stats.csv")

    # Augmented
    # augmented_strengths = pd.read_csv("teams/data/2526-prem-teams-augmented.csv")

    # Next week player projection
    gw = int(input("Enter the coming gameweek number: "))
    # current season strengths
    # change the last argument to true if want to adjust for home/away
    get_next_gameweek(fixtures, player_current_season, team_current_season, "currentseason", gw, False)

    # last 5 gameweeks strengths
    # get_next_gameweek(last5games_strengths, "last5games")

    # augmented strengths
    # get_next_gameweek(augmented_strengths, "augmented")

    # Next 5 weeks player projections

    # current season strengths
    # get_next_n_gameweek(fixtures, player_current_season, "currentseason", gw, False)

    # last 5 gameweeks strengths
    # get_next_5_gameweek(last5games_strengths, "last5games")

    # augmented strengths
    # get_next_5_gameweek(augmented_strengths, "augmented")