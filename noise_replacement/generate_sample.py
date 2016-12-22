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

def check_clip_len(options, duration):
    """
    TODO: document
    """
    remaining_options = []
    for pair in options:
        if ((pair[1] - pair[0]) > duration):
            remaining_options.append(pair)
            print(''.join(["Here's an option: ", str(pair[0]), ":", str(pair[
                  1])]))
    return remaining_options

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
    """
    # get file
    print (''.join(["Getting ", in_file]))
    # get ambient clips
    options = nr.get_ambient_clips(in_file)
    # how many?
    print(''.join([str(len(options)), " ambient clips"]))
    remaining_options = []
    # start by looking for clips 2.5 seconds or longer
    desired_duration = 110250
    while len(remaining_options) == 0:
        remaining_options = check_clip_len(options, desired_duration)
        # reduce desired duration by .25 seconds
        desired_duration = desired_duration - 11025
    num_options = len(remaining_options)
    print(''.join([str(num_options), " ≥ ", str(round(desired_duration /
          44100, 2)), " seconds"]))
    chosen_one = remaining_options[random.randrange(0, num_options)]
    print(''.join(['chosen clip : ', str(chosen_one[0]), ":",
          str(chosen_one[1]), " (", str(round((chosen_one[1] - chosen_one[0]) /
               44100, 2)), " seconds"]))
    # import original sound
    original = pydub.AudioSegment.from_wav(in_file)
    # create silenced sample
    silenced_sample = create_sample_silenced(in_file, original)
    # create replace silence with clone mask
    create_sample_cloned(in_file, silenced_sample)

def create_sample_cloned(path, original, chosen_one):
    """
    TODO: document
    """
    out_file = out_file_path(path, "clone_fill")
    clone = nr.grow_mask(original.get_sample_slice(chosen_one[0],
            chosen_one[1]), len(original))
    clone_clip = nr.replace_silence(original, clone, 44.1)
    return(export(clone_clip, out_file))

def create_sample_silenced(path, original, chosen_one):
    """
    TODO: document
    """
    out_file = out_file_path(path, "sample_silenced")
    print(''.join(["Building silenced sample 0:", str(chosen_one[0])]))
    sample_clip = original.get_sample_slice(0, chosen_one[0])
    print(''.join(["adding silence ", str(chosen_one[0]), ":", str(chosen_one[
          1])]))
    sample_clip.append(pydub.AudioSegment.silent(duration=(chosen_one[1] -
                       chosen_one[0])))
    print(''.join(["building silenced sample ", str(chosen_one[1]), ":", str(
          len(original))]))
    sample_clip.append(original.get_sample_slice(chosen_one[1], None))
    return(export(sample_clip, out_file))

def export(audio_segment, out_path):
    """
    TODO: document
    """
    print(''.join(["Exporting ", os.path.basename(os.path.dirname(out_path)),
          "/", os.path.basename(out_path)]))
    audio_segment.export(out_path, format="wav")
    return(audio_segment)

def out_file_path(path, method):
    """
    TODO: document
    """
    out_file = os.path.join(os.path.dirname(os.path.dirname(path)), method,
               os.path.basename(path))
    # if output directory does not exist, create
    if not os.path.exists(os.path.dirname(out_file)):
        print (''.join(["Making directory: ", os.path.dirname(out_file)]))
        os.makedirs (os.path.dirname(out_file))
    return out_file

def main():
    t_dir = "/Volumes/data/Research/CDB/openSMILE/audio_files"
    starting_files = iu.i_ursi(t_dir, "no_beeps")
    for file in starting_files:
        create_sample(file)

# ============================================================================
if __name__ == '__main__':
    main()