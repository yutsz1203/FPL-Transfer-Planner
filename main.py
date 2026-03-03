from teams.src.team_stats import team_stats
from prediction.src.predict import (
    predict,
    calc_accuracy,
    log_results,
    plot_calibration,
)
from utils import get_gameweek

if __name__ == "__main__":
    # print("Fetching team stats...")
    # team_stats()
    print("Performing prediction")
    predict()

    # print("Calculating accuracy of predictions...")
    # calc_accuracy()
    # print(get_gameweek("prev"))
    # print("Logging prediction results...")
    # log_results()

    # print("Plotting calibration curves...")
    # plot_calibration()
