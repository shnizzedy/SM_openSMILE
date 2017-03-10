#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
trees.py

Run tree analyses on
[n_participants × n_files × n_features × n_Dxs]
*.csv file from openSMILE_csv.py

Authors:
	– Jon Clucas, 2016–2017 (jon.clucas@childmind.org)

@author: jon.clucas
"""
import os, sys
if os.path.abspath('../../') not in sys.path:
    if os.path.isdir(os.path.join(os.path.abspath('../..'), 'SM_openSMILE')):
        sys.path.append(os.path.abspath('../..'))
    elif os.path.isdir(os.path.join(os.path.abspath('..'), 'SM_openSMILE')):
        sys.path.append(os.path.abspath('..'))
    elif os.path.isdir('SM_openSMILE'):
        sys.path.append(os.path.abspath('.'))
from itertools import zip_longest
import ast, csv, numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

def make_forest(replacement, condition, config):
    """
    Function to get training and target data, filling in unaltered rows when no
    altered row exists

    Parameters
    ----------
    replacement : string
        replacement condition
    
    condition : string
        experimental condition
        
    config : string
        basename of openSMILE config file

    Returns
    -------
    x_trees : numpy array
        array of [n_participants × n_features] size
        filled with training data (features)

    y_trees : numpy array
        array of [n_participants] size
        filled with target data (diagnoses)
    """
    x_trees = []
    y_trees = []
    n_samples = 0
    n_features = 0
    rpath = os.path.join(os.path.abspath('../openSMILE_preprocessing/'
            'noise_replacement/replacement_test_outputs/adults_replaced/'
            'summary'), config, ''.join([replacement, condition,
            'feature_data.csv']))
    opath = os.path.join(os.path.abspath('../openSMILE_preprocessing/'
            'noise_replacement/replacement_test_outputs/adults_replaced/'
            'summary'), config, ''.join(['original', condition,
            'feature_data.csv']))
    if(os.path.exists(rpath)):
        # fill in unaltered rows when no altered row exists
        with open(rpath, 'r') as rf, open(opath, 'r') as of:
            rreader = csv.reader(rf)
            oreader = csv.reader(of)
            for rrow, orow in zip_longest(rreader, oreader):
                if rrow:
                    if len(rrow) > 0:
                        row = rrow
                else:
                    row = orow
                for column in row:
                    column = ast.literal_eval(column)
                    if (column[1] != "['unknown']"):
                        enc = LabelEncoder()
                        enc.fit(np.array(column[0]))
                        for feature in list(column[0]):
                            try:
                                feature = float(feature)
                            except:
                                feature = enc.transform(np.array([feature]))[0]
                            x_trees.append(feature)
                            if n_samples == 0:
                                n_features = n_features + 1
                        y_trees.append(column[1])
                        n_samples = n_samples + 1
    return (np.array(x_trees).reshape(n_samples, n_features),
            np.array(y_trees).reshape(n_samples))

def make_ltd_forest(replacement, condition, config):
    """
    Function to get training and target data, skipping missing rows

    Parameters
    ----------
    replacement : string
        replacement condition
    
    condition : string
        experimental condition
        
    config : string
        basename of openSMILE config file

    Returns
    -------
    x_trees : numpy array
        array of [n_participants × n_features] size
        filled with training data (features)

    y_trees : numpy array
        array of [n_participants] size
        filled with target data (diagnoses)
    """
    x_trees = []
    y_trees = []
    n_samples = 0
    n_features = 0
    rpath = os.path.join(os.path.abspath('../openSMILE_preprocessing/'
            'noise_replacement/replacement_test_outputs/adults_replaced/'
            'summary'), config, ''.join([replacement, condition,
            'feature_data.csv']))
    if(os.path.exists(rpath)):
        with open(rpath, 'r') as rf:
            rreader = csv.reader(rf)
            for rrow in rreader:
                if len(rrow) > 0:
                    row = rrow
                else:
                    row = ''
                    next
                for column in row:
                    column = ast.literal_eval(column)
                    if (column[1] != "['unknown']"):
                        enc = LabelEncoder()
                        enc.fit(np.array(column[0]))
                        for feature in list(column[0]):
                            try:
                                feature = float(feature)
                            except:
                                feature = enc.transform(np.array([feature]))[0]
                            x_trees.append(feature)
                            if n_samples == 0:
                                n_features = n_features + 1
                        y_trees.append(column[1])
                        n_samples = n_samples + 1
    return (np.array(x_trees).reshape(n_samples, n_features),
            np.array(y_trees).reshape(n_samples))
    
def make_original_forest(condition, config):
    """
    Function to get training and target data, filling in unaltered rows when no
    altered row exists

    Parameters
    ----------
    condition : string
        experimental condition
        
    config : string
        basename of openSMILE config file

    Returns
    -------
    x_trees : numpy array
        array of [n_participants × n_features] size
        filled with training data (features)

    y_trees : numpy array
        array of [n_participants] size
        filled with target data (diagnoses)
    """
    x_trees = []
    y_trees = []
    n_samples = 0
    n_features = 0
    rpath = os.path.join(os.path.abspath('../openSMILE_preprocessing/'
            'noise_replacement/replacement_test_outputs/adults_replaced/'
            'summary'), config, ''.join(['adults', condition,
            'feature_data.csv']))
    opath = os.path.join(os.path.abspath('../openSMILE_preprocessing/'
            'noise_replacement/replacement_test_outputs/adults_replaced/'
            'summary'), config, ''.join(['original', condition,
            'feature_data.csv']))
    if(os.path.exists(rpath)):
        # fill in unaltered rows when no altered row exists
        with open(rpath, 'r') as rf, open(opath, 'r') as of:
            rreader = csv.reader(rf)
            oreader = csv.reader(of)
            for rrow, orow in zip_longest(rreader, oreader):
                if rrow:
                    if len(rrow) > 0:
                        row = ''
                        next
                else:
                    row = orow
                for column in row:
                    column = ast.literal_eval(column)
                    if (column[1] != "['unknown']"):
                        enc = LabelEncoder()
                        enc.fit(np.array(column[0]))
                        for feature in list(column[0]):
                            try:
                                feature = float(feature)
                            except:
                                feature = enc.transform(np.array([feature]))[0]
                            x_trees.append(feature)
                            if n_samples == 0:
                                n_features = n_features + 1
                        y_trees.append(column[1])
                        n_samples = n_samples + 1
    return (np.array(x_trees).reshape(n_samples, n_features),
            np.array(y_trees).reshape(n_samples))

def get_feature_dictionary(config):
    """
    Function to give name to emobase function from number

    Parameters
    ----------
    config : string
        basename of openSMILE config file

    Returns
    -------
    feature_dictionary : dictionary
        dictionary of emobase features
    """
    feature_dictionary = {}
    with open(os.path.join(dict_fp, config, ''.join([config, '_features.csv'])
             ), 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            feature_dictionary[row[0]] = row[1]
    return feature_dictionary

def main(replacement, condition, config, ltd=False):
    """
    Main function to run random forest analysis on a replacement & experimental
    condition.
    
    Parameters
    ----------
    replacement : string
        replacement condition
        
    condition : string
        experimental condition
        
    config : string
        openSMILE config basename
        
    ltd : boolean (optional, default == False)
       do not collect missing rows from original (non-replacement) condition
       
    Returns
    -------
    None
    
    Outputs
    -------
    replacement + condition + feature_ranking.csv : CSV file
        feature ranking CSV for replacement + condition
        
    replacement + condition + feature_ranking_score.txt : text file
        feature ranking confidence for replacement + condition
        
    replacement + condition + feature_ranking_gtp01.csv : CSV file
        feature ranking > .01 CSV for replacement + condition
        
    replacement + condition + feature_ranking_top15.csv : CSV file
        feature ranking top 15 CSV for replacement + condition
    """
    # get data
    if replacement == 'unmodified':
        x, y = make_original_forest(condition, config)
    else:
        if ltd:
            x, y = make_ltd_forest(replacement, condition, config)
        else:
            x, y = make_forest(replacement, condition, config)
    # random forest classification
    clf = RandomForestClassifier(n_estimators=2000, oob_score = True)
    clf = clf.fit(x, y)
    importances = clf.feature_importances_
    for importance in importances:
        importance = abs(importance)
    std = np.std([tree.feature_importances_ for tree in clf.estimators_],
             axis=0)
    indices = np.argsort(importances)[::-1]
    print (clf.oob_score_)
    print (clf.oob_decision_function_)

    # output feature rankings
    file_index = 0
    if replacement == 'unmodified':
        csv_path = os.path.join(os.path.abspath('../openSMILE_preprocessing/'
                   'noise_replacement/replacement_test_outputs/'
                   'adults_replaced/summary'), config, 'random_forests/'
                   'unmodified')
    else:
        if ltd:
            csv_path = os.path.join(os.path.abspath('../'
                       'openSMILE_preprocessing/noise_replacement/'
                       'replacement_test_outputs/adults_replaced/summary'),
                       config, 'random_forests/ltd')
        else:
            csv_path = os.path.join(os.path.abspath('../'
                       'openSMILE_preprocessing/noise_replacement/'
                       'replacement_test_outputs/adults_replaced/summary'),
                       config, 'random_forests')
    if not os.path.exists(csv_path):
        os.makedirs(csv_path)
    csv_filename = replacement + condition + 'feature_ranking'
    while os.path.exists(os.path.join(csv_path,(csv_filename + '.csv'))):
        csv_filename = replacement + condition + 'feature_ranking' + str(
                       file_index)
        file_index = file_index + 1
    o_csv = os.path.join(csv_path,(csv_filename + '.csv'))
    o_score = os.path.join(csv_path, (csv_filename + '_score.txt'))
    o_gtp01 = os.path.join(csv_path,(csv_filename + '_gtp01.csv'))
    o_top15 = os.path.join(csv_path,(csv_filename + '_top15.csv'))
    feature_dictionary = get_feature_dictionary(config)
    feature_ranking_csv = open(o_csv, 'w')
    feature_ranking_gtp01 = open(o_gtp01, 'w')
    feature_ranking_top15 = open(o_top15, 'w')
    feature_ranking_score = open(o_score, 'w')
    feature_ranking_score.write(str(clf.oob_score_))
    feature_ranking_score.write(str(clf.oob_decision_function_))
    feature_ranking_score.close()
    i = 0
    for f in range(x.shape[1]):
        feature_ranking_csv.write(feature_dictionary[str(indices[f])])
        feature_ranking_csv.write(",%f" % (importances[indices[f]]))
        feature_ranking_csv.write("\n")
        if (importances[indices[f]] >= 0.01):
            feature_ranking_gtp01.write(feature_dictionary[str(indices[f])])
            feature_ranking_gtp01.write(",%f" % (importances[indices[f]]))
            feature_ranking_gtp01.write("\n")
        if i < 15:
            feature_ranking_top15.write(feature_dictionary[str(indices[f])])
            feature_ranking_top15.write(",%f" % (importances[indices[f]]))
            feature_ranking_top15.write("\n")
            i = i + 1
    feature_ranking_csv.close()
    feature_ranking_gtp01.close()
    feature_ranking_top15.close()
    """
    # plot the feature importances of the forest
    fig, ax = plt.subplots()
    plt.title("Feature importances")
    ax.barh(width=range(x.shape[1]), bottom=importances[indices], color=cmi_colors()[0],
           xerr=std[indices], ecolor=cmi_colors()[1])
    # ax.set_adjustable('box')
    # ax.set_aspect(4/x.shape[1], adjustable='box')
    plt.axis('scaled')
    plt.yticks(range(x.shape[1]), indices)
    plt.ylim([-1, x.shape[1]])
    plt.xlim([0, max(importances[indices]) + .01])
    plt.gca().get_xaxis().set_visible(False)
    plt.xlabel("Feature importance")
    plt.ylabel("Features")
    plt.savefig(os.path.join(csv_path,(csv_filename + '.svg')),
                dpi=300, transparent=True)
    plt.figure()
    plt.title("Feature importances")
    plt.bar(range(x.shape[1]), abs(importances[indices]),
           color="r", yerr=std[indices], align="center")
    plt.xticks(range(x.shape[1]), indices)
    plt.xlim([-1, x.shape[1]])
    plt.xlab("Features")
    plt.ylab("Feature importance")
    plt.savefig(os.path.join(csv_path,(csv_filename + '.png')))
 
    plt.figure()
    plt.title("Feature importances")
    plt.bar(range(15), importances[indices],
           color="r", yerr=std[indices], align="center")
    plt.xticks(range(15), indices)
    plt.xlim([-1, 15])
    plt.savefig(os.path.join(csv_path,(csv_filename + '_top15.png')))
    """

# ============================================================================
if __name__ == '__main__':
    # filepath of feature dictionary top-level directory
    global dict_fp
    dict_fp = os.path.abspath('../openSMILE_preprocessing/noise_replacement/'
              'replacement_test_outputs/configs/')
    conditions = ['_button_no_', '_button_w_', '_vocal_no_', '_vocal_w_']
    replacements = ['adults_removed', 'adults_replaced_clone',
                   'adults_replaced_pink', 'adults_timeshifted']
    configs = ['emobase', 'ComParE_2016']
    for condition in conditions:
        for config in configs:
            print(' \u219D '.join(['unmodified', condition, config]))
            main('unmodified', condition, config)
    for replacement in replacements:
        for condition in conditions:
            for config in configs:
                print(' \u219D '.join([replacement, condition, config]))
                main(replacement, condition, config)
    for replacement in (['adults', 'original'] + replacements):
        for condition in conditions:
            for config in configs:
                print(' \u219D '.join(['ltd', replacement, condition, config]))
                main(replacement, condition, config, True)