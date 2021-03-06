#!/usr/bin/env python
#-*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import math

from sklearn import preprocessing
from sklearn.cross_validation import StratifiedShuffleSplit, StratifiedKFold
from sklearn.feature_selection import VarianceThreshold


from ubd.unbalanced_dataset import UnbalancedDataset
from ubd.over_sampling import OverSampler
from ubd.over_sampling import SMOTE

from ubd.under_sampling import UnderSampler
from ubd.under_sampling import TomekLinks
from ubd.under_sampling import ClusterCentroids
from ubd.under_sampling import NearMiss
from ubd.under_sampling import CondensedNearestNeighbour
from ubd.under_sampling import OneSidedSelection
from ubd.under_sampling import NeighbourhoodCleaningRule

from ubd.ensemble_sampling import EasyEnsemble
from ubd.ensemble_sampling import BalanceCascade

from ubd.pipeline import SMOTEENN
from ubd.pipeline import SMOTETomek

def ubd_sample(X, y, name="smote_regular", k =5, m = 10, ratio=1.0):
    if name == 'smote_regular':
        sm = SMOTE(kind='regular', k = k, m = m, ratio = ratio, verbose=True)
        svmx, svmy = sm.fit_transform(X, y)

        return (svmx, svmy)

    elif name == 'smote_type1':
        sm = SMOTE(kind='borderline1', k = k, m = m, ratio = ratio, verbose=True)
        svmx, svmy = sm.fit_transform(X, y)
        return (svmx, svmy)

    elif name == 'smote_type2':
        sm = SMOTE(kind='borderline2', k= 5, m = 10, ratio = 1.0, verbose=True)
        svmx, svmy = sm.fit_transform(X, y)
        return (svmx, svmy)

    elif name == 'smote_svm': # too slowly
        svm_args={'class_weight': 'auto', 'kernel': 'linear'}

        sm = SMOTE(kind='svm', verbose=True, **svm_args)
        svmx, svmy = sm.fit_transform(X, y)
        return (svmx, svmy)
    elif name == 'smote_tomek':
        print('SMOTE Tomek links')
        STK = SMOTETomek(verbose=True)
        stkx, stky = STK.fit_transform(X, y)
        return (stkx, stky)
    elif name == 'smote_enn':
        print('SMOTE ENN')
        SENN = SMOTEENN(ratio = 2.0, verbose=True)
        sennx, senny = SENN.fit_transform(X, y)
        return (sennx, senny)
    elif name == 'smote_easy':
        print('EasyEnsemble')
        EE = EasyEnsemble(verbose=True)
        eex, eey = EE.fit_transform(X, y)
        return (eex, eey)

    elif name == 'random_sample':
        US = UnderSampler(verbose=True)
        usx, usy = US.fit_transform(X, y)
        return (usx, usy)
    elif name == 'cascade':
        print 'Cascade UBD'
        BS = BalanceCascade(classifier = 'gradient-boosting', verbose=True)
        bsx, bsy = BS.fit_transform(X, y)
        return (bsx, bsy)


def merge_features(files, label_file=None):
    data_set = None
    for filepath in files:
        if data_set is None:
            data_set = pd.read_csv(filepath)
        else:
            d = pd.read_csv(filepath)
            data_set = pd.merge(data_set, d, on="enrollment_id")

    if label_file is not None:
        labels = pd.read_csv(label_file)
        data_set = pd.merge(data_set, labels, on="enrollment_id")
        #dataset['dropout'] = encode_labels(data_set.dropout.values)

    return data_set

def load_dataset(feature_file, label_file=None, verbose=False):
    # import data
    data_set = pd.read_csv(feature_file)

    if label_file is not None:
        labels = pd.read_csv(label_file)
        data_set = pd.merge(data_set, labels, on="enrollment_id")
        data_set['dropout'] = encode_labels(data_set.dropout.values)

    return data_set


def log_transf(data, features = None):
    # Create three new columns with logarithmic transform
    if features is None:
        features = data.columns
    for col in features:
        data['log-' + col] = data[col].apply(lambda x: math.log(1 + x))
    return data

def log_transf_replace(data, features = None):
    if features is None:
        features = data.columns
    for col in features:
        # print col
        data[col] = data[col].apply(lambda x: math.log(1.0 + x))
    return data

def square_root_transf(data, features):
    if features is None:
        features = data.columns
    for col in features:
        data['sqr_' + col] = data[col].apply(lambda x: math.sqrt(x))
    return data

def square_root_transf_replace(data, features):
    if features is None:
        features = data.columns
    for col in features:
        data[col] = data[col].apply(lambda x: math.sqrt(x))

    return data


def inverse_transf(data, features):
    if features is None:
        features = data.columns
    for col in features:
        data['inverse_' + col] = data[col].apply(lambda x: 1.0 / (x+1.0))
    return data

def inverse_transf_replace(data, features):
    if features is None:
        features = data.columns()
    for col in features:
        data[col] = data[col].apply(lambda x: 1.0 / (1.0 + x))
    return data

def sqrtexp_transf(data, features):
    if features is None:
        features = data.columns
    for col in features:
        data['sqrt_exp_' + col] = data[col].apply(lambda x: 1.0 / (1.0 + math.exp(-math.sqrt(x))))

    return data

def sqrtexp_transf_replace(data, features):
    if features is None:
        features = data.columns
    for col in features:
        data[col] = data[col].apply(lambda x: 1.0 / (1.0 + math.exp(-math.sqrt(x))))
    return data

def encode_labels(labels):
    # encode labels
    lbl_enc = preprocessing.LabelEncoder()
    return lbl_enc.fit_transform(labels)

def random_split(dataset, labels, test_size = 0.2, random_state = 0):

    sss = StratifiedShuffleSplit(labels, test_size=test_size, random_state= random_state)
    for train_index, test_index in sss:
        break
    data = dataset
    if isinstance(dataset, pd.DataFrame):
        data = dataset.values
    train_x, train_y  = data[train_index], labels[train_index]
    test_x, test_y = data[test_index], labels[test_index]

    return (train_x, train_y, test_x, test_y)

def folds_indexes(labels, n_folds = 5, random_state = 0):
    cv = StratifiedKFold(labels, n_folds = n_folds, shuffle=True, random_state = random_state)
    for train_index, test_index in cv:
        yield (train_index, test_index)

def folds_split(dataset, labels, n_folds=3, random_state = 314159):
    cv = StratifiedKFold(labels, n_folds=n_folds, shuffle=True, random_state=random_state)
    data = dataset
    if isinstance(dataset, pd.DataFrame):
        data = dataset.values
    for train_index, test_index in cv:
        train_x, train_y  = data[train_index], labels[train_index]
        test_x, test_y = data[test_index], labels[test_index]
        yield (train_x, train_y, test_x, test_y)
