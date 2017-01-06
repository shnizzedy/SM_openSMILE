#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
convert_dir_to_wav.py
Script to quickly convert all mp3 and mxf files in a directory to
waveform files.
Author:
        – Jon Clucas, 2017 (jon.clucas@childmind.org)
© 2017, Child Mind Institute, Apache v2.0 License

@author: jon.clucas
"""
import argparse, mp3_to_wav as mp3, mxf_to_wav as mxf, os


def main():
    # script can be run from the command line
    parser = argparse.ArgumentParser(description='get directory')
    parser.add_argument('in_dir', metavar='in_dir', type=str)
    arg = parser.parse_args()
    for root, dirs, files in os.walk(arg.in_dir):
        for file in files:
            if file.casefold().endswith(".mp3".casefold()):
                mp3.mp3_to_wav(os.path.join(root, file))
            elif file.casefold().endswith(".mxf".casefold()):
                mxf.mxf_to_wav(os.path.join(root, file))
            else:
                pass

# ============================================================================
if __name__ == '__main__':
    main()
