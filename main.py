import apicalls
import nbaconstants
import pandas as pd
import datacleaning

if __name__ == '__main__':
    # df = api.get_player_stats('2022-23', 'Regular Season', '203999')
    # print(df)
    # TODO Add a toggle option for running this im pickling it to save
    # apicalls.get_active_player_data(nbaconstants.CURRENT_SEASON, nbaconstants.REGULAR_SEASON, True)
    # apicalls.get_active_player_data(nbaconstants.CURRENT_SEASON, nbaconstants.REGULAR_SEASON, False)
    df = apicalls.get_player_box()
    per36 = datacleaning.convert_per_36(df)
    print(per36)
    # df = pd.read_pickle("playerstatsdf")
    datacleaning.create_last_x(per36, "Donte DiVincenzo", 5)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
