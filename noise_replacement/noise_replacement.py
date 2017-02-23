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
import os, sys
if os.path.abspath('../../..') not in sys.path:
    sys.path.append(os.path.abspath('../../..'))
import csv, fftnoise, math, numpy as np, pandas as pd, pydub, random
from xml.etree import ElementTree as ET
from scipy import signal
from scipy.io import wavfile
from SM_openSMILE.openSMILE_preprocessing.noise_replacement import \
     generate_sample as gs
from SM_openSMILE.openSMILE_runSM import openSMILE_csv as oS_c

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
    silence_table(path, ambience)

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
        """
        print(''.join(["initial building with segment [0:",
              str(seg_stop), "] out of ", str(len(with_silence) * rate)]))
        segmented_sound.append(with_silence.get_sample_slice(0, seg_stop))
        """
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

def silence_table(top_dir, silence_borders):
    out_path = '_'.join([top_dir.strip('.wav'), "silences.csv"])
    with open(out_path, "w") as f:
        writer = csv.writer(f)
        writer.writerows(silence_borders)

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
    conditions = ["button no", "button w", "vocal no", "vocal w"]
    dx = oS_c.get_dx_dictionary()
    # /Volumes/Data/Research/CDB/SM_Sound_Analysis/SM_DX_summary_status_dx.csv
    adults_removed_df = pd.DataFrame(columns=conditions.append("SM dx"),
                        dtype=bool)
    for participant in adults_removed_dict:
        row = [False, False, False, False, False]
        for item in adults_removed_dict[participant]:
            if "button_no" in item:
                row[0] = True
            if "button_w" in item:
                row[1] = True
            if "vocal_no" in item:
                row[2] = True
            if "vocal_w" in item:
                row[3] = True
        if dx[participant] == "SM":
            row[4] = True
        adults_removed_df = adults_removed_df.append(pd.Series(row, name=
                            participant, index=conditions))
    adults_removed_df = adults_removed_df.astype(bool)
    return adults_removed_df

def get_adults_table(top_dir):
    """
    Function to build a dataframe of participant audio files that have had at
    least one adult vocalization removed from them. Also notifies of any
    unaccounted-for conditions.
    
    Parameters
    ----------
    top_dir : string
        path to the top directory
        
    Returns
    -------
    adults_speak_df : pandas dataframe
        a dataframe with boolean values for whether an "adults removed" file
        for each condition for each participant
    """
    necessaries = ["adults_removed", "adults_replaced_pink", "no_beeps"]
    unnecessaries = ["ambient_clip", "clone_fill", "openSMILE_outputs",
                     "recorded_audio_files", "sample_silenced", "garbage",
                     "seawave_results", "timeshifted", ".DS_Store"]
    adults_speak = {}
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
    return build_adultTalk_dataframe(adults_speak)

def check_xml_for_silence(sbf):
    """
    Function to determine if a section marked in an Audacity xml file contains
    silence or sound.
    
    Parameters
    ----------
    sbf : dictionary
        `<simpleblockfile>` tag parsed from Audacity xml file
        
    Returns
    -------
    silence: boolean
        True if silence, False if sound
    """
    if float(sbf['min']) == 0.0 and float(sbf['max']) == 0.0 and float(sbf[
             'rms']) == 0.0:
        return True
    else:
        return False

def parse_audacity_file(ar_filepath):
    """
    Function to parse Audacity xml file to find marked silences.
    
    Parameters
    ----------
    ar_filepath : string
        path to wav_file with audacity file saved in same directory with same
        basenameinitial
        
    Returns
    -------
    list_of_silences : list of tuples
        list of (start_time, stop_time) tuples of marked silences in
        milliseconds
        
    list_of_normality : list of tuples
        list of (start_time, stop_time) tuples of marked non-silent segments in
        milliseconds
    """
    list_of_silences = []
    list_of_normality = []
    xml_filepath = ''.join([ar_filepath.strip('.wav'), '.aup'])
    aud = ET.parse(xml_filepath)
    root = aud.getroot()
    for child in root:
        # our tracks are stereo, but our edits are binaural, so we only need to
        # check one channel. We're using left.
        if (child.tag.endswith("wavetrack") and int(child.attrib['channel']) ==
            0):
            for wavetrack in child:
                time1 = float(wavetrack.attrib['offset']) * float(root.attrib[
                        'rate'])
                if wavetrack.tag.endswith("waveclip"):
                    for waveclip in wavetrack:
                        if waveclip.tag.endswith("sequence"):
                            time2 = float(waveclip.attrib['numsamples'])
                            for sequence in waveclip:
                                if sequence.tag.endswith('waveblock'):
                                    for waveblock in sequence:
                                        if waveblock.tag.endswith(
                                           'silentblockfile'):
                                            time_tuple = (round(time1), round(
                                                         time1 + time2))
                                            if (time_tuple not in
                                                    list_of_silences):
                                                        list_of_silences \
                                                        .append(time_tuple)
                                        if waveblock.tag.endswith(
                                           'simpleblockfile'):
                                            time_tuple = (round(time1), round(
                                                         time1 + time2))
                                            if check_xml_for_silence(
                                              waveblock.attrib):
                                                if (time_tuple not in
                                                    list_of_silences):
                                                        list_of_silences \
                                                        .append(time_tuple)
                                            else:
                                                if (time_tuple not in
                                                    list_of_normality):
                                                        list_of_normality \
                                                        .append(time_tuple)
    return(borders_frames_to_ms(list_of_silences, 44.1), borders_frames_to_ms(
            list_of_normality, 44.1))

def concat_adults(adult_path, segmentation):
    """
    Function to concatenate segments of adult sounds.
    
    Parameters
    ----------
    adult_path : string
        path to original file
    
    segmentation : list of tuples
        a list of (start_time, stop_time) tuples of adult sounds to concatenate
        
    Returns
    -------
    None
    
    Outputs
    -------
    wav_file
        a waveform of the concatenated file in an "adults" directory at the
        same depth as the original parent directory with the same basename as
        the original file
    """
    out_path = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(
               adult_path))), "adults", os.path.basename(adult_path))
    if not os.path.exists(os.path.dirname(out_path)):
        os.makedirs(os.path.dirname(out_path))
    adult = pydub.AudioSegment.from_wav(adult_path)
    print(''.join(["Building ", out_path, " from ", adult_path]))
    concatenated = build_new_soundfile(adult, 44.1, None, segmentation)
    concatenated.export(out_path, format="wav")
    
def choose_mask(original, ambience):
    """
    Function to choose a segment of ambience from which to build our clone mask
    
    Parameters
    ----------
    original : string
        path to the original sound
        
    ambience : list of tuples
        a list of starts and stops of ambient segments in frames
        
    Returns
    -------
    mask : pydub audio segment
        a clip of just ambience
        
    Outputs
    -------
    waveform file
        a waveform of the segment of ambeint noise used as a clone mask, saved
        in a "clone_masks" directory at the same depth as the original filepath
        with the same basename as the original file
    """
    out_path = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(
               original))), "clone_masks", os.path.basename(original))
    if not os.path.exists(os.path.dirname(out_path)):
        os.makedirs(os.path.dirname(out_path))
    # how many ambient clips?
    print(''.join([str(len(ambience)), " ambient clips"]))
    remaining_options = []
    # start by looking for clips 2.5 seconds or longer
    desired_duration = 110250
    while len(remaining_options) == 0:
        remaining_options = gs.check_clip_len(ambience, desired_duration)
        # reduce desired duration by .25 seconds
        desired_duration = desired_duration - 11025
    num_options = len(remaining_options)
    print(''.join([str(num_options), " ≥ ", str(round(desired_duration /
          44100, 2)), " seconds"]))
    # choose a clip to extract
    chosen_one = []
    chosen_one.append(remaining_options[random.randrange(0, num_options)])
    print(chosen_one)
    # store length of chosen_one
    chosen_one_l = chosen_one[0][1] - chosen_one[0][0]
    print(''.join(['chosen clip : ', str(chosen_one[0][0]), ":",
          str(chosen_one[0][1]), " (~", str(round(chosen_one_l /
               44100, 2)), " seconds)"]))
    # import original sound
    print(''.join(["Loading original file into pydub"]))
    original_sound = pydub.AudioSegment.from_wav(original)

    # save copy of ambient clip
    clip = original_sound.get_sample_slice(chosen_one[0][0], chosen_one[0][1])
    gs.build_sample(out_path, clip, None, None)
    return clip

def replace_adults(path, borders, mask, rate):
    """
    Function to replace all marked adult segments.
    
    Parameters
    ----------
    path : string
        path to original file
    
    borders : list of tuples
        list of (start_time, stop_time) tuples of segments to replace
        
    mask : pydub audio segment
        the mask with which to replace the adults
        
    rate : float
        the frame rate in milliseconds
        
    Returns
    -------
    replaced : pydub audio segment
        the sound with the adults replaced
        
    Output
    ------
    waveform file
        a waveform of the segment of ambeint noise used as a clone mask, saved
        in an "adults_replaced_clone" directory at the same depth as the
        original filepath with the same basename as the original file
    """
    out_path = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(
               path))), "adults_replaced_clone", os.path.basename(path))
    if not os.path.exists(os.path.dirname(out_path)):
        os.makedirs(os.path.dirname(out_path))
    original = pydub.AudioSegment.from_wav(path)
    replaced = build_new_soundfile(original, rate, mask, borders)
    print(''.join(["Saving ", out_path]))
    replaced.export(out_path, format="wav")
    return(replaced)

def save_list(in_path, condition, keep_list):
    """
    TODO: document
    """
    with open(''.join([in_path.strip('.wav'), '_', condition, '.csv']), 'w') \
              as out_path:
        csv_out = csv.writer(out_path)
        csv_out.writerow(['start_time', 'stop_time'])
        for row in keep_list:
            csv_out.writerow(row)

def main():
    # tasks = ["button", "vocal"]
    # stranger = ["w", "no"]
    top_dir = input("Top directory: ")
    # top_dir = "/Volumes/Data/Research/CDB/openSMILE/audio_files/"
    as_dir = os.path.join(os.path.dirname(os.path.dirname(top_dir)),
             'adults_speak')
    as_path = os.path.join(as_dir, 'adults_speak.csv')
    if not os.path.exists(os.path.dirname(as_dir)):
        os.makedirs(os.path.dirname(as_dir))
    if not os.path.exists(as_path):
        adults = get_adults_table(top_dir)
        adults.to_csv(as_path)
        adults.apply(pd.value_counts).to_csv(os.path.join(as_dir,
                     'counts.csv'))
    print('\n')
    for URSI in os.listdir(top_dir):
        if URSI not in [".DS_Store", "nobeeps"]:
            ar_path = os.path.join(top_dir, URSI, 'adults_removed')
            if os.path.isdir(ar_path):
                for wav_file in os.listdir(ar_path):
                    if wav_file.endswith('.wav'):
                        full_path = os.path.join(ar_path, wav_file)
                        original_path = os.path.join(top_dir, URSI, "no_beeps",
                                        os.path.basename(wav_file))
                        silences, sounds = parse_audacity_file(full_path)
                        save_list(full_path, "adults", silences)
                        save_list(full_path, "no_adults", sounds)
                        concat_adults(original_path, sounds)
                        ambience = get_ambient_clips(original_path)
                        mask = choose_mask(original_path, ambience)
                        replace_adults(original_path, silences, mask, 44.1)

# ============================================================================
if __name__ == '__main__':
        main()