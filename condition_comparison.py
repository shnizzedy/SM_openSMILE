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
import arff_csv_to_pandas as actp, math, numpy as np, pandas as pd

def main():
    dataframes = iterate_through()
    for dataframe in dataframes:
        print(dataframe[0])
        print(mean_absolute_deviation_rank(dataframe[1]))
        
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
    conditions = ["ambient", "noise"]
    # set methods
    methods = ["clone_all","replaced_clone","replaced_brownian","replaced_pink",
             "replaced_stretch", "replaced_white", "silenced"]
    # set config files
    config_files = ["emobase", "ComParE2016"]
    dataframes = []
    for config_file in config_files:
        for condition in conditions:
            dataframes.append(["_".join([config_file,condition]),
                               actp.build_dataframe(wd,config_file,condition,
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
    mad_series = pd.Series(index=dataframe.columns)
    mad_rank = pd.DataFrame(index=dataframe.index, columns=dataframe.columns)
    dataframe = dataframe.apply(pd.to_numeric, errors='coerce')
    for column in dataframe.columns:
        mad_series[column] = dataframe[column].mad()
    for index in dataframe.index:
        for column in dataframe.columns:
            try:
                mad_rank.set_value(index,column,(abs(math.floor(
                               dataframe.get_value(index,column) - mad_series[column]))))
            except:
                mad_rank.set_value(index,column,np.nan)
    return mad_rank

# ============================================================================
if __name__ == '__main__':
    main()