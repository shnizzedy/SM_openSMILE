#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
noise_replacement.py

Script to replace silenced noises in data sound files.

Author:
        – Jon Clucas, 2016 (jon.clucas@childmind.org)

© 2016, Child Mind Institute, Apache v2.0 License

Created on Mon Dec 19 17:00:00 2016
"""
import fftnoise, math, numpy as np, os, pandas as pd, pydub, random
from scipy import signal
from scipy.io import wavfile

def analyze_and_generate(path):
    """
    Function to find ambient clips, get their amplitude and power spectrum,
    and generate an ambeint mask based on this information.

    Parameters
    ----------
    path : string
        the absolute path of the original soundfile

    Returns
    -------
    mask : pydub audio segment
        the generated ambient mask
    """
    print(''.join(["Analyzing ", path]))
    input_data = wavfile.read(path)

    audio_l = input_data[1][:, 0]
    audio_r = input_data[1][:, 1]
    rate = input_data[0]
    ambience = get_ambient_clips(path)

    for start, stop in ambience:
        try:
            np.concatenate((sample_l, audio_l[start:stop]))
            np.concatenate((sample_r, audio_r[start:stop]))
        except NameError:
            sample_l = audio_l[start:stop]
            sample_r = audio_r[start:stop]

    fft_l = np.fft.fft(sample_l)
    fft_r = np.fft.fft(sample_r)

    l_sample, l_Pxx = signal.periodogram(fft_l, rate)
    r_sample, r_Pxx = signal.periodogram(fft_r, rate)


    l_sound = fftnoise.fftnoise(l_Pxx)
    r_sound = fftnoise.fftnoise(r_Pxx)
    out_file = os.path.join(os.path.dirname(path),"gen_mask.wav")

    wavfile.write(out_file, rate, np.transpose(np.array([l_sound, r_sound])))

    mask = pydub.AudioSegment.from_wav(out_file)
    original = pydub.AudioSegment.from_wav(path)
    print("build baseline")
    baseline = build_new_soundfile(original, rate, None, get_ambient_clips(
               path))
    mask = mask - abs(mask.dBFS - baseline.dBFS)
    mask = grow_mask(mask, len(original))
    mask.export(out_file, format="wav")
    return mask

def borders_frames_to_ms(borders, rate):
    """
    Function to convert a list of 2-item lists or tuples from frames to
    milliseconds.

    Parameters
    ----------
    borders : list
        a list of 2-item lists or tuples, each item of which is a number of
        frames

    rate : float
        frames per millisecond (fps / 1000)

    Returns
    -------
    frame_borders : list
        a list of 2-item lists or tuples, each item of which is a number of
        milliseconds
    """
    frame_borders = []
    for start, stop in borders:
        frame_borders.append((math.floor(start / rate), math.ceil(stop /
                             rate)))
    return frame_borders

def borders_ms_to_frames(borders, rate):
    """
    Function to convert a list of 2-item lists or tuples from milliseconds to
    frames.

    Parameters
    ----------
    borders : list
        a list of 2-item lists or tuples, each item of which is a number of
        milliseconds

    rate : float
        frames per millisecond (fps / 1000)

    Returns
    -------
    frame_borders : list
        a list of 2-item lists or tuples, each item of which is a number of
        frames
    """
    frame_borders = []
    for start, stop in borders:
        frame_borders.append((math.floor(start * rate), math.ceil(stop *
                             rate)))
    return frame_borders

def build_new_soundfile(with_silence, rate, mask, borders):
    """
    Given a soundfile, an optional mask, and a list of time-pairs,
    concatenate the segments outside of the time-pairs, replacing
    the time-pair marked segments with the mask, if applicable.

    Parameters
    ----------
    with_silence : pydub audio segment
        the segment to reconstruct

    rate : float
        frames per millisecond (fps / 1000)

    mask : pydub audio segment or None
        the mask segment to fill from

    borders : list of 2 item lists or tuples or None
        the time-pairs marking the beginning and ends of segments to cut
        or nothing to cut

    Returns
    -------
    new_sound : pydub audio segment
        the reconstructed segment
    """
    if (not borders):
        print("No marked segments.")
        return with_silence
    borders = borders_ms_to_frames(borders, rate)
    segmented_sound = []
    seg_start = 0
    if(borders[0][0] == 0):
        seg_stop = borders[0][1]
        print(''.join(["initial building with segment [0:",
              str(seg_stop), "] out of ", str(len(with_silence) * rate)]))
        segmented_sound.append(with_silence.get_sample_slice(0, seg_stop))
        seg_start = seg_stop
    for pair in borders:
        if(pair[0] > 0):
            try:
                segmented_sound.append(with_silence.get_sample_slice(seg_start,
                                       pair[0]))
                print(''.join(["building with segment [", str(seg_start), ":",
                      str(pair[0]), "]"]))
                if mask:
                    print(''.join([str(math.ceil(pair[1])), ' - ',
                          str(math.floor(pair[0]))]))
                    masked_segment = fill_in(mask, (math.ceil(pair[1]) -
                                     math.floor(pair[0])), rate)
                    segmented_sound.append(masked_segment)
                    print(''.join(["building with mask [", str(pair[0]), ":",
                          str(pair[1]), "]"]))
            except NameError:
                segmented_sound.append(fill_in(mask, math.ceil(pair[1]), rate))
                print(''.join(["building with mask [", str(pair[0]), ":",
                      str(len(with_silence) * rate), "]"]))
            seg_start = pair[1]
    if(seg_start < (len(with_silence) * rate)):
        try:
            segmented_sound.append(with_silence.get_sample_slice(seg_start,
                                   None))
            print(''.join(["final building with segment [", str(seg_start),
                  ":", str(len(
                  with_silence) * rate), "]"]))
        except:
            print("This is the end.")
    if len(segmented_sound) > 1:
        new_sound = segmented_sound[0]
        for i, v in enumerate(segmented_sound):
            if i > 0:
                new_sound = new_sound + segmented_sound[i]
    else:
        new_sound = segmented_sound[0]
    return new_sound

def fill_in(mask, duration, rate):
    """
    Get a section of a mask of the specified duration.

    Parameters
    ----------
    mask : pydub audio segment
        the mask to clip from

    duration : int
        the required duration in frames

    Returns
    -------
    mask : pydub audio segment
        the mask clipped to specified duration

    """
    mask_len = math.ceil(len(mask) * rate)
    print(str(mask_len))
    print(str(duration))
    if (duration >= mask_len):
        start = 0
    else:
        start = random.randrange(0, (mask_len - math.floor(
            duration)), 1)
    print(''.join(["fill in ", str(start), ":", str((start + duration))]))
    mask = mask.get_sample_slice(math.floor(start), math.ceil(start +
           duration))
    return mask

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
    if os.access(path, os.R_OK):
        print(''.join(['    Reading ', path]))
    else:
        print(''.join(['    !!! ', path,
              ' : insufficient permission to read']))
        return []
    # TODO: figure out why this is hanging when called from
    # TODO: generate_sample.create_sample
    input_data = wavfile.read(path)
    print('    read')
    # get numpy array of amplitude values
    audio = input_data[1][:, 0]
    print(''.join(['        left channel: ',str(len(audio))]))
    # get rate
    # rate = input_data[0]
    # t = np.arange(len(audio)) / rate
    # calculate envelope
    print('        calculating envelope')
    envelope = np.abs(signal.hilbert(audio))
    # initialize start, stop, and ambiance lists
    starts, stops, ambience = ([] for i in range(3))
    # initialize start flag
    start_flag = True
    # set threshold
    threshold = np.median(envelope)
    print('        finding ambient segments')
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

def grow_mask(mask, size):
    """
    Function to create a clone mask from an ambient clip.

    Parameters
    ----------
    mask : pydub audio segment
        the ambient clip from which to create the clone

    size : int
        how many milliseconds the clone should last

    Returns
    -------
    mask : pydub audio segment
        an ambient clone mask of specified duration
    """
    print("grow mask")
    while len(mask) < size:
        mask = mask + mask.reverse()
    return mask

def replace_silence(original, mask, rate):
    """
    Function to create a clip in which silences are replaced by masks.

    Parameters
    ----------
    original : pydub audio segment
        the original sound file

    mask : pydub audio segment
        the ambient clip from which to replace the silence

    rate : float
        frames per millisecond (fps / 1000)

    Returns
    -------
    new_sound : pydub audio segment
        the original sound with silence replaced from the specified mask
        
    silence_borders : list
        a list of start and stop times, in milliseconds, of silent segments
    """
    silence_borders = pydub.silence.detect_silence(original, min_silence_len=1,
                                                   silence_thresh = -60)
    print("build new sound")
    print(borders_ms_to_frames(silence_borders, rate))
    new_sound = build_new_soundfile(original, rate, mask, silence_borders)
    return new_sound, silence_borders

def check_conditions(directory, conditions):
    """
    Function to check if a condition is known and accounted for.
    
    Parameters
    ----------
    directory : string
        the name of a directory that is the condition to check for
        
    conditions : list of strings
        a list of known and accounted for conditions
        
    Returns
    -------
    directory : string or None
        either returns an unaccounted-for condition or returns None.
    """
    for condition in conditions:
        if condition in directory:
            return None
    return directory

def build_adultTalk_dataframe(adults_removed_dict):
    """
    Function to build a dataframe specifying which conditions included an
    audibly speaking adult.
    
    Parameters
    ----------
    adults_removed_dict : dictionary
        a dictionary of {URSI, list of string} pairs in which each string is
        the name of a file in which an adult was audible
    
    Returns
    -------
    adults_removed_df : pandas data frame
        a dataframe with one row per URSI and one column per condition
        indicating whether an adult spoke during that condition
    """
    adults_removed_df = pd.DataFrame(columns=["button no", "button w",
                        "vocal no", "vocal w"])
    # TODO: build dataframe
    print(adults_removed_df)

def main():
    necessaries = ["adults_removed", "adults_replaced_pink", "no_beeps"]
    unnecessaries = ["ambient_clip", "clone_fill", "openSMILE_outputs",
                     "recorded_audio_files", "sample_silenced", "garbage",
                     "seawave_results", "timeshifted", ".DS_Store"]
    # tasks = ["button", "vocal"]
    # stranger = ["w", "no"]
    top_dir = input("Top directory: ")
    adults_speak = {}
    # top_dir = "/Volumes/Data/Research/CDB/openSMILE/audio_files/"
    for URSI in os.listdir(top_dir):
        if URSI not in [".DS_Store", "nobeeps"]:
            adults_speak[URSI] = []
            for subdirectory in os.listdir(os.path.join(top_dir, URSI)):
                if os.path.isdir(os.path.join(top_dir, URSI, subdirectory)):
                    if subdirectory in necessaries:
                        if subdirectory == "adults_removed":
                            for wav_file in os.listdir(os.path.join(top_dir,
                                            URSI, subdirectory)):
                                if wav_file.endswith('.wav'):
                                    adults_speak[URSI] = adults_speak[URSI
                                                         ] + [wav_file]
                    elif check_conditions(subdirectory, unnecessaries):
                        print(''.join["Unaccounted for condition: ",
                              subdirectory])
    build_adultTalk_dataframe(adults_speak)
                            

# ============================================================================
if __name__ == '__main__':
        main()