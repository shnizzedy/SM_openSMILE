#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
feature_ranking.py

Explore weighted feature rankings produced by random forests in
trees.py

Authors:
	– Jon Clucas, 2017 (jon.clucas@childmind.org)

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
import pandas as pd

def main(config):
    """
    Main function. Builds and saves a ranking_table and a weighted_table for
    each replacement condition.
    
    Paremeters
    ----------
    config : string
        openSMILE configuration file basename
    
    Returns
    -------
    None
    
    Outputs
    -------
    *ranking_table.csv : CSV file
        a csv of ranking_table
        
    *weighted_table.csv : CSV file
        a csv of weighted_table
    """
    full_replacements = ["removed", "replaced_clone", "replaced_pink",
                       "timeshifted"]
    ltd_replacements = ["adults", "original"]
    
    analysis_dir = os.path.join('../openSMILE_analysis/random_forests',
                                'predict_SM/long_files/summary', config)
    # run and save the cleaned-up summaries
    for replacement in full_replacements:
        replacement = '_'.join(['adults', replacement])
        fs_path = os.path.join(analysis_dir, 'feature_summary',
                  replacement)
        ranking_table = build_ranking_table(replacement)
        run_and_save(''.join([fs_path, '_ranking.csv']), ranking_table)
        run_and_save(''.join([fs_path, '_weighted.csv']),
                     collect_weighted_table(ranking_table))
        fs_path = os.path.join(analysis_dir, 'feature_summary', 'ltd',
                  replacement)
        ranking_table = build_ranking_table(replacement, 'ltd')
        run_and_save(''.join([fs_path, '_ranking.csv']), ranking_table)
        run_and_save(''.join([fs_path, '_weighted.csv']),
                     collect_weighted_table(ranking_table))
        
    # run and save the limited summaries        
    for replacement in ltd_replacements:
        fs_path = os.path.join(analysis_dir, 'feature_summary', 'ltd',
                  replacement)
        ranking_table = build_ranking_table(replacement, 'ltd')
        run_and_save(''.join([fs_path, '_ranking.csv']), ranking_table)
        run_and_save(''.join([fs_path, '_weighted.csv']),
                     collect_weighted_table(ranking_table))
        
    # run and save the files that needed no cleaning summaries        
    fs_path = os.path.join(analysis_dir, 'feature_summary',
              'unmodified', 'unmodified')
    ranking_table = build_ranking_table('unmodified', 'unmodified')
    run_and_save(''.join([fs_path, '_ranking.csv']), ranking_table)
    run_and_save(''.join([fs_path, '_weighted.csv']), collect_weighted_table(
                 ranking_table))
    
def build_ranking_table(replacement, special=None):
    """
    Function to build a ranking table for each experimental condition for a
    given replacement condition

    Parameters
    ----------
    replacement : string
        the replacement condition to build the ranking table for
        
    special : string or None
        ["ltd", "unmodified", None]: if we're building from something other
        than a full replacement dataset, what the special case is
    
    Returns
    -------
    ranking_table : pandas dataframe
        a [4 × n_features] × [task, stranger, feature, score, confidence_weight
        ] dataframe
        
    """
    if special:
        topdir = os.path.join(data_dir, special)
    else:
        topdir = data_dir
    tasks = ["button", "vocal"]
    strangers = ["w", "no"]
    in_tables = []
    for task in tasks:
        for stranger in strangers:
            infile = os.path.join(topdir, '_'.join([replacement, task,
                     stranger, 'feature_ranking.csv']))
            in_table = get_weight_table(infile)
            in_table["task"] = task
            in_table["stranger"] = stranger
            in_tables.append(in_table)
    ranking_table = pd.concat(in_tables)
    return ranking_table
            
def collect_weighted_table(ranking_table):
    """
    Function to build a weighted table for each experimental condition for a
    given replacement condition, multiplying the better-than-chance confidence
    values and spreading the experimental conditions

    Parameters
    ----------
    ranking_table : pandas dataframe
        a [4 × n_features] × [task, stranger, feature, score, confidence_weight
        ] dataframe
    
    Returns
    -------
    weighted_table : pandas dataframe
        a n_important_features × [feature, 4 × score] dataframe
    """
    ranking_table = ranking_table.pivot_table(index='feature', columns=['task',
                     'stranger'])
    tasks = ['button', 'vocal']
    strangers = ['w', 'no']
    conditions = []
    columns = []
    for task in tasks:
        for stranger in strangers:
            conditions.append((task, stranger))
    for condition in conditions:
        columns.append(pd.Series(data = ranking_table.loc[:,(('score',) +
                       condition)] * ranking_table.loc[:,(('confidence_weight',
                       ) + condition)], name = '_'.join(list(condition))))
    weighted_table = pd.concat(columns, axis=1)
    weighted_table['mean_importance'] = weighted_table.mean(1)
    weighted_table = weighted_table.loc[weighted_table.mean_importance > 0]
    weighted_table.sort_values(by='mean_importance', ascending=False, 
                               inplace=True)
    return(weighted_table)

def get_weight_table(filename):
    """
    Function to get outputs from random forest models

    Parameters
    ----------
    filename : string
        path to random_forest output CSV
    
    Returns
    -------
    feature_table : pandas dataframe
        a n_features × [feature, score, confidence_weight] dataframe
    """
    # get feature and score from *feature_ranking.csv
    feature_table = pd.read_csv(filename, header=None, names=["feature",
                    "score"])
    # add confidence_weight from *feature_ranking_score.txt
    with open(''.join([filename.strip('.csv'), '_score.txt']), 'r') as f:
        feature_table["confidence_weight"] = float(f.readline().split('[')[0])
    return feature_table

def run_and_save(fs_path, table):
    print(''.join(["\ue316 Exporting", fs_path]))
    if not os.path.exists(os.path.dirname(fs_path)):
        os.makedirs(os.path.dirname(fs_path))
    table.to_csv(fs_path)

# ============================================================================
if __name__ == '__main__':
    # set directory of data
    global data_dir
    configs = ['emobase', 'ComParE_2016']
    for config in configs:
        data_dir = os.path.abspath(os.path.join('../openSMILE_preprocessing/'
                'noise_replacement/replacement_test_outputs/adults_replaced/'
                'summary/', config, 'random_forests'))
        main(config)