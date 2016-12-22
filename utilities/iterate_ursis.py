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

def i_ursi(top_in, sub_in, function, parameters = None, conditions = None):
    """
    Function to iterate through [top_directory]/URSI/[subdirectory]/files
    structure and perform a function on each file.

    Parameters
    ----------
    top_in : string
        absolute path of top directory for files we want to read from

    sub_in : string
        the name of the subdirectory we want to read from

    function : function
        the function to perform on each file

    parameters : list or None (optional)
        list of parameters to pass the function. The string "ursi_i", if
        included will be replaced with the ursi. The absolute path of the file
        to be operated on will be inserted in the front of this list.

    conditions : list or None (optional)
        conditions to check before performing function.

    Returns
    -------
    result : list or None
        returns either a list of all returns of the called function or None if
        the function has no return.
    """
    # initialize result
    result = []
    # get participant directories
    for root, dirs, files in os.walk(top_in):
        # get each participant
        for participant in dirs:
            print(os.path.basename(participant))
            # get participant subdirectories
            for proot, pdirs, pfiles in os.walk(os.path.join(root,
                                                participant)):
                # get desired subdirectory
                if pdirs == sub_in:
                    # get files
                    for pfile in pfiles:
                        # if applicable, check for conditions
                        try:
                            for condition in conditions:
                                condition = ''.join(pfile, condition)
                                print(condition)
                                if eval(condition):
                                    # add filepath to parameters
                                    try:
                                        parameters = [pfile, *parameters]
                                    except NameError:
                                        parameters = [pfile]
                                    # run the function
                                    print(str(function(*parameters)))
                                    result.append(function(*parameters))
                        # otherwise, just run the function
                        except NameError:
                            # add filepath to parameters
                            try:
                                parameters = [pfile, *parameters]
                            except NameError:
                                parameters = [pfile]
                            # run the function
                            print(str(function(*parameters)))
                            result.append(function(*parameters))
    return result