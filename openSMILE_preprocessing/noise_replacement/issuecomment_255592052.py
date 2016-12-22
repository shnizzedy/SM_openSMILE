#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scipy.io.wavfile.read troubleshooting
https://github.com/scipy/scipy/issues/6700#issuecomment-255592052
"""

from scipy.io.wavfile import _read_riff_chunk
from os.path import getsize

def small_program(filename):
    with open(filename, 'rb') as f:
        riff_size, _ = _read_riff_chunk(f)

    print('RIFF size: {}'.format(riff_size))
    print('os size:   {}'.format(getsize(filename)))