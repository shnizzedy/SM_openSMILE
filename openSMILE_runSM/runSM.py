#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""
Batch process SM dataset with user-entered openSMILE configuration file.

Authors:
    – Jon Clucas, 2016 (jon.clucas@childmind.org)
    - Arno Klein, 2015 - 2016

© 2016, Child Mind Institute, Apache v2.0 License

This script uses functions from mhealthx
( http://sage-bionetworks.github.io/mhealthx/ ).

Authors:
    - Arno Klein, 2015  (arno@sagebase.org)  http://binarybottle.com

Copyright 2015,  Sage Bionetworks (http://sagebase.org), Apache v2.0 License
"""
# extract and mhealthx.utilities are from mhealthx
# ( http://sage-bionetworks.github.io/mhealthx/ ).
# os is Python's operating system library.
# pandas is Python data analysis library.
import mhealthx.mhealthx.extract as ex, os

"""
Run from openSMILE home directory.
This script gets a configuration filename from the user, then
iteratively applies that configuration to
all wav files in "./all_audio_files/*".
"""
def runSM():
    """
    Function to run the same openSMILE configuration file on a batch of
    waveform files.

    Waveforms are expected to be under openSMILE home directory in
    all_audio_files/[URSI]/recorded_audio_files .

    Parameters
    ----------
    None.

    Returns
    -------
    feature_row : pandas Series
         row combining the original row with a row of openSMILE feature values

    feature_table : string
             output table file (full path)
    """
    # get config filename from user.
    config_file = raw_input('config file filename: ')
    while not os.path.exists(''.join(['config/',config_file])):
                config_file = raw_input('config file filename: ')
    # get subdirectories of "./all_audio_files/*".
    for root, dirs, files in os.walk('all_audio_files'):
        # get each participant.
        for participant in dirs:
            # declare row to pass to
            # ex.run_openSMILE(audio_file, command, flag1, flags, flagn,
            #           args, closing, row, table_stem, save_rows)
            row = None
            for proot, pdirs, pfiles in os.walk(os.path.join(root,
                                                participant)):
                # get each audio file
                for wav in pfiles:
                    # include only files with waveform extension
                    if wav.endswith('.wav'):
                        # check if all_audio_files/[URSI]/[config] exists for
                        # participant; if not, create that folder.
                        participant_home_dir = os.path.dirname(os.path.dirname(
                                               os.path.abspath(os.path.join(
                                               proot,wav))))
                        out_dir = os.path.join(participant_home_dir,
                                  'openSMILE_outputs', config_file.strip(
                                  '.conf'))
                        if not os.path.exists(out_dir):
                            os.makedirs(out_dir, 0755)
                        # run openSMILE and send results to
                        # all_audio_files/[URSI]/[config]
                        try:
                            # tell which file is being processed
                            print(wav)
                            # process the file
                            try:
                                row, table_path = ex.run_openSMILE(
                                     os.path.abspath(os.path.join(proot, wav)),
                                     ''.join(['/home/jclucas/opensmile-2.3.0/',
                                     'inst/bin/SMILExtract']), '-I', '-C',
                                     '-O', ''.join(['config/',config_file]),
                                     '', row, out_dir, True)
                            # if necessary, specify csvoutput
                            except cComRodentException:
                                row, table_path = ex.run_openSMILE(
                                     os.path.abspath(os.path.join(proot, wav)),
                                     ''.join(['/home/jclucas/opensmile-2.3.0/',
                                     'inst/bin/SMILExtract']), '-I', '-C',
                                     '-csvoutput', ''.join(['config/',
                                      config_file]), '', row, out_dir, True)
                        # keep going if openSMILE throws any other error
                        except:
                            pass
    return row, table_path

# ============================================================================
if __name__ == '__main__':
    runSM()
