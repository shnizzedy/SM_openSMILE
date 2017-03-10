#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
histograms.py

Histograms to explore weighted feature rankings produced by random forests in
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
from SM_openSMILE.utilities.cmi_color_pallette import cmi_colors
import matplotlib.pyplot as plt, pandas as pd, numpy as np, math

def main():
    configs = ['emobase', 'ComParE_2016']
    replacements = ['removed', 'replaced_clone', 'replaced_pink', 'timeshifted'
                    ]
    for i, replacement in enumerate(replacements):
        replacements[i] = '_'.join(['adults', replacement])
    for config in configs:
        dfs = []
        for replacement in replacements:
            dfs.append(get_df_from_file(get_filepath(config, replacement),
                       replacement))
        for replacement in [*replacements, 'adults', 'original']:
            dfs.append(get_df_from_file(get_filepath(config, replacement, 'ltd'
                       ), '/'.join(['ltd', replacement])))
        dfs.append(get_df_from_file(get_filepath(config, 'unmodified',
                   'unmodified'), 'unmodified'))
        build_histogram(get_features(dfs))

def build_histogram(df):
    for feature, sdf in df.groupby(level=0):
        dim = round(math.log(sdf.T.shape[1])**(2+(1/3)))
        dim = (dim, dim)
        axes = pd.DataFrame.hist(sdf.T, figsize=(dim), color=
                     cmi_colors()[0])
        axes[0][0].set_title(feature)
        axes[0][0].legend()
        axes[0][0].show()
            

def get_features(dfs):
    """
    Function to cross-tabulate feature dataframes and count by features.

    Parameters
    ----------
    dfs : list of pandas dataframes
        a list of dataframes to compare
        
    values : list
        a list of column headers to cross-tabulate by
   
    Returns
    -------
    p_t : pandas dataframe
        a multi-indexed dataframe of ['base_feature' × 'coefficient' ×
        'summary_type'] × ['replacement' × 'condition'] predictive counts
    """
    df = pd.concat(dfs)
    conditions = ['button_w', 'button_n', 'vocal_w', 'vocal_no']
    features = ['base_feature', 'coefficient', 'summary_type']
    return pd.pivot_table(df, values=conditions, index=features,
          columns=['replacement'], aggfunc='count', fill_value=0)
    

def get_df_from_file(filepath, replacement="unmodified"):
    """
    Function to get weighted summary table from filepath.

    Parameters
    ----------
    filepath : string
        absolute path to the weighted dataframe csv
        
    replacement : string
        adult replacement method
   
    Returns
    -------
    df : pandas dataframe
        a features × ['base_feature', 'coefficient', 'summary_type',
        'button_w', 'button_no', 'vocal_w', 'vocal_no'] pandas dataframe
    """
    df = pd.read_csv(filepath)
    df['base_feature'] = df['feature'].str.extract('(.*(?=_sma))', expand=True)
    df['coefficient'] = df['feature'].str.extract('([\d+])', expand=True)
    df['summary_type'] = df['feature'].str.extract('((?<=_).*?)*(?=\s)',
                         expand=True)
    df['replacement'] = replacement
    df = df.ix[:, ['base_feature', 'coefficient', 'summary_type', 'button_w',
         'button_no', 'vocal_w', 'vocal_no', 'replacement']]
    return df

def get_filepath(config, replacement, special=None):
    """
    Function to get filepaths for weighted summary tables.

    Parameters
    ----------
    config : string
        openSMILE config file basename
    
    replacement : string
        adult replacement method
        
    special : string or None
        ['ltd', 'unmodified', None] if we're looking at something other than
        the cleaned data with the unmodified data filled in
    
    Returns
    -------
    filepath : string
        absolute path to the weighted dataframe csv
    """
    if not special:
        return os.path.join(topdir, config, 'feature_summary', '_'.join([
               replacement, 'weighted.csv']))
    else:
        return os.path.join(topdir, config, 'feature_summary', special, 
               '_'.join([replacement, 'weighted.csv']))

# ============================================================================
if __name__ == '__main__':
    global topdir
    topdir = os.path.abspath(os.path.join('../openSMILE_analysis/'
             'random_forests/predict_SM/long_files/summary'))
    main()