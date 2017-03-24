#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
replacement_comparison.py

Functions to compare openSMILE outputs for various noise replacement methods
for each waveform in the sample.

Authors:
    – Jon Clucas, 2017 (jon.clucas@childmind.org)

© 2017, Child Mind Institute, Apache v2.0 License

@author: jon.clucas
"""

import numpy as np, os, pandas as pd, sys
if os.path.abspath('../../') not in sys.path:
    if os.path.isdir(os.path.join(os.path.abspath('../..'), 'SM_openSMILE')):
        sys.path.append(os.path.abspath('../..'))
    elif os.path.isdir(os.path.join(os.path.abspath('..'), 'SM_openSMILE')):
        sys.path.append(os.path.abspath('..'))
    elif os.path.isdir('SM_openSMILE'):
        sys.path.append(os.path.abspath('.'))
from SM_openSMILE.openSMILE_preprocessing.noise_replacement import \
     condition_comparison_nr_all as cc, nr_box_plots as nbp
from SM_openSMILE.cfg import conditions, oSdir, configs
adults_replaced = os.path.dirname(oSdir)

def main():
    # collect_mad_ranks()
    plot_mad_ranks()
    
def collect_mad_ranks():
    """
    Function to collect median absolute deviations for all [replacement ×
    condition]s for each configuration for each URSI
    
    Parameters
    ----------
    None
    
    Returns
    -------
    None
    
    Outputs
    -------
    csv files
        two csv files per URSI per configuration file: one for totals, and one
        for summaries
    """
    replacements = ['removed', 'replaced_clone', 'replaced_pink', 'timeshifted'
                    ]
    for i, replacement in enumerate(replacements):
        replacements[i] = '_'.join(['adults', replacement])
    replacements = [*replacements, 'adults']
    list_of_dataframes = []
    for URSI in os.listdir(adults_replaced):
        if URSI not in ['.DS_Store', 'summary']:
            for condition in conditions:
                for config_file in configs:
                    URSI_files = []
                    for method in replacements:
                        method_dir = os.path.join(adults_replaced, URSI,
                                     'openSMILE_outputs', config_file,
                                     method)
                        if os.path.isdir(method_dir):
                            if len(URSI_files) == 0:
                                or_dir = os.path.join(adults_replaced, URSI,
                                         'openSMILE_outputs', config_file,
                                         'original')
                                if os.path.isdir(or_dir):
                                    for or_file in os.listdir(or_dir):
                                        if condition in or_file:
                                            URSI_files.append(os.path.join(
                                                              or_dir, or_file))
                            for csv_file in os.listdir(method_dir):
                                csv_path = os.path.join(method_dir, csv_file)
                                if condition in csv_file and csv_path not in \
                                   URSI_files: 
                                    URSI_files.append(csv_path)
                    if len(URSI_files) == 6:
                        print(''.join(["Processing ", URSI, ", ", condition,
                              " : ", config_file]))
                        list_of_dataframes.append(["_".join([URSI, config_file]
                                                  ), cc.build_dataframe(URSI,
                                                  ['original', *replacements],
                                                  config_file, URSI_files)])
    cc.mad_rank_analyses([list_of_dataframes], adults_replaced)
    
def plot_mad_ranks():
    """
    Function to build boxplots for the outputs of collect_mad_ranks().
    
    Parameters
    ----------
    None
    
    Returns
    -------
    None
    
    Outputs
    -------
    svg files
        one svg file for each config file
    """
    for config in configs:
        for y in ["sum(MAD)", "mean(MAD)"]:
            out_path = os.path.join(oSdir, 'mad_ranks', config)
            if not os.path.exists(out_path):
                os.makedirs(out_path)
            nbp.plot(sum_mad_ranks(config), out_path, y, "csv")
            nbp.plot(sum_mad_ranks(config), out_path, y)
    
def sum_mad_ranks(config):
    """
    Function to build boxplots for the outputs of collect_mad_ranks().
    
    Parameters
    ----------
    config : string
        openSMILE config file
    
    Returns
    -------
    df : pandas dataframe
        pandas dataframe totalling all relevant summaries
    
    Outputs
    -------
    csv files
        one csv file for each config file
    """
    df = pd.DataFrame()
    for URSI in os.listdir(adults_replaced):
        mrp = os.path.join(adults_replaced, URSI, 'mad_ranks', config,
              '_'.join([URSI, config, 'mad_rank_summary.csv']))
        if os.path.exists(mrp):
            if(df.shape == (0, 0)):
                df = pd.read_csv(mrp, index_col=0)
            else:
                df = df.append(pd.read_csv(mrp, index_col=0))
    indices = (np.vstack(df.index.to_series().str.split(" > ").values))
    df['config'] = indices[:,0]
    df['csv'] = indices[:,1]
    df['method'] = indices[:,2]
    df.sort_values(by='sum(MAD)', inplace=True)
    summed = df.groupby(by='method').sum().sort_values(by='sum(MAD)')
    out_path = os.path.join(oSdir, 'mad_ranks', '_'.join([config,
               'mad_rank_summary.csv']))
    if not os.path.exists(os.path.dirname(out_path)):
        os.makedirs(os.path.dirname(out_path))
    summed.to_csv(out_path)
    return(df)

# ============================================================================
if __name__ == '__main__':
    main()