#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
"""
import json, os, subprocess

def google_speech(in_file):
    with open("/Users/jon.clucas/Documents/recorder_test/"
              "Speech API test-16e0802b3564.json") as google_credentials:
        cred = json.load(google_credentials)
    url = (''.join(["https://www.google.com/speech-api/v2/recognize?output="
            "json&lang=en-US&&pfilter=2&key=", cred["api_key"]]))
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
                     " audio/x-flac; rate=44100;' '", url, "' -o '", out_file,
                     "'"])
    print(command_string)
    subprocess.call(command_string, shell = True)

def watson_speech(in_file):
    with open("/Users/jon.clucas/Documents/recorder_test/watson-cred.json"
              ) as watson_credentials:
        cred = json.load(watson_credentials)
    out_base = os.path.basename(in_file.strip('.flac').strip('.FLAC'))
    out_file = os.path.join(os.path.dirname(in_file), ''.join([out_base,
               '_(Watson).json']))
    out_i = 0
    while os.path.exists(out_file):
        out_file = os.path.join(os.path.dirname(in_file), ''.join([out_base,
                   '_', str(out_i), '_(Watson).json']))
        out_i = out_i + 1
    if not os.path.exists(os.path.dirname(out_file)):
        os.makedirs(out_file)
    command_string = (''.join(["curl -u '", cred["username"], "':'",
                      cred["password"], "' --header 'Content-Type: audio/"
                      "flac' --data-binary '@", in_file, "' 'https://stream.",
                      "watsonplatform.net/speech-to-text/api/v1/recognize?'",
                      "continuous=true > '", out_file, "'"]))
    print(command_string)
    subprocess.call(command_string, shell = True)
          
def main():
    google_speech("/Users/jon.clucas/Documents/recorder_test/"
                  "12_seconds.flac")

# ============================================================================
if __name__ == '__main__':
    main()
