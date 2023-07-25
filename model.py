# 3rdpartyimports
import math

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
from numpy import absolute, mean, std
from scipy.stats import poisson
import numpy as np
import pandas as pd


def create_model(X, y):  # generate opposition variables
    """a function that takes in our player averages, last ten averages, opponent and other predictors to generate
    a model to predict FTA per 36 value for player. y=historical fta/36"""
    dummies = pd.get_dummies(X['MATCHUP'])
    X = X.drop('MATCHUP', axis=1)
    X = pd.concat([X, dummies], axis=1)
    X = X.drop(['FT_PCTlastxgames', 'FG_PCTlastxgames', 'FG3_PCTlastxgames', 'FG_PCT', 'FG3_PCT', 'FT_PCT'], axis=1)
    X = X.fillna(0)
    X=X.values
    y = [0 if math.isnan(x) else x for x in y]
    y=y.values
    model = Lasso(alpha=1.0)
    cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)  # pretty typical numbers,can mess around later
    scores = cross_val_score(model, X, y, cv=cv, n_jobs=1)
    scores = absolute(scores)
    print('Mean MAE: %.3f (%.3f)' % (mean(scores), std(scores)))
    model.fit(X, y)
    return model


def propbet(X, y):
    scaler = StandardScaler()
    dummies = pd.get_dummies(X['MATCHUP'])
    X = X.drop('MATCHUP', axis=1)
    X = pd.concat([X, dummies], axis=1)
    X = X.drop(['FT_PCTlastxgames', 'FG_PCTlastxgames', 'FG3_PCTlastxgames', 'FG_PCT', 'FG3_PCT', 'FT_PCT'], axis=1)
    X = X.fillna(0)
    print(X)
    y = [0 if math.isnan(x) else x for x in y]
    X_train_val, X_test, y_train_val, y_test = train_test_split(
        X, y, test_size=.2, random_state=1)
    X_train, X_val, y_train, y_val = train_test_split(
        X_train_val, y_train_val, test_size=.25, random_state=2)
    X_train_scaled = scaler.fit_transform(X_train.values)
    X_val_scaled = scaler.fit_transform(X_val.values)
    alphavec = 10 ** np.linspace(-2, 2, 200)

    lasso_cv = LassoCV(alphas=alphavec, cv=5)
    lasso_cv.fit(X_train_scaled, y_train)
    lasso_cv.alpha_
    for col, coef in zip(X_train.columns, lasso_cv.coef_):
        print(f"{col:<16}: {coef:>12,.7f}")
    print(
        f'R2 for LassoCV Model on train set: {lasso_cv.score(X_train_scaled, y_train)}')
    val_set_preds = lasso_cv.predict(X_val_scaled)
    print(
        f'R2 for LassoCV Model on validation set: {lasso_cv.score(X_val_scaled, y_val)}')
    mae = mean_absolute_error(y_val, val_set_preds)
    print(f'Mean absolute error for LassoCV model on validation set: {mae}')

    alpha = np.logspace(-4, 2, 100)  # np.logspace(-4, -.1, 20)
    param_grid = dict(alpha=alpha)
    grid_en = GridSearchCV(ElasticNet(), param_grid=param_grid,
                           scoring='neg_mean_absolute_error', cv=5)
    grid_result_en = grid_en.fit(X_train, y_train)

    print(f'Best Score: {grid_result_en.best_score_}')
    print(f'Best Param: {grid_result_en.best_params_}')
    elastic_cv = ElasticNetCV(
        alphas=[0.0021544346900318843], cv=5, random_state=0)
    elastic_cv.fit(X_train, y_train)
    print(
        f'ElasticNet Mean R Squared Score on training data: {elastic_cv.score(X_train, y_train)}')
    print(
        f'ElasticNet Mean R Squared Score on validation data: {elastic_cv.score(X_val, y_val)}')
    val_set_preds = elastic_cv.predict(X_val)
    mae = mean_absolute_error(y_val, val_set_preds)
    print(f'Mean absolute error for ElasticNet model on validation set: {mae}')
    rmse = mean_squared_error(y_val, val_set_preds, squared=False)
    print(
        f'Root mean squared error for ElasticNet model on validation set: {rmse}')
    for col, coef in zip(X_test.columns, elastic_cv.coef_):
        print(f"{col:<16}: {coef:>12,.7f}")
    elastic_preds = elastic_cv.predict(X)
    X['Model Predictions'] = elastic_preds
    return elastic_cv


def predictandpoisson(X, ftpercent, model, line):
    """taking our created model and x values for upcoming games output our projected FTA/36 and use
    last ten games minutes average to get a final FTA number for the game, then use poisson to create distribution"""
    yhat = model.predict(X)
    yhat = yhat * X[0][0]/36 #convert out of per36
    yhat = float(yhat * ftpercent)
    print("projected makes", yhat, " minutes ",X[0][0])
    line=float(line)
    drawodds= poisson.pmf(line,yhat)
    overodds = 1 - poisson.cdf(line, yhat)
    underodds = poisson.cdf(line, yhat)
    print("On a line of ",line, " Over odds are: ", overodds, "Draw odds are: ",drawodds, " and Under odds are ", underodds-drawodds)
    return [line,overodds,drawodds,underodds-drawodds,yhat]
