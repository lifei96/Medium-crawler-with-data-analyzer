# -*- coding: utf-8 -*-

import pandas as pd
import xgboost as xgb
from sklearn.metrics import classification_report
from sklearn.metrics import f1_score
import numpy as np


def f1(preds, dtrain):
    return 'f1-score', -f1_score(dtrain.get_label(), preds, average='weighted')


def xgb_pr():
    train_set = pd.read_csv('./data/prediction/dataset_1_train.csv')
    test_set = pd.read_csv('./data/prediction/dataset_1_test.csv')
    y_train = np.array(train_set['class_1'].values.tolist())
    y_test = np.array(test_set['class_1'].values.tolist())
    train_set = train_set.drop('class_1', axis=1)
    test_set = test_set.drop('class_1', axis=1)
    X_train = np.array(train_set.values.tolist())
    X_test = np.array(test_set.values.tolist())
    dtrain = xgb.DMatrix(X_train, label=y_train)
    dtest = xgb.DMatrix(X_test, label=y_test)
    param = {'learning_rate': 0.1,
             'n_estimators': 100,
             'max_depth': 6,
             'min_child_weight': 1,
             'gamma': 0,
             'subsample': 0.8,
             'colsample_bytree': 0.8,
             'reg_alpha': 0,
             'objective': 'multi:softmax',
             'num_class': 2,
             'seed': 7,
             'silent': 1}
    evallist = [(dtest, 'eval')]
    bst = xgb.train(param, dtrain, num_boost_round=300, evals=evallist, feval=f1, early_stopping_rounds=50)
    print (param)
    preds = bst.predict(dtest)
    #print (classification_report(y_test, preds, digits=6))


if __name__ == '__main__':
    xgb_pr()
