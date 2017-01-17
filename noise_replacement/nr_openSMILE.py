#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""
nr_openSMILE.py

Run selected openSMILE scripts on files with noises replaced by various methods
(see `openSMILE_preprocessing/noise_replacement` for noise replacement
details).

Author:
    – Jon Clucas, 2016–2017 (jon.clucas@childmind.org)

© 2017, Child Mind Institute, Apache v2.0 License

This script uses functions from mhealthx
( http://sage-bionetworks.github.io/mhealthx/ ).

Authors:
    - Arno Klein, 2015–2017  (arno@sagebase.org)  http://binarybottle.com

Copyright 2015–2017,  Sage Bionetworks (http://sagebase.org) & Child Mind
Institute, Apache v2.0 License

"""

from ...openSMILE_runSM import mhealthx.mhealthx.extract as ex
from ... import iterate_ursis as iu
import os


# change this variable to your openSMILE installation location
openSMILE = '/home/jclucas/opensmile-2.3.0/inst/bin/SMILExtract'

def run_openSMILE(config_file, sound_file):
    """
    Function to run the openSMILE with a specified config_file on a specified
    sound file and save the results.

    Parameters
    ----------
    config_file : string
        the basename of the openSMILE config file that lives in `config`

    sound_file : string
        the absolute path to the soundfile

    Returns
    -------
    None.

    Outputs
    -------
    *soundfile*.csv : comma separated value file
        openSMILE output in arff–csv format with the original filename with the
        extension replaced, and in a subdirectory with a name matching the
        original location within an `openSMILE_output` directory at the
        relative level of original location
    """
    sub_dir = os.path.split(os.path.dirname(sound_file))
    basename = ''.join([os.path.basename(sound_file).strip('.wav').strip(
               '.WAV'), '.csv'])
    out_path = os.path.join(sub_dir[0], 'openSMILE_output', sub_dir[1])
    if not os.path.exists(out_path):
        os.makedirs(out_path, 0755)
    row = None
    r_oS_args = sound_file, openSMILE, '-I', '-C', '-O', ''.join(['config/',
                config_file]), '', row, out_dir, True
    print(' '.join(r_oS_args))
    # process the file
    try:
        row, table_path = ex.run_openSMILE(r_oS_args)
    # if necessary, specify csvoutput
    except cComponentException:
        row, table_path = ex.run_openSMILE(sound_file, openSMILE, '-I', '-C',
                          '-csvoutput', ''.join(['config/', config_file]), '',
                          row, out_dir, True)

def main():
    # replace `top_dir`'s value with your top-level directory
    top_dir = '/home/jclucas/opensmile-2.3.0/test/noise_replacement_efficacy'
    # replace `sub_dirs` with your conditions
    sub_dirs = ['ambient_clip', 'clone_fill', 'no_beeps', 'sample_silenced',
                'timeshifted']
    # replace `configs` with your openSMILE config files
    configs = ['emobase.conf', 'ComParE_2016.conf']
    # initialize file_list
    file_list = []
    # get files
    for sub_dir in sub_dirs:
        file_list.extend(iu.i_ursi(top_dir, sub_dir))
    for sound_file in file_list:
        for config in configs:
            run_openSMILE(config, sound_file)

# ============================================================================
if __name__ == '__main__':
    main()