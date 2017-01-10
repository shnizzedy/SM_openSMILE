#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Batch process recorder tests with user-entered openSMILE configuration file.

Author:
	– Jon Clucas, 2017 (jon.clucas@childmind.org)
	
© 2017, Child Mind Institute, Apache v2.0 License
"""

import os, subprocess

def recurse(top_dir):
    """
    Function to recursively collect the absolute paths of all files in
    `top_dir`.
    https://github.com/shnizzedy/recurse
    
    Parameters
    ----------
    top_dir : string
        absolute path of top directory for files we want to read from
    Returns
    -------
    result : list
        either a list of all files to act upon or an empty list
    """
    # initialize result
    file_list = []
    print(''.join(["Getting files from `", top_dir, "`"]))
    # get files
    for root, dirs, files in os.walk(top_dir):
        for file in files:
            filepath = os.path.join(root, file)
            print(''.join(["  ", filepath])) 
            file_list.append(filepath)
        for dir in dirs:
            file_list.extend(recurse(dir))
    return file_list

def main():
    top_dir = "/home/jclucas/opensmile-2.3.0/test/recorder_test"
    configs = ["emobase.conf", "ComParE_2016.conf"]
    file_list = recurse(top_dir)
    for file in file_list:
        if (os.path.basename(file).endswith(".wav") or 
            os.path.basename(file).endswith(".WAV")):
            for config in configs:
                outpath = os.path.join(os.path.dirname(file),
                          config.strip(".conf"), ''.join([os.path.basename(
                          file).strip('.wav').strip('.WAV'), ".csv'"]))
                if not os.path.exists(outpath):
                    os.makedirs(outpath)
                command = ''.join(["./SMILExtract -C 'config/", config,
                          "' -I '", file, "' -O '", outpath])
                print(command)
                subprocess.call(command, shell = True)
        
    
# ============================================================================
if __name__ == '__main__':
	main()
