#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
"""
import os, subprocess

def google_speech(in_file):
    url = ("https://www.google.com/speech-api/v2/recognize?output=json&"
           "lang=en-US&&pfilter=2&key=AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw")
    out_base = os.path.basename(in_file.strip('.flac').strip('.FLAC'))
    out_file = os.path.join(os.path.dirname(in_file), ''.join([out_base,
               '_(Google).json']))
    out_i = 0
    while os.path.exists(out_file):
        out_file = os.path.join(os.path.dirname(in_file), ''.join([out_base,
                   '_', str(out_i), '_(Google).json']))
        out_i = out_i + 1
    if not os.path.exists(os.path.dirname(out_file)):
        os.makedirs(out_file)
    command_string = ''.join(["curl -X POST --data-binary @", in_file,
                     " --user-agent 'Mozilla/5.0' --header 'Content-Type:"
                     " audio/x-flac; rate=44100;' '", url, "' -o ", out_file])
    print(command_string)
    subprocess.call(command_string, shell=True)
    """
    f = open(out_file, 'w')
    print(request.data.decode("utf-8", 'ignore'))
    f.write(request.data.decode("utf-8", 'ignore'))
    """

def main():
    google_speech("/Users/jon.clucas/Documents/recorder_test/"
                  "12_seconds.flac")

# ============================================================================
if __name__ == '__main__':
    main()
