#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
copy_nr_files.py

Script to copy noise-replaced files from original location to a different 
centralized location.

Author:
        – Jon Clucas, 2017 (jon.clucas@childmind.org)

© 2017, Child Mind Institute, Apache v2.0 License

Created on Wed Mar  1 12:25:41 2017

@author: jon.clucas
"""
import os, subprocess

def main():
    to_copy = ["adults", "adults_removed", "adults_replaced_clone",
               "adults_replaced_pink", "adults_timeshifted"]

    top_dir = input("Top directory (where files are already): ")
    out_dir = input("Top directory (where files are going): ")

    for URSI in os.listdir(top_dir):
            if URSI not in [".DS_Store", "nobeeps"]:
                for ar in to_copy:
                    ar_path = os.path.join(top_dir, URSI, ar)
                    if os.path.isdir(ar_path):
                        for wav_file in os.listdir(ar_path):
                            if wav_file.endswith('.wav'):
                                full_path = os.path.join(ar_path, wav_file)
                                out_path = os.path.join(out_dir, ar, wav_file)
                                if not os.path.exists(os.path.dirname(out_path)
                                       ):
                                    os.makedirs(os.path.dirname(out_path))
                                sp_command = ''.join(['cp -v ', full_path, " ",
                                             out_path])
                                print(sp_command)
                                subprocess.run(sp_command, shell=True)
                            
# ============================================================================
if __name__ == '__main__':
        main()                     