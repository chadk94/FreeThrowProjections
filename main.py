import apicalls
import nbaconstants

if __name__ == '__main__':
    # df = api.get_player_stats('2022-23', 'Regular Season', '203999')
    # print(df)
    #TODO Add a toggle option for running this im pickling it to save
    apicalls.get_active_player_data(nbaconstants.CURRENT_SEASON, nbaconstants.REGULAR_SEASON, True)
    # api.get_active_player_data(constants.CURRENT_SEASON, constants.REGULAR_SEASON, False)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
