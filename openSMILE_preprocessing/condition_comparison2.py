#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
condition_comparison2.py

Functions to compare openSMILE outputs for two recording methods.

Authors:
    – Jon Clucas, 2016–2017 (jon.clucas@childmind.org)
    – Arno Klein, 2016 (arno.klein@childmind.org)
    – Bonhwang Koo, 2016 (bonhwang.koo@childmind.org)

© 2016–2017, Child Mind Institute, Apache v2.0 License

@author: jon.clucas
"""
import arff_csv_to_pandas as actp, math, numpy as np, os, pandas as pd

def build_dataframe(wd, config_file, condition, methods, entity):
    """
    Function to pull openSMILE output csv into a pandas dataframe

    Parameters
    ----------
    wd : string
        working directory

    config_file : string
        openSMILE configuration file filename

    condition : string
        ["sentences", "word_list"]

    methods : list
        ["PØNE__Canon", "Sony"]

    Returns
    -------
    d : pandas dataframe
        a dataframe for the relevant set of files and features
    """

    flag = False
    for method in methods:
        try:
            filepath = os.path.join(wd, condition, config_file)
            for file in os.listdir(filepath):
                if (os.path.basename(file).endswith(".csv")) and (entity in
                    file) and (method in file):
                    s = actp.get_oS_data(os.path.join(filepath, file), method,
                                         config_file, " > ".join([condition,
                                         entity]))
                    if flag == False:
                        d = s.to_frame()
                        flag = True
                    else:
                        d = d.join(s.to_frame())
        except FileNotFoundError as e404:
            pass
    if flag:
        # transpose dataframe
        d = d.T
        # convert numeric strings to numeric data
        d = d.apply(pd.to_numeric, errors='ignore')
        return(d)
    else:
        return None

def main():
    # set path
    op_path = ("/Volumes/Jon.Clucas/recorders/recorder_test/outputs")
    dataframes = iterate_through()
    list_of_dataframes = []
    for dataframe in dataframes:
        # export dataframe to csv
        dataframe[1].to_csv(os.path.join(op_path, ".".join([dataframe[0],
                            "csv"])))
        # tell which config_file+condition is being processed
        print(dataframe[0])
        # get mean absolute deviation for each column
        mad_ranks = mean_absolute_deviation_rank(dataframe[1])
        # output results to csv file
        mad_ranks.to_csv(os.path.join(op_path, "".join([dataframe[0],
                         "_mad_rank.csv"])))
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
                          'sum(MAD)'].rank(method='min', na_option='bottom',
                           ascending=True, numeric_only=True).astype('int')
        mad_ranks_summary['rank(mean(MAD))'] = mad_ranks_summary[
                          'mean(MAD)'].rank(method='min', na_option='bottom',
                           ascending=True, numeric_only=True).astype('int')
        mad_ranks_summary['rank(median(MAD))'] = mad_ranks_summary[
                          'median(MAD)'].rank(method='min', na_option=
                          'bottom', ascending=True, numeric_only=True).astype(
                          'int')
        mad_ranks_summary = mad_ranks_summary.sort_values(by=
                            'rank(sum(MAD))', ascending=True)
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
    wd = "/Volumes/Jon.Clucas/recorders/recorder_test"
    # set conditions
    conditions = ["sentences", "word_list"]
    # set methods
    methods = ["RODE__Canon", "Sony"]
    # set entities
    entities = ["Arno_", "ArnoD", "ArnoR", "ArnoU", "Curt", "David", "group",
                "Helen", "Jasmine", "Jon", "Karina", "Lindsay"]
    # set config files
    config_files = ["emobase", "ComParE_2016"]
    dataframes = []
    for config_file in config_files:
        for entity in entities:
            for condition in conditions:
                p = build_dataframe(wd, config_file, condition, methods,
                                entity)
                if type(p) != type(None):
                    dataframes.append(["_".join([config_file, condition,
                                      entity]), p])
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