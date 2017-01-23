#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
openSMILE_dir_to_csv.py

Script to format openSMILE emobase *.csv output for a given set of files into a
single csv. Also returns the data as a pandas dataframe.

Created on Mon Jan 23 10:43:34 2017

Author:
        – Jon Clucas, 2017 (jon.clucas@childmind.org)

© 2017, Child Mind Institute, Apache v2.0 License
"""

import argparse, csv, os, pandas as pd, scipy.spatial, subprocess

def oS_csv_reformat(oS_csv, first):
    """
    Function to get features from openSMILE emobase configuration file csv
    outputs.

    Parameters
    ----------
    csv_file : string
        absolute path to a *.csv openSMILE output file

    first : boolean
        if this is the first csv of the set, `True`; otherwise, `False`

    Returns
    -------
    data : pandas dataframe or list
        if `first`, a dataframe with feature names, types, and csv values;
        if !`first`, a list of csv values.
    """
    print(oS_csv)
    if first:
        header = []
    #    type_header = []
    temp_list = []
    # initialize data_flag
    data_flag = False
    # read file
    at_at = "@attribute "
    with open(oS_csv, 'r') as f:
         # open file for reading
        reader = csv.reader(f)
        for index, row in enumerate(reader):
            if first:
                header_element = ''.join(row)
                if header_element.startswith(at_at):
                    he1, he2 = str(header_element.split(at_at)[1]).split(' ')
                    header.append(str(he1))
     #               if he2 != "unknown":
     #                   type_header.append(str(he2))
     #               else:
     #                   type_header.append("string")
            if data_flag:
                # read data row
                temp_list.append(row)
            if ''.join(row).startswith("@data"):
                data_flag = True
    if first:
        data = pd.DataFrame(data=temp_list[1], index=header, columns=[
                            os.path.basename(oS_csv).rstrip('.csv').casefold(
                           )])
        return(data)
    else:
        return(temp_list[1])


def oS_dir_to_csv(top_dir):
    """
    Function collect all openSMILE output csv files in a given top-level
    directory into a single csv file that also includes some summary columns
    with one column for each csv in the original directory.

    Parameters
    ----------
    top_dir : string
        absolute path to a directory of *.csv openSMILE output files

    Outputs
    -------
    (top_dir + `/collected/all-collected.csv`) : csv file
        a csv file containing all of the data from the input files and some
        added summary columns

    Returns
    -------
    collected_data : pandas dataframe
        the exported *.csv as a pandas dataframe
    """
    cols = []
    col_dir = os.path.join(top_dir, "collected")
    if not os.path.exists(col_dir):
        os.makedirs(col_dir)
    collected_data = None
    for i, file in enumerate(os.listdir(top_dir)):
        if file.casefold().endswith('.csv'.casefold()):
            if i == 0:
                collected_data = oS_csv_reformat(os.path.join(top_dir, file),
                                 True)
            else:
                collected_data[os.path.basename(file).rstrip('.csv').casefold(
                               )] = oS_csv_reformat(os.path.join(top_dir,
                               file), False)
    collected_data = collected_data.apply(pd.to_numeric, errors='coerce')
    for index, column in enumerate(list(collected_data)):
        if index > 0:
            cols.append(column)
    collected_data['mean'] = collected_data[cols].mean(axis=1)
    collected_data['median'] = collected_data[cols].median(axis=1)
    collected_data['std'] = collected_data[cols].std(axis=1)
    collected_data['mad'] = collected_data[cols].mad(axis=1)
    collected_data.sort_values(by='mad', axis=0, ascending=False, inplace=True)
    collected_data.to_csv(os.path.join(col_dir, "all_collected.csv"))
    return collected_data

def main():
    # script can be used from commandline.
    parser = argparse.ArgumentParser(description='get directory')
    parser.add_argument('in_dir', metavar='in_dir', type=str)
    arg = parser.parse_args()
    if os.path.exists(os.path.join(arg.in_dir, ".DS_Store")):
        shell_command = ''.join(['rm ', os.path.join(arg.in_dir, ".DS_Store")])
        print(shell_command)
        subprocess.run(shell_command, shell = True)
    oS_dir_to_csv(arg.in_dir)

# ============================================================================
if __name__ == '__main__':
        main()