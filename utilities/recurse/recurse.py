#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
recurse.py

Script to recursively collect files.

Author:
        – Jon Clucas, 2017 (jon.clucas@childmind.org)

© 2017, Child Mind Institute, Apache v2.0 License

@author: jon.clucas
"""

import argparse, os

def recurse(top_dir):
    """
    Function to recursively collect the absolute paths of all files in
    `top_dir`.

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
    
def filter_list(file_list, requirement):
    """
    Function to select files from `file_list` based on requirement.

    Parameters
    ----------
    file_list : list
        a list of absolute filepaths
    
    requirement : string
        requirement to filter `file_list` by

    Returns
    -------
    result : list
        either a list of all files to act upon or an empty list
    """
    for file in file_list:
        if not eval(''.join(["'", file, "'", requirement])):
            file_list.remove(file)
    return file_list
    
def filter_recurse(top_dir, requirement):
    """
    Function to recursively collect the absolute paths of select files in
    `top_dir` based on requirement.

    Parameters
    ----------
    top_dir : string
        absolute path of top directory for files we want to read from
        
    requirement : string
        requirement to filter `file_list` by

    Returns
    -------
    result : list
        either a list of all files to act upon or an empty list
    """
    file_list = []
    print(''.join(["Getting files from `", top_dir, "`"]))
    # get files
    for root, dirs, files in os.walk(top_dir):
        for file in files:
            if eval(''.join(["'", file, "'", requirement])):
                filepath = os.path.join(root, file)
                print(''.join(["  ", filepath])) 
                file_list.append(filepath)
        for dir in dirs:
            file_list.extend(recurse(dir))
    return file_list

def main():
    # script can be run from the command line to see results
    parser = argparse.ArgumentParser(description='get directory')
    parser.add_argument('in_dir', type=str)
    parser.add_argument('--req', type=str)
    arg = parser.parse_args()
    if arg.req:
        filter_recurse(arg.in_dir, arg.req)
    else:
        recurse(arg.in_dir)

# ============================================================================
if __name__ == '__main__':
    main()