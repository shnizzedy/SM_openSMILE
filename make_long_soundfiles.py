#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_long_soundfiles.py

Create mylist.txt and run ffmpeg -f concat for each (particpant + condition).

Authors:
    – Jon Clucas, 2016 (jon.clucas@childmind.org)
    – Bonhwang Koo, 2016 (bonhwang.koo@childmind.org)
	
© 2016, Child Mind Institute, Apache v2.0 License

Created on Tue Nov 29 15:52:30 2016

@author: jon.clucas
@author: bonhwang.koo
"""

import os, subprocess


def make_long_wav(ursi_dir, mylist_txt):
    """
    Function to run "ffmpeg -f concat" on mylist_txt.
    
    Parameters
    ----------
    ursi_dir : string
         absolute path to *.txt file's parent directory for participant waveforms
         
    mylist_txt : string
        file list textfile filename
        
    Returns
    -------
    None
    
    Output
    ------
    [ursi][conditon]long".wav : waveform
        concatenated waveform file
    """
    # create filename for output file
    ursi_condition_wav = "".join([mylist_txt.strip(".txt"),"long_no_beeps.wav"])
    # create shell command 
    shell_command = "".join(["cd /Applications && ./ffmpeg -y -f concat -i \"",
                            os.path.join(ursi_dir,mylist_txt), "\" -c copy \"",
                            os.path.join(ursi_dir,ursi_condition_wav),"\""])
    # run shell command
    subprocess.run(shell_command, shell=True)
    
def make_file_list(topdir, ursi, condition):
    """
    Function to make a *.txt file for each (ursi + condtion).
    
    Parameters
    ----------
    topdir : string
        absolute path for top-level directory containing participant directories
    
    ursi : string
        URSI, which is also the directory name in which our files are located
    
    condition : string
        experimental condition
        
    Returns
    -------
    ursi_dir : string
        absolute path to *.txt file's parent directory for participant waveforms
    
    mylist_txt : string
        file list textfile filename
        
    Output
    ------
    [ursi][condition].txt : text files
        a listing of 3" waveforms to be concatenated
    """
    # initialize empty list
    file_list = []
    ursi_dir = os.path.join(topdir,ursi,'no_beeps')
    # make the file list
    for wav_file in os.listdir(ursi_dir):
        if (condition in wav_file and wav_file.endswith('.wav') and not "long" in wav_file):
            file_list.append(wav_file)
    
    # write list to txt file, one item per line
    mylist_txt = "".join([ursi, condition, ".txt"])
    with open(os.path.join(ursi_dir,mylist_txt), 'w') as mylist:
        for waveform in file_list:
            mylist.write('file \'' + waveform + '\'\n')
    # return directory and filename as a tuple
    return (ursi_dir, mylist_txt)

def create_long_soundfiles():
    """
    Function to take 3" sound files and splice them back together.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    # initialize list of conditions
    conditions = ['_vocal_w_', '_vocal_no_', '_button_w_', '_button_no_']
    # set directory
    topdir = '/Volumes/data/Research/CDB/SM_Sound_Analysis/all_audio_files/NEW/'
    # iterate through participant directories
    for dirs in os.listdir(topdir):
        # do not include hidden files or directories
        if dirs[0] == 'M':
            for condition in conditions:
                try:
                    ursi_dir, mylist_txt = make_file_list(topdir, dirs, condition)
                    make_long_wav(ursi_dir, mylist_txt)
                except (KeyError):
                    print (dirs + ' ' + condition)

def main():
  create_long_soundfiles()

# ============================================================================
if __name__ == '__main__':
	main()
