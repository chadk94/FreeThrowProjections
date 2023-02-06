import apicalls
import nbaconstants
import pandas as pd
import datacleaning
import ppscrape
import model
import numpy as np
import pickle

if __name__ == '__main__':
  #  lines = ppscrape.GetLines()
    lines=pd.DataFrame([["Julius Randle","5.5", "PHI"],["Joel Embiid","9.5","MEM"]],columns=["name","line_score","description"])
    df = apicalls.get_player_box()
    per36 = datacleaning.convert_per_36(df)
    # df = pd.read_pickle("playerstatsdf")
    # print(datacleaning.create_last_x(per36, "Donte DiVincenzo", 5))
    # print (datacleaning.create_season_avg(per36,"Donte DiVincenzo"))
  #  x, y = datacleaning.generate_x_y(per36)  # Run to generate model TODO SAVE MODEL/experiment with past x numbre
    #model1 = model.create_model(x, y)  # same here
    #print(model1.coef_)
#    finalmodel = model.propbet(x, y)
    filename="finalmodel.sav"
 #   pickle.dump(finalmodel,open(filename,'wb'))
    finalmodel=pickle.load(open(filename,'rb'))
    for index,row in lines.iterrows():
        player = row[0]
        ppline = row[1]
        opp = row[2]
        playerft = per36.where(per36['PLAYER_NAME'] == player).dropna(how="all")
        playerft = playerft['FTM'].sum() / playerft['FTA'].sum()
        buildplayer = (datacleaning.buildplayer(per36, player, opp, 5)) #todo add home/away
        buildplayer = np.array(buildplayer)
        buildplayer = buildplayer.reshape(1,-1)
        print (player, "odds")
        model.predictandpoisson(buildplayer, playerft,finalmodel, ppline)

# See PyCnharm help at https://www.jetbrains.com/help/pycharm/
