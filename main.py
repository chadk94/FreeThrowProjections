import apicalls
import nbaconstants
import pandas as pd
import datacleaning
import ppscrape
import model
import numpy as np

if __name__ == '__main__':
    # lines = ppscrape.GetLines()
    df = apicalls.get_player_box()
    per36 = datacleaning.convert_per_36(df)
    # print(per36)
    # df = pd.read_pickle("playerstatsdf")
    # print(datacleaning.create_last_x(per36, "Donte DiVincenzo", 5))
    # print (datacleaning.create_season_avg(per36,"Donte DiVincenzo"))
    x, y = datacleaning.generate_x_y(per36)  # Run to generate model TODO SAVE MODEL
    #model1 = model.create_model(x, y)  # same here
    #print(model1.coef_)
    finalmodel = model.propbet(x, y)
    player = (datacleaning.buildplayer(per36, "Bennedict Mathurin","CLE", 5)) #todo add home/away
    player = np.array(player)
    player = player.reshape(1,-1)
    print (player)
    model.predictandpoisson(player, 70,finalmodel, 2.5) #todo incorporate rigoruos pull and parse

# See PyCnharm help at https://www.jetbrains.com/help/pycharm/
