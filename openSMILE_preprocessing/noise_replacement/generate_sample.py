#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_sample.py

Script to find a 2.5 second clip of ambient noise and silence that clip.

Author:
        – Jon Clucas, 2016 (jon.clucas@childmind.org)

© 2016, Child Mind Institute, Apache v2.0 License
Created on Wed Dec 21 16:34:37 2016

@author: jon.clucas
"""
import iterate_ursis as iu, noise_replacement as nr, pydub, random

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
	out_file = os.path.join([os.path.dirname(os.path.dirname(in_file)), 
	             "sample_silenced", os.path.basename(in_file)])
	options = nr.get_ambient_clips(in_file)
	remaining_options = []
	for pair in options:
		if ((pair[1] - pair[0]) > 110250):
			remaining_options.append(pair)
	num_options = len(remaining_options)
	if num_options == 0:
		remaing_options = options
		num_options = len(remaining_options)
	chosen_one = remaining_options[random.randrange(0, num_options)]
	original = pydub.AudioSegment.from_wav(in_file)
	sample_clip = original.get_sample_slice(0, chosen_one[0])
	sample_clip.append(pydub.AudioSegment.silent(duration=(chosen_one[1] -
	                   chosen_one[0])))
	sample_clip.append(original.get_sample_slice(chosen_one[1], None)
	print(''.join(["Exporting ", os.path.basename(os.path.dirname(outfile)), 
	      "/", os.path.basename(out_file)]))
	sample_clip.export(out_file, format="wav")

def main():
	iu.i_ursi("/Volumes/data/Research/CDB/openSMILE/", "no_beeps", create_sample, None, ['.contains("long")', '.ends_with(".wav")'])
		
# ============================================================================
if __name__ == '__main__':
    main()