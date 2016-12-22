#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_sample.py

Script to find a 2.5 second clip of ambient noise and silence that clip.

*in progress*

Author:
        – Jon Clucas, 2016 (jon.clucas@childmind.org)

© 2016, Child Mind Institute, Apache v2.0 License
Created on Wed Dec 21 16:34:37 2016

@author: jon.clucas
"""
# workaround for local installation : adjust these paths to local installation
#     directories
import sys
sys.path.append("/Volumes/Jon.Clucas/openSMILE/SM_openSMILE")
sys.path.append("/Library/Frameworks/Python.framework/Versions/2.7/lib/"
                "python2.7/site-packages")

import iterate_ursis as iu, noise_replacement as nr, os, pydub, random

def create_sample(in_file):
    """
    Function to iterate through [top_directory]/URSI/[subdirectory]/files
    structure and perform a function on each file.

    Parameters
    ----------
    in_file : string
        absolute path of file

    Returns
    -------
    None

    TODO: break this function apart
    """
    # get file
    print (''.join(["Getting ", in_file]))
    out_file = os.path.join(os.path.dirname(os.path.dirname(in_file)),
                 "sample_silenced", os.path.basename(in_file))
    out_clone = os.path.join(os.path.dirname(os.path.dirname(in_file)),
                 "clone_fill", os.path.basename(in_file))
    # if output directory does not exist, create
    if not os.path.exists(os.path.dirname(out_file)):
        print (''.join(["Making directory: ", os.path.dirname(out_file)]))
        os.makedirs (os.path.dirname(out_file))
    if not os.path.exists(os.path.dirname(out_clone)):
        print (''.join(["Making directory: ", os.path.dirname(out_clone)]))
        os.makedirs (os.path.dirname(out_clone))
    # get ambient clips
    options = nr.get_ambient_clips(in_file)
    # how many?
    print(''.join([str(len(options)), " ambient clips"]))
    remaining_options = []
    for pair in options:
        if ((pair[1] - pair[0]) > 110250):
            remaining_options.append(pair)
    num_options = len(remaining_options)
    print(''.join([str(num_options), " ≥ 2.5 seconds"]))
    if num_options == 0:
        remaining_options = options
        num_options = len(remaining_options)
    chosen_one = remaining_options[random.randrange(0, num_options)]
    print(''.join(['chosen clip : ', str(chosen_one[0]), ":",
          str(chosen_one[1])]))
    original = pydub.AudioSegment.from_wav(in_file)
    clone = nr.grow_mask(original.get_sample_slice(chosen_one[0],
            chosen_one[1]), len(original))
    sample_clip = original.get_sample_slice(0, chosen_one[0])
    sample_clip.append(pydub.AudioSegment.silent(duration=(chosen_one[1] -
                       chosen_one[0])))
    sample_clip.append(original.get_sample_slice(chosen_one[1], None))
    print(''.join(["Exporting ", os.path.basename(os.path.dirname(out_file)),
          "/", os.path.basename(out_file)]))
    sample_clip.export(out_file, format="wav")
    clone_clip = nr.replace_silence(sample_clip, clone, 44.1)
    clone_clip.export(out_clone, format="wav")

def main():
    t_dir = "/Volumes/data/Research/CDB/openSMILE/audio_files"
    starting_files = iu.i_ursi(t_dir, "no_beeps")
    for file in starting_files:
        create_sample(file)

# ============================================================================
if __name__ == '__main__':
    main()