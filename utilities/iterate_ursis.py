#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
iterate_ursis.py

Script to iterate through [top_directory]/URSI/[subdirectory]/files structure
and perform a function on each file.

Author:
        – Jon Clucas, 2016 (jon.clucas@childmind.org)

© 2016, Child Mind Institute, Apache v2.0 License
Created on Wed Dec 21 16:34:37 2016

@author: jon.clucas
"""
import os

def i_ursi(top_in, sub_in):
    """
    Function to iterate through [top_directory]/URSI/[subdirectory]/files
    structure and perform a function on each file.

    Parameters
    ----------
    top_in : string
        absolute path of top directory for files we want to read from

    sub_in : string
        the name of the subdirectory we want to read from

    Returns
    -------
    result : list or None
        returns either a list of all files to act upon.
    """
    # initialize result
    result = []
    print("Getting files.")
    # get participant directories
    for root, dirs, files in os.walk(top_in):
        # get each participant
        for participant in dirs:
            if (os.path.basename(participant).startswith("M") or
                os.path.basename(participant).startswith("m")):
                print(''.join(["From ", os.path.basename(participant)]))
                # get participant subdirectories
                for proot, pdirs, pfiles in os.walk(os.path.join(root,
                                                    participant)):
                    for pdir in pdirs:
                        # get desired subdirectory
                        if os.path.basename(pdir) == sub_in:
                            # get files
                            for qroot, qdirs, qfiles in os.walk(os.path.join(
                                                                proot, pdir)):
                                for qfile in qfiles:
                                    if not os.path.basename(qfile).startswith(
                                                            '.'):
                                        rfile = os.path.join(qroot, qfile)
                                        print(''.join(["    adding ", rfile]))
                                        result.append(rfile)
    print(''.join(["Returning ", str(len(result)), " files"]))
    return result