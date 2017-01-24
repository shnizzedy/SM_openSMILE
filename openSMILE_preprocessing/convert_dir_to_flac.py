#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
convert_dir_to_flac.py
Script to quickly convert all mp3 and mxf files in a directory to
flac files.
Author:
        – Jon Clucas, 2016 (jon.clucas@childmind.org)
© 2016, Child Mind Institute, Apache v2.0 License

@author: jon.clucas
"""
import argparse, wav_to_flac as wtf, os


def main():
    # script can be run from the command line
    parser = argparse.ArgumentParser(description='get directory')
    parser.add_argument('in_dir', metavar='in_dir', type=str)
    arg = parser.parse_args()
    for root, dirs, files in os.walk(arg.in_dir):
        for file in files:
            if file.casefold().endswith(".wav".casefold()):
                wtf.wav_to_flac(os.path.join(root, file))
            else:
                pass

# ============================================================================
if __name__ == '__main__':
    main()
