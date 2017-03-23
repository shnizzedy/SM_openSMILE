#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
barh.py

Script to build horizontal bar charts to explore weighted feature rankings
produced by random forests in trees.py

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
import math, pandas as pd, matplotlib.pyplot as plt
from SM_openSMILE.cfg import topdir


def main():
    configs = ['emobase', 'ComParE_2016']
    replacements = ['removed', 'replaced_clone', 'replaced_pink', 'timeshifted'
                    ]
    for i, replacement in enumerate(replacements):
        replacements[i] = '_'.join(['adults', replacement])
    for config in configs:
        dfs, ltd_dfs, adults_dfs, unmod = collect_dfs(config, replacements)
        for dlist in [dfs, ltd_dfs, adults_dfs]:
            dlist.append(unmod)
        build_barh(get_features(dfs), config, replacements)
        build_barh(get_features(ltd_dfs), config, replacements, 'ltd')
        build_barh(get_features(adults_dfs), config, ['adults', 'unmodified'],
                   'adults')
        
def collect_dfs(config, replacements):
    """
    Function to collect dataframes to build relevant plots.
    
    Parameters
    ----------
    config : string
        openSMILE config file
        
    replacements : list of strings
        list of replacement methods
        
    Returns
    -------
    dfs : list of pandas dataframes
        list of cleaned dataframes
        
    ltd_dfs : list of pandas dataframes
        list of limited dataframes excluding unmodified files
        
    adults_dfs : list of pandas dataframes
        list of dataframes in which only adults speak
        
    unmod : pandas dataframe
        dataframe of unmodified files  
    """
    dfs, ltd_dfs, adults_dfs = [], [], []
    for replacement in replacements:
        dfs.append(get_df_from_file(get_filepath(config, replacement),
                   replacement))
    for replacement in replacements:
        ltd_dfs.append(get_df_from_file(get_filepath(config, replacement,
                       'ltd'), '/'.join(['ltd', replacement])))
    unmod = get_df_from_file(get_filepath(config, 'unmodified','unmodified'),
            'unmodified')
    adults_dfs.append(get_df_from_file(get_filepath(config, 'adults','ltd'),
                      '/'.join(['ltd', 'adults'])))
    return(dfs, ltd_dfs, adults_dfs, unmod)

def build_barh(df, config, replacements, special=None):
    """
    Function to prepare a dataframe for plotting and to send that prepared
    dataframe to the plot funcion (plot_barh) for plotting and saving in as
    many forms as is appropriate.

    Parameters
    ----------
    df : pandas dataframe
        dataframe to prepare for plotting
        
    config : string
        openSMILE config file
        
    replacements : list
        noise replacement methods
        
    special : string or None
        'ltd' or None
   
    Returns
    -------
    None
    """
    conditions = ['button_w', 'button_no', 'vocal_w', 'vocal_no']
    # plot each condition with replacements as colors
    for condition in conditions:
        sdf = df.xs(condition, axis=1)
        # get rid of non-predictive features
        sdf = sdf[sdf > 0].dropna(how='all')
        if special:
            out_path = os.path.join(topdir, config, 'feature_summary', special,
                       '_'.join([condition, 'complete.svg']))
        else:
            out_path = os.path.join(topdir, config, 'feature_summary', ''.join(
                    [condition, '.svg']))
        if not os.path.exists(os.path.dirname(out_path)):
            os.makedirs(os.path.dirname(out_path))
        title = " :\n".join(["weighted random forest values", config, condition
                ])
        plot_barh(sdf, title, out_path)
        
        # plot conditions in which all replacements returned values above the
        # median
        top_all = sdf[sdf > sdf.sum(axis=1).median()].dropna(how='any')
        out_path_all = ''.join([out_path.strip('.svg'), '_top_all.svg'])
        plot_barh(top_all, title, out_path_all)
        
        # plot conditions in which any replacements returned values above the
        # median
        top_any = sdf[sdf > sdf.sum(axis=1).median()].dropna(how='all')
        out_path_any = ''.join([out_path.strip('.svg'), '_top_any.svg'])
        plot_barh(top_any, title, out_path_any)
        
    if special:
        for i, replacement in enumerate(replacements):
            if replacement != 'unmodified':
                replacements[i] = '/'.join(['ltd', replacement])
                
    # plot each replacement with conditions as colors
    for replacement in replacements:
        sdf = df.xs(replacement, axis=1, level=1)
        out_path = os.path.join(topdir, config, 'feature_summary', ''.join(
                   [replacement, '.svg']))
        if not os.path.exists(os.path.dirname(out_path)):
            os.makedirs(os.path.dirname(out_path))
        title = " :\n".join(["weighted random forest values", config,
                replacement])
        plot_barh(sdf, title, out_path)
        
        # plot conditions in which all conditions returned values above the
        # median
        top_all = sdf[sdf > sdf.sum(axis=1).median()].dropna(how='any')
        out_path_all = ''.join([out_path.strip('.svg'), '_top_all.svg'])
        plot_barh(top_all, title, out_path_all)
        
        # plot conditions in which any conditions returned values above the
        # median
        top_any = sdf[sdf > sdf.sum(axis=1).median()].dropna(how='all')
        out_path_any = ''.join([out_path.strip('.svg'), '_top_any.svg'])
        plot_barh(top_any, title, out_path_any)
        
        # plot each replacement and condition combination individually
        for condition in conditions:
            tdf = sdf.xs(condition, axis=1)
            tdf = tdf[tdf > 0]
            out_path = os.path.join(topdir, config, 'feature_summary',
                       ''.join([replacement, '_', condition, '.svg']))
            if not os.path.exists(os.path.dirname(out_path)):
                os.makedirs(os.path.dirname(out_path))
            title = " :\n".join(["weighted random forest values", config, 
                    replacement, condition])
            plot_barh(tdf, title, out_path)
            
            # plot conditions in which replacement and condition returned
            # values above the median
            top_any = tdf[tdf > tdf.median()]
            out_path_any = ''.join([out_path.strip('.svg'), '_top_any.svg'])
            plot_barh(top_any, title, out_path_any)
        
def plot_barh(sdf, title, out_path):
    """
    Function to plot a horizontal barplot and save said plot.

    Parameters
    ----------
    sdf : pandas dataframe
        dataframe to plot
        
    title : string
        plot title
        
    out_path : string
        path of image file save location
   
    Returns
    -------
    None
    
    Output
    ------
    out_path : image
        image file
    """
    print(title.replace("\n"," "))
    print(sdf.shape)
    plt.figure()
    if sdf.shape[0] > 0:
        if len(sdf.shape) == 2:
            # color per condition and/or replacement method
            color = cmi_colors()
            # plot dimensions: f(maximum value) × f(# of features)
            dim = (abs(sdf.sum(axis=0)).max()*25, math.log(sdf.shape[0])**3)
        else:
            # all bars one color
            color = cmi_colors()[0]
            # plot dimensions: f(maximum value) × f(# of features)
            dim = (abs(sdf.max())*500, math.log(sdf.shape[0])**3)
        ax = sdf.plot.barh(figsize=dim, color=color, stacked=True, title=title
             )
        ax.legend(loc=3, fancybox=True, shadow=True, bbox_to_anchor=(-0.01,
                  -0.01))    
    plt.savefig(out_path, bbox_inches="tight")
    plt.close()

def get_features(dfs):
    """
    Function to cross-tabulate feature dataframes and sum by features.

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
    conditions = ['button_w', 'button_no', 'vocal_w', 'vocal_no']
    features = ['base_feature', 'coefficient', 'summary_type']
    return pd.pivot_table(df, values=conditions, index=features,
          columns=['replacement'], aggfunc='sum', fill_value=0)
    

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
    if special:
        special_path = os.path.join(topdir, config, 'feature_summary', special, 
                       '_'.join([replacement, 'weighted.csv']))
        if os.path.exists(special_path):
            return special_path
    return os.path.join(topdir, config, 'feature_summary', '_'.join([
           replacement, 'weighted.csv']))

# ============================================================================
if __name__ == '__main__':
    main()