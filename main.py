import apicalls
import nbaconstants
import pandas as pd
import datacleaning
import ppscrape
import model
import numpy as np
import pickle
import matplotlib
if __name__ == '__main__':
    pd.set_option('display.width', 400)
    pd.set_option('display.max_columns', 20)
    pd.set_option('display.max_rows', 100)
    lines = pd.DataFrame(ppscrape.GetLines2())
    #lines=pd.DataFrame([["Julius Randle","5.5", "PHI"],["Joel Embiid","9.5","MEM"]])
    # columns=["name","line_score","description"])
    df = apicalls.get_player_box()
    per36 = datacleaning.convert_per_36(df)
   # filter=df['MIN']>30
    #df=df.where(filter)
    #((df['FTM']).plot(kind='hist',bins=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]))
    #matplotlib.pyplot.show()
    #(datacleaning.create_last_x(per36,"James Harden",5))
    #x, y = datacleaning.generate_x_y(per36,5)  # Run to generate model 5 best tested, TODO need to search in 5-10 range
    #storedx=x.to_pickle("storedx")
    #storedy=y.to_pickle("storedy")
    #finalmodel = model.propbet(x, y)
    filename = "finalmodel.sav"
    #pickle.dump(finalmodel,open(filename,'wb'))
    finalmodel = pickle.load(open(filename, 'rb'))
    output = pd.DataFrame(columns=['Name', 'Line', 'Over_Odds', 'Draw_Odds', 'Under_Odds','Projected_Makes'])
    for index, row in lines.iterrows():
        player = row[0]
        ppline = row[1]
        opp = row[2]
        playerft = per36.where(per36['PLAYER_NAME'] == player).dropna(how="all")
        playerft = playerft['FTM'].sum() / playerft['FTA'].sum()
        buildplayer = (datacleaning.buildplayer(per36, player,True,opp, 5))  # todo add home/away
        buildplayer = np.array(buildplayer)
        buildplayer = buildplayer.reshape(1, -1)
        print(player, "odds")
        result = model.predictandpoisson(buildplayer, playerft, finalmodel, ppline)
        output.loc[len(output.index)] = [player, result[0], result[1], result[2], result[3],result[4]]
    print(output)
