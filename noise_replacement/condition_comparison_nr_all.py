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
        list_of_dataframes.append(iterate_through(os.path.join(op_path,
                                  participant)))
    print(list_of_dataframes)
    """
    dataframes = iterate_through()
    list_of_dataframes = []
    for dataframe in dataframes:
        # tell which config_file+condition is being processed
        print(dataframe[0])
        # get mean absolute deviation for each column
        mad_ranks = mean_absolute_deviation_rank(dataframe[1])
        # output results to csv file
        mad_ranks.to_csv(os.path.join(op_path,
                                    "".join([dataframe[0], "_mad_rank.csv"])))
        # sum the rows
        mad_ranks_summary = mad_ranks.sum(axis=1).to_frame(name = "sum(MAD)")
        # mean rows
        mad_ranks_summary['mean(MAD)'] = mad_ranks.mean(axis=1).to_frame(
                                      name = "mean(MAD)")
        # median rows
        mad_ranks_summary['median(MAD)'] = mad_ranks.median(axis=1).to_frame(
                                      name = "median(MAD)")
        # rank the summary statistics
        mad_ranks_summary['rank(sum(MAD))'] = mad_ranks_summary[
                          'sum(MAD)'].rank(method = 'min', na_option = 'keep',
                           ascending = True).astype('int')
        mad_ranks_summary['rank(mean(MAD))'] = mad_ranks_summary[
                          'mean(MAD)'].rank(method = 'min', na_option = 'keep',
                           ascending = True).astype('int')
        mad_ranks_summary['rank(median(MAD))'] = mad_ranks_summary[
                          'median(MAD)'].rank(method = 'min', na_option =
                          'keep', ascending = True).astype('int')
        mad_ranks_summary = mad_ranks_summary.sort_values(by =
                            'rank(sum(MAD))', ascending = True)
        # output results to csv file
        mad_ranks_summary.to_csv(os.path.join(op_path, "".join([dataframe[0],
                                 "_mad_rank_summary.csv"])))
        list_of_dataframes.append(mad_ranks_summary)
    dataframes = pd.concat(list_of_dataframes)
    # output all results to a single csv file
    dataframes.to_csv(os.path.join(op_path, "mad_rank_summary_all.csv"))
    """

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
    for csv_file in csv_files:
        s = actp.get_oS_data(csv_file, os.path.dirname(csv_file), config_file,
                             "ambient")
        try:
            if first:
                d = s.to_frame()
                first = False
            else:
                d.join(s.to_frame())
        except FileNotFoundError as e404:
            print(''.join("Not found: ", csv_file))
    # transpose dataframe
    d = d.T
    # convert numeric strings to numeric data
    d = d.apply(pd.to_numeric, errors='ignore')
    return(d)
            
        
    """
    if condition == 'only_ambient_noise':
        s = get_oS_data(os.path.join(wd, config_file,
            "only_ambient_noise_original.csv"), "original", config_file,
            condition)
    else:
        s = get_oS_data(os.path.join(wd, config_file, "full_original.csv"),
        "original", config_file, condition)
    d = s.to_frame()
    for method in methods:
        try:
            if condition == 'only_ambient_noise':
                s = get_oS_data(os.path.join(
                            wd, config_file,
                            condition, "".join([condition,
                            "_", method, ".csv"])), method, config_file,
                            condition)
            else:
                s = get_oS_data(os.path.join(
                                wd,config_file,
                                condition, "".join(["full_", condition,
                                "_", method, ".csv"])), method, config_file,
                                condition)
            d = d.join(s.to_frame())
        except FileNotFoundError as e404:
            pass
    # transpose dataframe
    d = d.T
    # convert numeric strings to numeric data
    d = d.apply(pd.to_numeric, errors='ignore')
    return(d)
    """

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
    wd = os.path.join(URSI, "openSMILE_output")
    # set methods
    methods = ["no_beeps", "clone_fill", "sample_silenced", "timeshifted"]
    # set config files
    config_files = ["emobase.conf", "ComParE_2016.conf"]
    # initialize dataframes, URSI_files
    dataframes = []
    URSI_files = []
    for config_file in config_files:
        for method in methods:
            method_dir = os.path.join(wd, config_file, method)
            for csv_file in os.listdir(method_dir):
                URSI_files.append(os.path.join(method_dir, csv_file))
        dataframes.append(build_dataframe(URSI, methods, config_file,
                          URSI_files))
    return dataframes
    """
    for config_file in config_files:
        for condition in conditions:
            dataframes.append(["_".join([config_file, condition]),
                               actp.build_dataframe(wd, config_file, condition,
                                                    methods)])
    return dataframes
    """

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
    """

# ============================================================================
if __name__ == '__main__':
    main()