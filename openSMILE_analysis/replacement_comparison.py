#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
replacement_comparison.py

Functions to compare openSMILE outputs for various noise replacement methods
for each waveform in the sample.

Authors:
    – Jon Clucas, 2017 (jon.clucas@childmind.org)

© 2017, Child Mind Institute, Apache v2.0 License

@author: jon.clucas
"""

import os, sys
if os.path.abspath('../../') not in sys.path:
    if os.path.isdir(os.path.join(os.path.abspath('../..'), 'SM_openSMILE')):
        sys.path.append(os.path.abspath('../..'))
    elif os.path.isdir(os.path.join(os.path.abspath('..'), 'SM_openSMILE')):
        sys.path.append(os.path.abspath('..'))
    elif os.path.isdir('SM_openSMILE'):
        sys.path.append(os.path.abspath('.'))
from SM_openSMILE.openSMILE_preprocessing.noise_replacement import \
     condition_comparison_nr_all as cc
from SM_openSMILE.cfg import conditions, oSdir
adults_replaced = os.path.dirname(oSdir)

def main():
    configs = ['emobase', 'ComParE_2016']
    replacements = ['removed', 'replaced_clone', 'replaced_pink', 'timeshifted'
                    ]
    for i, replacement in enumerate(replacements):
        replacements[i] = '_'.join(['adults', replacement])
    replacements = [*replacements, 'adults']
    list_of_dataframes = []
    for URSI in os.listdir(adults_replaced):
        if URSI not in ['.DS_Store', 'summary']:
            for condition in conditions:
                for config_file in configs:
                    URSI_files = []
                    for method in replacements:
                        method_dir = os.path.join(adults_replaced, URSI,
                                     'openSMILE_outputs', config_file,
                                     method)
                        if os.path.isdir(method_dir):
                            if len(URSI_files) == 0:
                                or_dir = os.path.join(adults_replaced, URSI,
                                         'openSMILE_outputs', config_file,
                                         'original')
                                if os.path.isdir(or_dir):
                                    for or_file in os.listdir(or_dir):
                                        if condition in or_file:
                                            URSI_files.append(os.path.join(
                                                              or_dir, or_file))
                            for csv_file in os.listdir(method_dir):
                                csv_path = os.path.join(method_dir, csv_file)
                                if condition in csv_file and csv_path not in \
                                   URSI_files: 
                                    URSI_files.append(csv_path)
                    if len(URSI_files) == 6:
                        print(''.join(["Processing ", URSI, ", ", condition,
                              " : ", config_file]))
                        list_of_dataframes.append(["_".join([URSI, config_file]
                                                  ), cc.build_dataframe(URSI,
                                                  ['original', *replacements],
                                                  config_file, URSI_files)])
    cc.mad_rank_analyses([list_of_dataframes], adults_replaced)

# ============================================================================
if __name__ == '__main__':
    main()