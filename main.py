import apicalls
import nbaconstants
import pandas as pd
import datacleaning
import ppscrape
import model
import numpy as np
import pickle

if __name__ == '__main__':
    lines = pd.DataFrame(ppscrape.GetLines2())
    #lines=pd.DataFrame([["Julius Randle","5.5", "PHI"],["Joel Embiid","9.5","MEM"]],columns=["name","line_score","description"])
    df = apicalls.get_player_box()
    per36 = datacleaning.convert_per_36(df)
    # df = pd.read_pickle("playerstatsdf")
    # print(datacleaning.create_last_x(per36, "Donte DiVincenzo", 5))
    # print (datacleaning.create_season_avg(per36,"Donte DiVincenzo"))
    #x, y = datacleaning.generate_x_y(per36,10)  # Run to generate model TODO interaction terms/experiment with past x numbre
    #model1 = model.create_model(x, y)  # same here
    #print(model1.coef_)
    #finalmodel = model.propbet(x, y)
    filename="finalmodel.sav"
    #pickle.dump(finalmodel,open(filename,'wb'))
    finalmodel=pickle.load(open(filename,'rb'))
    output=pd.DataFrame(columns=['Name','Line','Over_Odds','Draw_Odds','Under_Odds'])
    for index,row in lines.iterrows():
        player = row[0]
        ppline = row[1]
        opp = row[2]
        playerft = per36.where(per36['PLAYER_NAME'] == player).dropna(how="all")
        playerft = playerft['FTM'].sum() / playerft['FTA'].sum()
        buildplayer = (datacleaning.buildplayer(per36, player, opp, 10)) #todo add home/away
        buildplayer = np.array(buildplayer)
        buildplayer = buildplayer.reshape(1,-1)
        print (player, "odds")
        result=model.predictandpoisson(buildplayer, playerft,finalmodel, ppline)
        output.loc[len(output.index)] = [player, result[0],result[1],result[2],result[3]]
    print (output)

# See PyCnharm help at https://www.jetbrains.com/help/pycharm/
