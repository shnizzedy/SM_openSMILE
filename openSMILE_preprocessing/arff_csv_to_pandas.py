#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
arff_csv_to_pandas.py

Functions to import openSMILE outputs to Python pandas.

Authors:
    – Jon Clucas, 2016 (jon.clucas@childmind.org)
    – Arno Klein, 2016 (arno.klein@childmind.org)
    – Bonhwang Koo, 2016 (bonhwang.koo@childmind.org)

© 2016, Child Mind Institute, Apache v2.0 License

Created on Thu Dec  8 10:43:37 2016

@author: jon.clucas
"""
import arff, csv, os, pandas as pd, subprocess

def main():
    pass

def arff_to_pandas(arff_data, method, config_file, condition):
    """
    Function to convert python arff data into a pandas series

    Parameters
    ----------
    arff_data : string
        arff formatted data string

    method : string
        ["clone_all", "replaced_clone", "replaced_brownian", "replaced_pink",
             "replaced_stretch", "replaced_white", "replaced_timeshift",
             "silenced", "original"]

    config_file : string
        openSMILE configuration file filename

    condition : string
        ["ambient", "noise", "only_ambient_noise"]

    Returns
    -------
    oS_series : pandas series
        pandas series
    """
    indicies = []
    for attribute in arff_data["attributes"]:
        indicies.append(attribute[0])
    return(pd.Series(arff_data["data"][0], indicies, name = " > ".join([
           config_file, condition, method])))

def build_dataframe(wd, config_file, condition, methods):
    """
    Function to pull openSMILE output csv into a pandas dataframe

    Parameters
    ----------
    wd : string
        working directory

    config_file : string
        openSMILE configuration file filename

    condition : string
        ["ambient", "noise"]

    methods : list
        ["clone_all", "replaced_clone", "replaced_brownian", "replaced_pink",
         "replaced_stretch", "replaced_white", "replaced_timeshift",
         "silenced"]

    Returns
    -------
    d : pandas dataframe
        a dataframe for the relevant set of files and features
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

def get_oS_data(csvpath, method, config_file, condition):
    """
    Function to pull openSMILE output csv into a pandas series

    Parameters
    ----------
    csvpath : string
        absolute path to csv file

    method : string
        ["clone_all", "replaced_clone", "replaced_brownian", "replaced_pink",
             "replaced_stretch", "replaced_white", "replaced_timeshift",
             "silenced", "original"]

    config_file : string
        openSMILE configuration file filename

    condition : string
        ["ambient", "noise", "only_ambient_noise"]

    Returns
    -------
    oS_series : pandas series
    """
    try:
        # print(''.join(["Loading ", csvpath, '\n']))
        oS_data = arff.load(open(csvpath))
    except arff.BadLayout:
        # remove index column
        temp_data = ""
        with open(csvpath, 'r') as csvfile:
            # print(''.join(["Loading ", csvpath, '\n']))
            csv_reader = csv.reader(csvfile)
            temp_i = 0
            temp_label = ''
            for row in csv_reader:
                if temp_label != '@data':
                    if((len(row[0]) == 0) or (int(row[0]) == 0) or (int(row[
                       0]) == int(temp_i) + 1)):
                        temp_data = "".join([temp_data, row[1], "\n"])
                    else:
                        temp_data = "".join([temp_data, row[0], row[1]])
                    if(len(row[0]) != 0):
                        temp_i = row[0]
                    temp_label = row[1][:5]
                else:
                    temp_data = "".join([temp_data, row[1], ','])
            temp_data = temp_data[:-1]
        tempcsv = "temp.csv"
        tof = open(tempcsv, "w")
        tof.write(temp_data)
        tof.close()
        oS_data = replace_unknown(tempcsv)
    except arff.BadAttributeType:
        # replace "unknown" attribute type with "string" attribute type
        oS_data = replace_unknown(csvpath)
    return arff_to_pandas(oS_data, method, config_file, condition)
    
def replace_unknown(arff_path):
    """
    Function to pull openSMILE output csv into a pandas series

    Parameters
    ----------
    arff_path : string
        absolute path to csv file

    Returns
    -------
    oS_data : string
        arff formatted data string
    """
    temp_oS = open(arff_path, 'r')
    temp_oS_lines = temp_oS.readlines()
    temp_oS_string = ""
    for temp_oS_line in temp_oS_lines:
        words = temp_oS_line.split()
        if(len(words) == 3):
            if ((words[0] == "@attribute") and (words[2] == "unknown")):
                temp_oS_string = "".join([temp_oS_string,
                                         " ".join([words[0], words[1],
                                         "string\n"])])
            else:
                temp_oS_string = "".join([temp_oS_string, temp_oS_line])
        else:
            temp_oS_string = "".join([temp_oS_string, temp_oS_line])
    tempcsv = "temp.csv"
    tof = open(tempcsv, "w")
    tof.write(temp_oS_string)
    tof.close()
    oS_data = arff.loads(open(tempcsv))
    subprocess.run("rm temp.csv", shell=True)
    return(oS_data)

# ============================================================================
if __name__ == '__main__':
    main()