import pandas as pd
import time
from nba_api.stats.endpoints import cumestatsplayer, cumestatsplayergames, commonplayerinfo
from nba_api.stats.static import players
from nba_api.stats.endpoints import boxscoretraditionalv2
from nba_api.stats.endpoints import LeagueGameLog
import nbaconstants


def get_player_box():
    # returns all player box scors or the season
    playerbox = LeagueGameLog(player_or_team_abbreviation='P').get_data_frames()[0]
    return playerbox


# Returns a list of active player id's
def get_active_player_ids():
    active_players_list = players.get_active_players()
    ids_active_players = []

    for player in active_players_list:
        ids_active_players.append(player['id'])

    return ids_active_players


# Returns dataframe of active player stats. "last_ten" is a boolean to either
# look at last 10 games (true) or entire season (false).
def get_active_player_data(season, season_type, last_ten):
    ids_active_players = get_active_player_ids()
    df_player_stats = pd.DataFrame()

    time.sleep(1)

    counter = 1
    for active_player_id in ids_active_players:
        # Pulls and prints out common player data like College, Roster Status, Position, Birthdate,
        # Team Abbreviation, etc. This code can be moved to another function.
        # player_info = commonplayerinfo.CommonPlayerInfo(player_id).common_player_info.get_dict()
        # p_columns = player_info['headers']
        # p_rows = player_info['data'][0]
        # p_data = dict(zip(p_columns, p_rows))
        # print(p_data)

        # Collects a dict of player data for the sole purpose of identifying game_id's.
        # This could probably be optimized.
        while True:
            try:
                p_games = cumestatsplayergames.CumeStatsPlayerGames(
                    active_player_id,
                    league_id='00',
                    season=season,
                    season_type_all_star=season_type
                ).cume_stats_player_games.get_dict()['data']
            except:
                p_games = []
                print('FAILED pulling game info for ' + str(active_player_id) + ' Pausing and Trying again')
                time.sleep(2)
                continue
            break

        # Code block creates a string of game_id's in proper format: '0022200047|0022200030|0022200022'
        game_ids = ''
        if last_ten and len(p_games) >= 10:
            length = len(p_games)
            p_games_last_ten = p_games[length - 10: length: 1]
            for game in p_games_last_ten:
                game_ids += game[1] + '|'
        else:
            for game in p_games:
                game_ids += game[1] + '|'
        game_ids = game_ids[:len(game_ids) - 1]

        # print('game ids located for ' + str(active_player_id))
        while True:
            try:
                p_stats = cumestatsplayer.CumeStatsPlayer(active_player_id, game_ids, league_id='00',
                                                          season=season).total_player_stats.get_data_frame()
            except:
                p_stats = pd.DataFrame()
                print('FAILED pulling stats for ' + str(active_player_id) + ' pausing 2 seconds and trying again')
                time.sleep(2)
                continue
            break

        df_player_stats = pd.concat([df_player_stats, p_stats], axis=0, ignore_index=True)

        # print(df_player_stats)
        if counter % 10 or counter == 1:
            print('Completed ' + str(counter) + '/' + str(len(ids_active_players)) + ' players')

        counter += 1
        time.sleep(0.2)
    filename = "playerstatsdf"
    if last_ten == True:
        filename += "last_ten"
    df_player_stats.to_pickle("playerstatsdf")
    print(df_player_stats)
