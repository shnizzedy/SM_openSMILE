#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
condition_comparison_nr_all.py

Functions to compare openSMILE outputs for various noise replacement methods
for each waveform in the sample.

Authors:
    – Jon Clucas, 2016–2017 (jon.clucas@childmind.org)
    – Arno Klein, 2016–2017 (arno.klein@childmind.org)
    – Bonhwang Koo, 2016 (bonhwang.koo@childmind.org)

© 2016–2017, Child Mind Institute, Apache v2.0 License

Created on Tue Dec  6 17:53:01 2016

@author: jon.clucas
"""
import math, numpy as np, os, pandas as pd, sys
sys.path.append(os.path.abspath('../../..'))
from SM_openSMILE.openSMILE_preprocessing import arff_csv_to_pandas as actp


def main():
    # set path
    op_path = (os.path.abspath(
               "replacement_test_outputs/ambient_clip_replaced"))
    # initialize list of dataframes
    list_of_dataframes = []
    for participant in os.listdir(op_path):
        if participant != ".DS_Store":
            list_of_dataframes.append(iterate_through(os.path.join(op_path,
                                      participant)))
    mad_rank_analyses(list_of_dataframes, op_path)
            
def mad_rank_analyses(list_of_dataframes, op_path):
    """
    Function to analyze dataframes of openSMILE outputs

    Parameters
    ----------
    list_of_dataframes : list of list of tuples of (string, pandas dataframe)s
        openSMILE output dataframes to compare
        
    op_path : string
        path to start from when saving outputs

    Returns
    -------
    None
    
    Outputs
    -------
    csv files
        csv files to compare openSMILE outputs
    """
    list_of_analyses = []
    for dataframes in list_of_dataframes:
        for dataframe in dataframes:
            URSI, config_file = dataframe[0].split('_', maxsplit=1)
            out_path = os.path.join(op_path, URSI, 'mad_ranks', config_file)
            if not os.path.exists(out_path):
                os.makedirs(out_path)
            # tell which config_file+condition is being processed
            # print(''.join(['Analysing ', dataframe[0], '\n']))
            # get mean absolute deviation for each column
            mad_ranks = mean_absolute_deviation_rank(dataframe[1])
            # output results to csv file
            mad_ranks.to_csv(os.path.join(out_path, "".join([dataframe[0],
                             "_mad_rank.csv"])))
            # sum the rows
            mad_ranks_summary = mad_ranks.sum(axis=1).to_frame(name="sum(MAD)")
            # mean rows
            mad_ranks_summary['mean(MAD)'] = mad_ranks.mean(axis=1).to_frame(
                                             name="mean(MAD)")
            # median rows
            mad_ranks_summary['median(MAD)'] = mad_ranks.median(axis=1
                                               ).to_frame(name="median(MAD)")
            # rank the summary statistics
            mad_ranks_summary['rank(sum(MAD))'] = mad_ranks_summary['sum(MAD)'
                                                  ].rank(method='min',
                                                  na_option='keep',
                                                  ascending=True).astype('int')
            mad_ranks_summary['rank(mean(MAD))'] = mad_ranks_summary[
                                                   'mean(MAD)'].rank(method=
                                                   'min', na_option='keep',
                                                   ascending=True).astype('int'
                                                   )
            mad_ranks_summary['rank(median(MAD))'] = mad_ranks_summary[
                                                     'median(MAD)'].rank(method
                                                     ='min', na_option='keep',
                                                     ascending=True).astype(
                                                     'int')
            mad_ranks_summary = mad_ranks_summary.sort_values(by=
                                'rank(sum(MAD))', ascending=True)
            # output results to csv file
            mad_ranks_summary.to_csv(os.path.join(out_path, "".join([dataframe[
                                     0], "_mad_rank_summary.csv"])))
            list_of_analyses.append(mad_ranks_summary)
    all_analyses = pd.concat(list_of_analyses)
    # output all results to a single csv file
    all_analyses.to_csv(os.path.join(op_path, "mad_rank_summary_all.csv"))

def build_dataframe(URSI, methods, config_file, csv_files):
    """
    Function to pull openSMILE output csv into a pandas dataframe

    Parameters
    ----------
    URSI : string
        participant identifier
        
    method : list
        noise replacement methods

    config_file : string
        openSMILE configuration file filename

    csv_files : list
        list of paths to openSMILE output files

    Returns
    -------
    d : pandas dataframe
        a dataframe for the relevant set of files and features
    """
    first = True
    for method in methods:
        for csv_file in csv_files:
            print(''.join(["Loading ", csv_file]))
            if (os.path.basename(csv_file) != ".DS_Store" and method ==
                os.path.basename(os.path.dirname(csv_file))):
                s = actp.get_oS_data(csv_file, method,
                                     config_file, os.path.basename(csv_file
                                     ).rstrip('.csv'))
                try:
                    if first:
                        d = s.to_frame()
                        first = False
                    else:
                        d = d.merge(s.to_frame(), left_index=True,
                            right_index=True)
                except FileNotFoundError as e404:
                    print(''.join("Not found: ", csv_file))
    # transpose dataframe
    d = d.T
    # convert numeric strings to numeric data
    d = d.apply(pd.to_numeric, errors='ignore')

    return(d) 

def iterate_through(URSI):
    """
    Function to iterate through openSMILE configuration files and noise
    conditions.

    Parameters
    ----------
    URSI : string
        path to participant subdirectory

    Returns
    -------
    dataframes : list
        list of config_files ([0]) and pandas dataframes ([1])
    """
    # set working directory
    wd = os.path.join(URSI, "openSMILE_outputs")
    # extract URSI from path
    URSI = os.path.basename(URSI)
    # set conditions
    conditions = ["_button_no_", "_button_w_", "_vocal_no_", "_vocal_w_"]
    # set methods
    methods = ["no_beeps", "clone_fill", "sample_silenced", "timeshifted"]
    # set config files
    config_files = ["emobase", "ComParE_2016"]
    # initialize dataframes, URSI_files
    dataframes = []
    for condition in conditions:
        for config_file in config_files:
            URSI_files = []
            for method in methods:
                method_dir = os.path.join(wd, config_file, method)
                if os.path.isdir(method_dir):
                    for csv_file in os.listdir(method_dir):
                        if condition in csv_file:
                            URSI_files.append(os.path.join(method_dir, csv_file
                                              ))
            if len(URSI_files) > 0:
                print(''.join(["Processing ", URSI, ", ", condition, " : ",
                      config_file]))
                dataframes.append(["_".join([URSI, config_file]),
                                  build_dataframe(URSI, methods, config_file,
                                  URSI_files)])
    return dataframes

def mean_absolute_deviation_rank(dataframe):
    """
    Function to calculate the number of full mean average deviations each
    value is across each config_file+condition.

    Parameters
    ----------
    dataframe : pandas dataframe
        dataframe containing openSMILE output data

    Returns
    -------
    dataframe : pandas dataframe
        dataframe containing mean average deviation counts
    """
    mad_series = pd.Series(index = dataframe.columns)
    mad_rank = pd.DataFrame(index = dataframe.index, columns =
                            dataframe.columns)
    dataframe = dataframe.apply(pd.to_numeric, errors = 'coerce')
    for column in dataframe.columns:
        mad_series[column] = dataframe[column].mad()
    i = None
    for index in dataframe.index:
        if i is None:
            i = index
        for column in dataframe.columns:
            try:
                mad_rank.set_value(index, column, (abs(math.floor(
                               (dataframe.get_value(index, column) -
                                dataframe.get_value(i, column)) /
                                mad_series[column]))))
            except:
                mad_rank.set_value(index, column, np.nan)
    return mad_rank

# ============================================================================
if __name__ == '__main__':
    main()