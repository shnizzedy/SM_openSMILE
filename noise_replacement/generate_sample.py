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

def build_sample(path, original, chosen_one, mask):
    """
    Function to create a sample file in which the chosen clip of ambience is
    replaced with a cloned clip of ambience.

    Parameters
    ----------
    path : string
        absolute path where the new clip should be saved

    original : pydub audio segment
        the clip from which to replace the silence with a clone

    chosen_one : 2-item iterable (tuple or list)
        the start and stop times of the ambience or silence in the clip which
        will be replaced with the mask

    Returns
    -------
    new_clip : pydub audio segment
        a clip that matches original except that the marked silence or ambience
        is filled with a matching-duration segment of the specified mask
    """
    new_clip = nr.build_new_soundfile(original, 44.1, mask, chosen_one)
    print(''.join(["Saving ", path]))
    return(export(new_clip, path))

def check_clip_len(options, duration):
    """
    Function to determine the number of clips of a specified duration.

    Parameters
    ----------
    options : list of 2-item tuples or lists
        start and stop times to evaluate

    duration : numeric (int or float)
        minimum desired clip duration

    Returns
    -------
    remaining_options : list of 2-item tuples or lists or empty list
        start and stop times that are at least sepcified duration, or an empty
        list if no given clips are sufficiently long
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
    # choose a clip to extract
    chosen_one = []
    chosen_one.append(remaining_options[random.randrange(0, num_options)])
    ms_chosen_one = nr.borders_frames_to_ms(chosen_one, 44.1)
    print(chosen_one)
    # store length of chosen_one
    chosen_one_l = chosen_one[0][1] - chosen_one[0][0]
    print(''.join(['chosen clip : ', str(chosen_one[0][0]), ":",
          str(chosen_one[0][1]), " (~", str(round(chosen_one_l /
               44100, 2)), " seconds)"]))
    # import original sound
    print(''.join(["Loading original file into pydub"]))
    original = pydub.AudioSegment.from_wav(in_file)

    # save copy of ambient clip
    clip = original.get_sample_slice(chosen_one[0][0], chosen_one[0][1])
    out_file = out_file_path(in_file, "ambient_clip")
    build_sample(out_file, clip, None, None)

    # create silenced sample
    out_file = out_file_path(in_file, "sample_silenced")
    print("Creating silence mask")
    silence = pydub.AudioSegment.silent(duration=int(round(chosen_one_l / 44.1,
                                        2)))
    print(chosen_one)
    silenced_sample = build_sample(out_file, original, ms_chosen_one, silence)

    # create replace silence with clone mask
    out_file = out_file_path(in_file, "clone_fill")
    clone = nr.grow_mask(clip, len(original))
    build_sample(out_file, silenced_sample, ms_chosen_one, clone)

    # create timeshifted sample
    out_file = out_file_path(in_file, "timeshifted")
    build_sample(out_file, silenced_sample, ms_chosen_one, None)

def export(audio_segment, out_path):
    """
    Function to export a pydub audio segment to a local waveform file.

    Parameters
    ----------
    audio_segment : pydub audio segment
        the segment to export

    out_path : string
        absolute path of the location in which to save file

    Returns
    -------
    audio_segment : pydub audio segment
        the same segment (so that this function can be called in a return
        statement)
    """
    print(''.join(["Exporting ", os.path.basename(os.path.dirname(out_path)),
          "/", os.path.basename(out_path)]))
    audio_segment.export(out_path, format="wav")
    return(audio_segment)

def out_file_path(path, method):
    """
    Function to build an export filepath based on the original filepath and the
    method being investigated.

    Parameters
    ----------
    path : string
        absolute path of the original file

    method : string
        method of investigation (to be used as a subdirectory)

    Returns
    -------
    out_file : string
        absolute path of the location in which to save file
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
