import pandas as pd
import numpy as np

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
    final_df['Home'] = final_df['MATCHUP'].str[-5]
    final_df['MATCHUP'] = final_df['MATCHUP'].str[-3:]
    final_df.loc[final_df['Home'] == "@", 'Home'] = False
    final_df.loc[final_df['Home'] == ".", 'Home'] = True
    final_df.replace([np.inf,-np.inf],0,inplace=True) #deal with edge case
    return final_df


def create_last_x(data, player, x, y=0):
    # creates player averages for last x games from y games ago
    player_data = data.where(data['PLAYER_NAME'] == player).dropna(how="all")
    if y != 0:
        player_data = player_data.iloc[:-y]  # remove y games
    player_last_x = player_data.iloc[-x:]  # take last x
    # averages = player_last_x.mean()
    averages = player_last_x.groupby('PLAYER_NAME').mean()
    averages = (averages.add_suffix('lastxgames'))
    return averages


def create_season_avg(data, player, y=0):
    # creates player seasonal averages
    player_data = data.where(data['PLAYER_NAME'] == player).dropna(how="all")
    if y != 0:
        player_data = player_data.iloc[:-y]  # remove y games

    averages = player_data.groupby('PLAYER_NAME').mean()
    return (averages)


def generate_x_y(data, lastx=5):
    # an eventual task to generate data points from player lst x and plyaer seasonal averages at the time of the game
    # y values are simply fta per 36
    column_names = data.columns
    x = pd.DataFrame()
    y = []
    playernamedict = {}
    for index, row in data.iterrows():  # go through each row, identify number of games played
        name = row['PLAYER_NAME']
        if name not in playernamedict:
            playernamedict.setdefault(name, 1)
        else:
            playernamedict[name] += 1
        minmatch=[row['MIN'], row['MATCHUP']]
        minmatch=pd.Series(minmatch,index=['MIN','MATCHUP'])
        playergames = len(data[data['PLAYER_NAME'] == name])  # totalnumber of games with player
        tempx = (create_last_x(data, name, lastx, playergames - playernamedict[name]))
        tempx = pd.concat([tempx, (create_season_avg(data, name, playergames - playernamedict[name]))],axis=1)
        tempx['MINTHISGAME']=row['MIN']
        tempx['MATCHUP']=row['MATCHUP']
        x=pd.concat([x,tempx],axis=0)
        y.append(row['FTA'])
        tempx=tempx.iloc[0:0]
    x = pd.DataFrame(x)
    return x, y

def buildplayer(data,Name,matchup,x): #TODO INTROUCE HOME/away
    lastx= create_last_x(data,player=Name,x=x)
    season=create_season_avg(data,Name)
    season['MINTHISGAME']=lastx['MINlastxgames']
    dummies = pd.get_dummies(data['MATCHUP'])
    dummies.iloc[:]=0
    X = data.drop('MATCHUP', axis=1)
    X = pd.concat([lastx, season, dummies], axis=1)
    X = X.drop(['FT_PCTlastxgames', 'FG_PCTlastxgames', 'FG3_PCTlastxgames', 'FG_PCT', 'FG3_PCT', 'FT_PCT'], axis=1)
    X = X.fillna(0)
    X[matchup]=1
    player=X.iloc[0]
    return player