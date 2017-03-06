#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
openSMILE_csv.py

Script to format openSMILE *.csv
output combined with Dx data into a new
[participant × file × feature × Dx]
*.csv file.

Authors:
	– Jon Clucas, 2016-2017 (jon.clucas@childmind.org)
	
© 2016-2017, Child Mind Institute, Apache v2.0 License
"""

import csv, os

def create_sample_row(ursi, replacement, condition, config):
    """
    Function to create a row for a training set.

    Parameters
    ----------
    ursi : string
        a participant's URSI

    Returns
    -------
    sample_row : list
        an n_files × 1 list of n_features × 2 lists of [features],[diagnosis]
    """
    sample_row = []
    topdir = os.path.abspath('../adults_replaced')
    ursi_dir = os.path.join(topdir, ursi, 'openSMILE_outputs', config,
               replacement)
    ursi_dx = get_dx(ursi)
    try:
        for csv_file in os.listdir(ursi_dir):
            if csv_file.endswith('.csv') and (condition in csv_file):
                sample_row.append([get_features(os.path.join(ursi_dir,
                                  csv_file), config), [ursi_dx]])
    except FileNotFoundError:
        print ("no such directory: " + ursi_dir)
    return sample_row

def create_samples(config):
    """
    Function to create samples for a training set based on trial condition.

    Parameters
    ----------
    None

    Returns
    -------
    condition + feature_data.csv : file
        *.csv file containing feature data
    """
    sample = {}
    replacements = ['original', 'adults', 'adults_removed',
                    'adults_replaced_clone', 'adults_replaced_pink',
                    'adults_timeshifted']
    conditions = ['_vocal_w_', '_vocal_no_', '_button_w_', '_button_no_']
    for replacement in replacements:
        for condition in conditions:
            sample[(replacement, condition)] = []
    topdir = os.path.abspath('../adults_replaced')
    for dirs in os.listdir(topdir):
        # do not include hidden files or directories
        if dirs.startswith('M00'):
            for replacement in os.listdir(os.path.join(topdir, dirs,
                               'openSMILE_outputs', config)):
                if replacement != '.DS_Store':
                    for condition in conditions:
                        try:
                            sample[(replacement, condition)].append(
                                    create_sample_row(dirs, replacement, 
                                    condition, config))
                        except (KeyError):
                            print (dirs + condition + replacement)
    csv_path = os.path.join(topdir, 'summary', config)
    if not os.path.exists(csv_path):
        os.makedirs(csv_path)
    for replacement in replacements:
        for condition in conditions:
            if len(sample[(replacement, condition)]) > 0:
                f_csv = os.path.join(csv_path,''.join([replacement,
                        condition, 'feature_data.csv']))
                if not os.path.exists(csv_path):
                    os.makedirs(csv_path)
                with open(f_csv, 'w') as features_csv:
                    feature_writer = csv.writer(features_csv)
                    for item in sample[(replacement, condition)]:
                        feature_writer.writerow(item)

def get_features(csv_file, config):
    """
    Function to get features from openSMILE
    emobase configuration file csv outputs

    Parameters
    ----------
    csv_file : string
        filename of a *.csv emobase output file 
     
    config : string
        openSMILE config file basename

    Returns
    -------
    temp_list : list
        list of features from emobase output file
    """
    num_features = get_num_features(config)
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        temp_list = []
        for row in reader:
            temp_list.append(row)
        temp_list = ''.join(temp_list[num_features + 2][1]).split(',')
        for item in temp_list:
            try:
                item = float(item)
            except (TypeError, ValueError):
                pass
    return temp_list

def get_dx(ursi, dx_dictionary=None):
    """
    Function to get a participant's diagnosis
    from a dictionary of diagnoses.

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
    Function to create a diagnosis dictionary
    from a csv file containing diagnoses.
  
    Parameters
    ----------
    None

    Returns
    -------
    dx_dictionary : dictionary
        a dictionary of {['URSI']:['Dx?']} pairs
    """
    dx_dictionary = {}
    with open('dx/SM_DX_summary_status_dx.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            dx_dictionary[row['URSI']] = row['Dx?']
        return dx_dictionary

def get_num_features(config):
    """
    Function to get the number of features in an openSMILE config
    output CSV.
    
    Parameters
    ----------
    config : string
        basename of the openSMILE config file
    """
    if config in features:
        return features[config]
    else:
        feature_path = os.path.abspath(os.path.join(config, ''.join([config,
                       '_features.csv'])))
        print(feature_path)
        if os.path.exists(feature_path):
            features[config] = len(open(feature_path).readlines())
            return features[config]
        else:
            return 0

def main():
    global features
    features = {}
    os.chdir("/Users/jon.clucas/SM_openSMILE/openSMILE_preprocessing/"
             "noise_replacement/replacement_test_outputs/configs")
    configs = ['emobase', 'ComParE_2016']
    for config in configs:
        create_samples(config)
    
    
# ============================================================================
if __name__ == '__main__':
	main()
