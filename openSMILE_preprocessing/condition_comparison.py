#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
condition_comparison.py

Functions to compare openSMILE outputs for various noise replacement methods.

Authors:
    – Jon Clucas, 2016 (jon.clucas@childmind.org)
    – Arno Klein, 2016 (arno.klein@childmind.org)
    – Bonhwang Koo, 2016 (bonhwang.koo@childmind.org)

© 2016, Child Mind Institute, Apache v2.0 License

Created on Tue Dec  6 17:53:01 2016

@author: jon.clucas
"""
import arff_csv_to_pandas as actp, math, numpy as np, os, pandas as pd

def main():
    # set path
    op_path = ("/Volumes/Jon.Clucas/openSMILE/SM_openSMILE/"
               "openSMILE_preprocessing/noise_replacement/"
               "replacement_test_outputs")
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

def iterate_through():
    """
    Function to iterate through openSMILE configuration files and noise
    conditions.

    Parameters
    ----------
    none

    Returns
    -------
    dataframes : list
        A list of (config_files × conditions) pairs of
        config_file+condition ([0]) and pandas dataframe ([1])
    """
    # set working directory
    wd = "/Volumes/data/Research/CDB/openSMILE/Audacity/test"
    # set conditions
    conditions = ["ambient", "noise", "only_ambient_noise"]
    # set methods
    methods = ["clone_all", "replaced_clone", "replaced_brownian",
               "replaced_pink", "replaced_stretch", "replaced_white",
               "replaced_timeshift", "silenced"]
    # set config files
    config_files = ["emobase", "ComParE_2016"]
    dataframes = []
    for config_file in config_files:
        for condition in conditions:
            dataframes.append(["_".join([config_file, condition]),
                               actp.build_dataframe(wd, config_file, condition,
                                                    methods)])
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