#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
wav32_to_wav16.py

Script to quickly convert a directory of 32 bit waveform files to 16 bit
waveform file.

Author:
        – Jon Clucas, 2016 (jon.clucas@childmind.org)

© 2016, Child Mind Institute, Apache v2.0 License

Created on Fri Dec 23 12:43:40 2016

@author: jon.clucas
"""
import argparse, subprocess
from os import path, walk

def wav32_to_wav16(in_file):
    # make an output filename
    out_base = path.basename(in_file).strip('.wav').strip('.WAV')
    out_i = 0
    out_file = path.join(path.dirname(in_file), ''.join([out_base, '.wav']))
    while path.exists(out_file):
        out_file = path.join(path.dirname(in_file), ''.join([out_base, '_',
                   str(out_i), '.wav']))
        out_i = out_i + 1
    # do the conversion verbosely
    to_convert = ''.join(["ffmpeg -i ", in_file, " -ac 2 -acodec pcm_s16le ",
                 out_file])
    print(''.join(["Converting ", in_file, " to ", out_file]))
    subprocess.call(to_convert, shell = True)

def main():
    # script can be run from the command line
    parser = argparse.ArgumentParser(description='get directory')
    parser.add_argument('in_dir', metavar='in_dir', type=str)
    arg = parser.parse_args()
    for root, dirs, files in walk(arg.in_dir):
        for file in files:
            if file.casefold().endswith(".wav".casefold()):
                wav32_to_wav16(path.join(root, file))
            elif file.casefold().endswith(".mxf".casefold()):
                mxf.mxf_to_wav(path.join(root, file))
            else:
                pass

# ============================================================================
if __name__ == '__main__':
    main()
    
