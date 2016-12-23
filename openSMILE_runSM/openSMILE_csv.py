#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
openSMILE_csv.py

Script to format openSMILE emobase *.csv output combined with dx data into a
set of new [participant × file × feature × dx] *.csv files, one for each
experimental condition.

Short (segmented) and long (concatenated) outputs are handled separately.

Author:
        – Jon Clucas, 2016 (jon.clucas@childmind.org)

© 2016, Child Mind Institute, Apache v2.0 License
"""

import csv, os

def get_features(csv_file):
    """
    Function to get features from openSMILE emobase configuration file csv
    outputs.

    Parameters
    ----------
    csv_file : string
    filename of a *.csv emobase output file

    Returns
    -------
    temp_list : list
    list of features from emobase output file
    """
    with open(csv_file, 'r') as f:
        # open file for reading
        reader = csv.reader(f)
        # initalize list
        temp_list = []
        # initialize data_flag
        data_flag = False
        # read file
        for row in reader:
            if data_flag:
                # read data row
                temp_list = ''.join(row[1]).split(',')
            if row[1].endswith("@data"):
                # set data_flag
                data_flag = True
        # convert data from strings to floats
        for item in temp_list:
            try:
                item = float(item)
            # if not a number, do not convert
            except (TypeError, ValueError):
                pass
        # return feature list
        return temp_list


def get_dx(ursi, dx_dictionary = None):
    """
    Function to get a participant's diagnosis from a dictionary of diagnoses.

    Parameters
    ----------
    ursi : string
        a participant's URSI

    dx_dictionary : dictionary
        a dictionary of {['URSI']:['Dx?']} pairs

    Returns
    -------
    {['Dx?']} : string
        a diagnosis or an empty string
    """
    if dx_dictionary == None:
        dx_dictionary = get_dx_dictionary()
    try:
        return dx_dictionary[ursi]
    except (KeyError):
        return 'unknown'

def get_dx_dictionary():
    """
    Function to create a diagnosis dictionary from a csv file containing
    diagnoses.

    Parameters
    ----------
    None

    Returns
    -------
    dx_dictionary : dictionary
        a dictionary of {['URSI']:['Dx?']} pairs
    """
    # initialize diagnosis dictionary
    dx_dictionary = {}
    # absolute path to 2 column *.csv file with 'URSI' and 'Dx?' column headers
    dictionary_csv = ('/Volumes/data/Research/CDB/SM_Sound_Analysis/'
                      'SM_DX_summary_status_dx.csv')
    # read file into dictionary with URSI keys and Dx values
    with open(dictionary_csv, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            dx_dictionary[row['URSI']] = row['Dx?']
        return dx_dictionary

def create_sample_row(ursi, condition, config_file):
    """
    Function to create a row for a training set.

    Parameters
    ----------
    ursi : string
        a participant's URSI

    Returns
    -------
    sample_row_long : list
        an n_files × 1 list of
        n_features × 2 lists of [features],[diagnosis]

    sample_row_short : list
        an n_files × 1 list of
        n_features × 2 lists of [features],[diagnosis]
    """
    # initialize short and long sample rows
    sample_row_short = []
    sample_row_long = []
    # set absolute top directory for input *.csv files
    topdir = ('/Volumes/data/Research/CDB/SM_Sound_Analysis/all_audio_files/'
              'NEW/')
    # get diagnosis dictionary
    dx_dict = get_dx_dictionary()
    # find participant directory
    for dirs in os.listdir(topdir):
        if dirs == ursi:
            # set participant directory
            ursi_dir = os.path.join(topdir,dirs,''.join(['openSMILE_outputs/',
                                                         config_file]))
            # get participant diagnosis from dictionary
            ursi_dx = get_dx(ursi, dx_dict)
            try:
                    for csv_file in os.listdir(ursi_dir):
                            if csv_file.endswith('.csv') and (condition in
                                                              csv_file):
                                # be verbose
                                print(''.join(['Processing ', csv_file, " (",
                                      ursi, " : ", ursi_dx, ")"]))
                                if csv_file.endswith('_long.csv'):
                                    # add long file data to long file list
                                    sample_row_long.append([get_features(
                                                            os.path.join(
                                                            ursi_dir,
                                                            csv_file)),[
                                                            ursi_dx]])
                                else:
                                    # add short file data to short file list
                                    sample_row_short.append([get_features(
                                                             os.path.join(
                                                             ursi_dir,
                                                             csv_file)),[
                                                             ursi_dx]])
            except FileNotFoundError:
                # tell if something is missing
                print ("no such directory: " + ursi_dir)
    # return both lists
    return sample_row_short, sample_row_long

def create_samples(config_file):
    """
    Function to create samples for a training set based on trial condition.

    Parameters
    ----------
    config_file : string
        openSMILE config_file filename

    Returns
    -------
    condition + feature_data.csv : file
        *.csv file containing feature data
    """
    # initialize dictionaries for short and long samples
    sample_short = {}
    sample_long = {}
    # set conditions
    conditions = ['_vocal_w_', '_vocal_no_', '_button_w_', '_button_no_']
    for condition in conditions:
        # initialize lists within dictionaries
        sample_short[condition] = []
        sample_long[condition] = []
    # set absolute path of top directory
    topdir = ('/Volumes/data/Research/CDB/SM_Sound_Analysis/all_audio_files/'
              'NEW/')
    for dirs in os.listdir(topdir):
        # do not include hidden files or directories
        # only take URSI directories
        if dirs[0] != '.' and (len(dirs) == 9 and dirs.startswith('M004')):
            for condition in conditions:
                # get the data from the openSMILE output *.csv files
                short_row, long_row = create_sample_row(dirs, condition,
                                                            config_file)
                try:
                    # add the data to the lists in the dictionaries
                    sample_short[condition].append(short_row)
                    sample_long[condition].append(long_row)
                except (KeyError):
                    # tell if something is missing
                    print (dirs + ' ' + condition)
    # set absolute path of output directory
    out_top_dir = '/Volumes/data/Research/CDB/SM_Sound_Analysis/openSMILE/'
    # set path for subdirectory for config_file
    csv_path = os.path.join(out_top_dir,config_file)
    for condition in conditions:
        # set filename for short files
        fs_csv = os.path.join(csv_path,(condition + 'short_feature_data.csv'))
        # set filename for long files
        fl_csv = os.path.join(csv_path,(condition + 'long_feature_data.csv'))
        # if output subdirectory does not exist, create it
        if not os.path.exists(csv_path):
            os.makedirs(csv_path)
        # save short formatted data file
        with open(fs_csv, 'w') as features_short_csv:
            feature_writer = csv.writer(features_short_csv)
            for item in sample_short[condition]:
                feature_writer.writerow(item)
        # save long formatted data file
        with open(fl_csv, 'w') as features_long_csv:
            feature_writer_long = csv.writer(features_long_csv)
            for item in sample_long[condition]:
                feature_writer_long.writerow(item)

def main():
        '''
        Get config_file from user.

        Iterate through openSMILE output *.csv files.

        Output reformatted *.csv files.
        '''
        # get config_file from user
        config_file = input("config file: ")
        # strip .conf extension if necessary
        if(config_file.endswith('.conf')):
                config_file = config_file.strip('.conf')
        # process and reformat the *.csv files
        create_samples(config_file)

# ============================================================================
if __name__ == '__main__':
        main()
