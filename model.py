#3rdpartyimports
from sklearn.model_selection import (
    cross_val_score, KFold, train_test_split, GridSearchCV, RepeatedKFold)
import matplotlib.pyplot as plt
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import (OneHotEncoder, StandardScaler,
                                   PolynomialFeatures)
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import (accuracy_score, confusion_matrix,
                             classification_report, mean_squared_error,
                             mean_absolute_error)
from sklearn.linear_model import (LinearRegression, LassoCV, Lasso, RidgeCV, Ridge,
                                  ElasticNetCV, ElasticNet, BayesianRidge,
                                  LogisticRegression, SGDRegressor)
from numpy import absolute,mean,std
from scipy.stats import poisson
def create_model(X,y):
    '''a function that takes in our player averges, last ten averages, opponent and other predictors to generate
    a model to predict FTA per 36 value for player. y=historical fta/36'''
    model= Lasso(alpha=1.0)
    cv=RepeatedKFold(n_splits=10,n_repeats=3,random_state=1) #pretty typical numbers,can mess around later
    scores=cross_val_score(model,X,y,scoring='neg_man_absolute_error',cv=cv,n_jobs=1)
    scors=absolute(scores)
    print ('Mean error: %.3f (%.3f)' % mean(scores),std(scores))
    model.fit(X,y)
    return model

def predictandpoisson(X,model,lines):
    '''taking our created model and x values for upcoming games output our projected FTA/36 and use
    last ten games minutes average to get a final FTA number for the game, then use poisson to create distribution'''
    yhat=model.predict(X)
    FTA=yhat #TODO Create conversion once dataframe known
    for player in lines:  ##iterate over every player row, match lines to names, output results
        overodds=poisson.cdf(player['line'],player['FT%'])
        underodds=1-poisson.cdf(player['line'],player['FT%'])

