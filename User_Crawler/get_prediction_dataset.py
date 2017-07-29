# -*- coding: utf-8 -*-

import pandas as pd
from sklearn.model_selection import train_test_split


def get_prediction_dataset():
    dataset = pd.read_csv('./data/prediction/dataset.csv')
    dataset = dataset.dropna(how='any')
    dataset = dataset.drop(['PR', 'authorTags', 'bio', 'collections', 'createdAt', 'facebook', 'username', 'followers', 'following', 'highlights', 'interestTags', 'lastPostCreatedAt', 'posts', 'postsInMonthlyTop100', 'recommends', 'responses', 'topAuthorTags', 'twitter'], axis=1)
    cols = list(dataset.columns.values)
    cols.pop(cols.index('class_1'))
    cols.pop(cols.index('class_5'))
    cols.pop(cols.index('class_10'))
    dataset = dataset[cols + ['class_1', 'class_5', 'class_10']]

    dataset_1 = dataset
    dataset_1 = dataset_1.drop(['class_5', 'class_10'], axis=1)
    dataset_1_0 = dataset_1[dataset_1['class_1'] == 0].sample(10000)
    dataset_1_1 = dataset_1[dataset_1['class_1'] == 1].sample(10000)
    dataset_1_0_train, dataset_1_0_test = train_test_split(dataset_1_0, test_size=0.2, random_state=7)
    dataset_1_1_train, dataset_1_1_test = train_test_split(dataset_1_1, test_size=0.2, random_state=77)
    dataset_1_train = pd.concat([dataset_1_0_train, dataset_1_1_train])
    dataset_1_test = pd.concat([dataset_1_0_test, dataset_1_1_test])
    dataset_1_train.to_csv('./data/prediction/dataset_1_train.csv', index=False, encoding='utf-8')
    dataset_1_test.to_csv('./data/prediction/dataset_1_test.csv', index=False, encoding='utf-8')

    dataset_5 = dataset
    dataset_5 = dataset_5.drop(['class_1', 'class_10'], axis=1)
    dataset_5_0 = dataset_5[dataset_5['class_5'] == 0].sample(10000)
    dataset_5_1 = dataset_5[dataset_5['class_5'] == 1].sample(10000)
    dataset_5_0_train, dataset_5_0_test = train_test_split(dataset_5_0, test_size=0.2, random_state=7)
    dataset_5_1_train, dataset_5_1_test = train_test_split(dataset_5_1, test_size=0.2, random_state=77)
    dataset_5_train = pd.concat([dataset_5_0_train, dataset_5_1_train])
    dataset_5_test = pd.concat([dataset_5_0_test, dataset_5_1_test])
    dataset_5_train.to_csv('./data/prediction/dataset_5_train.csv', index=False, encoding='utf-8')
    dataset_5_test.to_csv('./data/prediction/dataset_5_test.csv', index=False, encoding='utf-8')

    dataset_10 = dataset
    dataset_10 = dataset_10.drop(['class_5', 'class_1'], axis=1)
    dataset_10_0 = dataset_10[dataset_10['class_10'] == 0].sample(10000)
    dataset_10_1 = dataset_10[dataset_10['class_10'] == 1].sample(10000)
    dataset_10_0_train, dataset_10_0_test = train_test_split(dataset_10_0, test_size=0.2, random_state=7)
    dataset_10_1_train, dataset_10_1_test = train_test_split(dataset_10_1, test_size=0.2, random_state=77)
    dataset_10_train = pd.concat([dataset_10_0_train, dataset_10_1_train])
    dataset_10_test = pd.concat([dataset_10_0_test, dataset_10_1_test])
    dataset_10_train.to_csv('./data/prediction/dataset_10_train.csv', index=False, encoding='utf-8')
    dataset_10_test.to_csv('./data/prediction/dataset_10_test.csv', index=False, encoding='utf-8')


if __name__ == '__main__':
    get_prediction_dataset()
