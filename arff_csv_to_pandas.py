#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
arff_csv_to_pandas.py

Functions to import openSMILE outputs to Python pandas.

Authors:
    – Jon Clucas, 2016 (jon.clucas@childmind.org)
    – Arno Klein, 2016 (arno.klein@childmind.org)
    – Bonhwang Koo, 2016 (bonhwang.koo@childmind.org)
	
© 2016, Child Mind Institute, Apache v2.0 License

Created on Thu Dec  8 10:43:37 2016

@author: jon.clucas
"""
import arff, os, pandas as pd

def main():
    pass

def build_dataframe(wd,config_file,condition,methods):
    """
    Function to pull openSMILE output csv into a pandas series
    
    Parameters
    ----------
    wd : string
        working directory
                                
    config_file : string
        openSMILE configuration file filename
        
    condition : string
        ["ambient", "noise"]
        
    methods : list
        ["clone_all","replaced_clone","replaced_brownian","replaced_pink",
             "replaced_stretch", "replaced_white", "silenced"]
        
    Returns
    -------
    d : pandas dataframe
        a dataframe for the relevant set of files and features
    """
    s = get_oS_data(os.path.join(wd,config_file,"full_original.csv"),"original",
                    config_file,"original")
    d = s.to_frame()
    for method in methods:
        try:
            s = get_oS_data(os.path.join(
                            wd,config_file,
                            condition,"".join(["full_",condition,
                            "_",method,".csv"])),method,config_file,
                            condition)
            d = d.join(s.to_frame())
        except FileNotFoundError as e404:
            pass
    return(d)
                                    
def get_oS_data(csvpath,method,config_file,condition):
    """
    Function to pull openSMILE output csv into a pandas series
    
    Parameters
    ----------
    csvpath : string
        absolute path to csv file
        
    method : string
        ["clone_all","replaced_clone","replaced_brownian","replaced_pink",
             "replaced_stretch", "replaced_white", "silenced", "original"]
                                
    config_file : string
        openSMILE configuration file filename
        
    condition : string
        ["ambient", "noise"]
        
    Returns
    -------
    oS_series : pandas series
    """
    try:
        oS_data = arff.load(open(csvpath))
        return arff_to_pandas(oS_data,method,config_file,condition)
    # replace "unknown" attribute type with "string" attribute type
    except arff.BadAttributeType:
        temp_oS = open(csvpath, 'r')
        temp_oS_lines = temp_oS.readlines()
        temp_oS_string = ""
        for temp_oS_line in temp_oS_lines:
            words = temp_oS_line.split()
            if(len(words) == 3):
                if ((words[0] == "@attribute") and (words[2] == "unknown")):
                    temp_oS_string = "".join([temp_oS_string,
                                             " ".join([words[0],words[1],
                                             "string\n"])])
                else:
                    temp_oS_string = "".join([temp_oS_string,temp_oS_line])
            else:
                temp_oS_string = "".join([temp_oS_string,temp_oS_line])
        tof = open("/Volumes/data/Research/CDB/openSMILE/Audacity/test/temp.csv","w")
        tof.write(temp_oS_string)
        tof.close()
        oS_data = arff.loads(open("/Volumes/data/Research/CDB/openSMILE/Audacity/test/temp.csv"))
        return arff_to_pandas(oS_data,method,config_file,condition)
        
def arff_to_pandas(arff_data,method,config_file,condition):
    """
    Function to convert python arff data into a pandas series
    
    Parameters
    ----------
    arff_data : string
        arff formatted data string
        
    method : string
        ["clone_all","replaced_clone","replaced_brownian","replaced_pink",
             "replaced_stretch", "replaced_white", "silenced", "original"]
             
    config_file : string
        openSMILE configuration file filename
        
    condition : string
        ["ambient", "noise"]
        
    Returns
    -------
    oS_series : pandas series
        pandas series 
    """
    indicies = []
    for attribute in arff_data["attributes"]:
        indicies.append(attribute[0])
    return(pd.Series(arff_data["data"][0],indicies,name="_".join([config_file,condition,method])))

# ============================================================================
if __name__ == '__main__':
    main()