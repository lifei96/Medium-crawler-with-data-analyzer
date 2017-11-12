# -*- coding: utf-8 -*-

import pandas
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import f1_score
import numpy as np
import random
import json


def data_pre_process(train_path, test_path, label, drop_list=None):
    train_dataset = pandas.read_csv(train_path)
    if drop_list:
        train_dataset = train_dataset.drop(drop_list, axis=1)
    y_train = train_dataset[label].astype(int)
    print y_train.dtypes
    X_train = train_dataset.drop(label, axis=1)
    test_dataset = pandas.read_csv(test_path)
    if drop_list:
        test_dataset = test_dataset.drop(drop_list, axis=1)
    y_test = test_dataset[label].astype(int)
    print y_test.dtypes
    X_test = test_dataset.drop(label, axis=1)
    dtrain = xgb.DMatrix(X_train, label=y_train)
    dtest = xgb.DMatrix(X_test, label=y_test)
    return dtrain, dtest


def f1(preds, dtrain):
    dtrain = dtrain.get_label()
    y_bin = [1. if y_cont > 0.5 else 0. for y_cont in preds]
    return 'f1', f1_score(dtrain, y_bin)


def xgb_train(dtrain, dtest, param, num_boost_round=200):
    evallist = [(dtest, 'eval')]
    bst = xgb.train(param, dtrain, num_boost_round=num_boost_round, evals=evallist, feval=f1, maximize=True, early_stopping_rounds=50)
    print (param)
    print '-----cur_f1 ', bst.best_score
    preds = bst.predict(dtest)
    print (classification_report(dtest.get_label(), [1. if y_cont > 0.5 else 0. for y_cont in preds], digits=6))
    return bst.best_score


def random_grid_search(dtrain, dtest, output_path):
    param = {'learning_rate': 0.10,
             'max_depth': 6,
             'min_child_weight': 1,
             'gamma': 0,
             'subsample': 0.8,
             'colsample_bytree': 0.8,
             'alpha': 0,
             'lambda':1,
             'objective': 'multi:softmax',
             'num_class': 2,
             'seed': 7,
             'silent': 1}
    search_range = dict()
    search_range['learning_rate'] = [i/100.0 for i in range(5, 41)]
    search_range['max_depth'] = range(3, 11, 1)
    search_range['min_child_weight'] = range(1, 8, 1)
    search_range['gamma'] = [0.0, 0.1, 0.2]
    search_range['subsample'] = [i/10.0 for i in range(5, 11)]
    search_range['colsample_bytree'] = [i/10.0 for i in range(5, 11)]
    search_range['alpha'] = [0.0, 0.0001, 0.001, 0.005]
    param_list = list()
    for p1 in search_range['learning_rate']:
        for p2 in search_range['max_depth']:
            for p3 in search_range['min_child_weight']:
                for p4 in search_range['gamma']:
                    for p5 in search_range['subsample']:
                        for p6 in search_range['colsample_bytree']:
                            for p7 in search_range['alpha']:
                                param['learning_rate'] = p1
                                param['max_depth'] = p2
                                param['min_child_weight'] = p3
                                param['gamma'] = p4
                                param['subsample'] = p5
                                param['colsample_bytree'] = p6
                                param['alpha'] = p7
                                param_list.append(dict(param))
    random.shuffle(param_list)
    bst_param = dict()
    bst_f1 = 0
    cnt = 0
    tot = len(param_list)
    for param_cur in param_list:
        cur_f1 = xgb_train(dtrain, dtest, param_cur)
        if cur_f1 > bst_f1:
            bst_f1 = cur_f1
            bst_param = param_cur
        print '-----bst_f1 ', bst_f1
        if cnt % 10 == 0:
            with open(output_path, 'w') as f:
                json.dump(bst_param, f, indent=4)
            with open(output_path, 'a') as f:
                f.write(str(bst_f1))
        cnt += 1
        print '%d/%d' % (cnt, tot)


def solo_train():
    param = {'learning_rate': 0.37,
             'max_depth': 6,
             'min_child_weight': 1,
             'gamma': 0,
             'subsample': 0.6,
             'colsample_bytree': 0.9,
             'alpha': 0.005,
             'lambda': 1,
             'booster': 'gbtree',
             'objective': 'binary:logistic',
             'eval_metric': 'auc',
             'seed': 7,
             'silent': 1}
    dtrain, dtest = data_pre_process('./data/prediction/dataset_1_train.csv',
                                     './data/prediction/dataset_1_test.csv',
                                     'class_1')
    xgb_train(dtrain, dtest, param, 16)


def grid_train():
    dtrain, dtest = data_pre_process('./data/prediction/dataset_1_train.csv',
                                     './data/prediction/dataset_1_test.csv',
                                     'class_1')
    random_grid_search(dtrain, dtest, "./result/prediction/bst_param.txt")


if __name__ == '__main__':
    solo_train()
