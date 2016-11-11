#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Batch process SM dataset with user-entered openSMILE configuration file.

Author:
	– Jon Clucas, 2016 (jon.clucas@childmind.org)
	
© 2016 Child Mind Institute

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

This script uses functions from mhealthx
( http://sage-bionetworks.github.io/mhealthx/ ).

Authors:
    - Arno Klein, 2015  (arno@sagebase.org)  http://binarybottle.com

Copyright 2015,  Sage Bionetworks (http://sagebase.org), Apache v2.0 License
"""
# extract and mhealthx.utilities are from mhealthx
# ( http://sage-bionetworks.github.io/mhealthx/ ).
# os is Python's operating system library.
# pandas is Python data analysis library.
import mhealthx.extract as ex, mhealthx.utilities, os, pandas as pd

"""
Run from openSMILE home directory.
This script gets a configuration filename from the user, then
iteratively applies that configuration to
all wav files in "./all_audio_files/*".
"""
def main():
	# get config filename from user.
	config_file = raw_input('config file filename: ')
	# get subdirectories of "./all_audio_files/*".
	for root, dirs, files in os.walk('all_audio_files'):
		for participant in dirs:
			# get each participant.
			if participant.startswith('M004'):
				# declare row to pass to
				# ex.run_openSMILE(audio_file, command, flag1, flags, flagn,
				#				   args, closing, row, table_stem, save_rows)
				row = None
				for proot, pdirs, pfiles in os.walk(os.path.join(root,participant)):
					# get each audio file
					for wav in pfiles:
						# include only files with waveform extension
						if wav.endswith('.wav'):
							row, table_path = ex.run_openSMILE(os.path.join(proot),'SMILExtract',
										   '-I','-C','-O',''.join(['config/',config_file]),
										   '',row,''.join(['./',participant]),True)


if __name__ == '__main__':
	main()
