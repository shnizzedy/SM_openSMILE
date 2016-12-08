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
import arff_csv_to_pandas as actp, pandas as pd

def main():
    dataframes = iterate_through()
    for dataframe in dataframes:
        print(dataframe[0])
        mean_absolute_deviation_rank(dataframe[1])
        
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
    print(dataframe.mad)

# ============================================================================
if __name__ == '__main__':
    main()