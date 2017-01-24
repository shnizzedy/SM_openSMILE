#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mxf_to_wav.py

Script to quickly convert an mxf file to a waveform file.

Author:
        – Jon Clucas, 2016 (jon.clucas@childmind.org)

© 2016, Child Mind Institute, Apache v2.0 License

Created on Fri Dec 23 12:43:40 2016

@author: jon.clucas
"""
import argparse, subprocess
from os import path

def mxf_to_wav(in_file):
    # make an output filename
    out_base = path.basename(in_file).strip('.mxf').strip('.MXF')
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
    parser = argparse.ArgumentParser(description='get mxf')
    parser.add_argument('in_file', metavar='in_file', type=str)
    arg = parser.parse_args()
    mxf_to_wav(arg.in_file)

# ============================================================================
if __name__ == '__main__':
    main()
