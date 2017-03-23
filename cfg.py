#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cfg.py

global variables

@author: jon.clucas
"""
import os

# top directory for random forest summary files
topdir = os.path.abspath(os.path.join(os.path.dirname(__file__),
         'openSMILE_analysis/random_forests/predict_SM/long_files/summary'))

# top directory for openSMILE output summary files
oSdir = os.path.abspath(os.path.join(os.path.dirname(__file__),
        'openSMILE_preprocessing/noise_replacement/replacement_test_outputs/'
        'adults_replaced/summary'))

# set conditions
conditions = ["_button_no_", "_button_w_", "_vocal_no_", "_vocal_w_"]