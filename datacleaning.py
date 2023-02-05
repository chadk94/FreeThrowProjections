import pandas as pd


def convert_per_36(data):
    # converts data to per36 numbers,leaving minutes intact,also trims matchup to opponent
    columns_wanted = data[
        ['PLAYER_NAME', 'MATCHUP', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M',
         'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB',
         'REB', 'AST', 'PF', 'STL', 'TOV', 'BLK', 'PTS', 'PLUS_MINUS']]
    per36 = columns_wanted[['FGM', 'FGA', 'FG3M',
                           'FG3A', 'FTM', 'FTA', 'OREB', 'DREB',
                           'REB', 'AST', 'PF', 'STL', 'TOV', 'BLK', 'PTS', 'PLUS_MINUS']].div(columns_wanted.MIN,
                                                                                              axis=0) * 36
    frames = [columns_wanted[['PLAYER_NAME', 'MATCHUP', 'MIN', 'FG_PCT', 'FG3_PCT', 'FT_PCT']], per36]
    final_df = pd.concat(frames, axis=1)
    final_df['MATCHUP'] = final_df['MATCHUP'].str[-3:]
    return final_df


def create_last_x(data, player, x, y=0):
    # creates player averages for last x games from y games ago
    player_data = data.where(data['PLAYER_NAME'] == player).dropna(how="all")
    player_last_x = player_data.iloc[-x:-y]
    averages = player_last_x.mean()
    return averages


def create_season_avg(data, player, y=0):
    # creates player seasonal averages
    player_data = data.where(data['PLAYER_NAME'] == player).dropna(how="all")
    averages = player_data.iloc[-y].mean()
    return (averages)


def generate_x_y(data):  # todo fill out this formula, strip opposing team name from matchup
    # an eventual task to generate data points from player lst x and plyaer seasonal averages at the time of the game
    # y values are simply fta per 36
    if True:
        return
