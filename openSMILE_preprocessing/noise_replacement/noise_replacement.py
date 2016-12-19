#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
noise_replacement.py

* in progress *

Script to replace silenced noises in data sound files.

Author:
        – Jon Clucas, 2016 (jon.clucas@childmind.org)

© 2016, Child Mind Institute, Apache v2.0 License

Created on Mon Dec 19 17:00:00 2016
"""
import numpy as np
from scipy import signal
from scipy.io import wavfile

def get_ambient_clips(path):
    """
    Find sections of ambient noise at least 2 seconds long.

    Parameters
    ----------
    path : string
        absolute path to waveform file to process

    Returns
    -------
    ambience : list of tuples
        a list of (start-time, stop-time) tuples of ambient segments
    """
    # read waveform file
    input_data = wavfile.read(path)
    # get numpy array of amplitude values
    audio = input_data[1][:, 0]
    # get rate
    # rate = input_data[0]
    # t = np.arange(len(audio)) / rate
    # calculate envelope
    envelope = np.abs(signal.hilbert(audio))

    # initialize start, stop, and ambiance lists
    starts, stops, ambience = ([] for i in range(3))
    # initialize start flag
    start_flag = True
    # set threshold
    threshold = 1036
    for index, point in enumerate(envelope):
        # get beginnings of ambient segments
        if (start_flag and point < threshold and point != 0):
            start_flag = False
            starts.append(index)
        # get ends of ambient segments
        elif (point > threshold and (not start_flag)):
            if(index >= starts[-1] + 88200):
                start_flag = True
                stops.append(index)
    # make tuple list
    for i, v in enumerate(stops):
        ambience.append((starts[i], v))
    # return tuple list
    return(ambience)

def main():
    path = "/Volumes/data/Research/CDB/openSMILE/Audacity/test/original.wav"
    get_ambient_clips(path)

# ============================================================================
if __name__ == '__main__':
        main()