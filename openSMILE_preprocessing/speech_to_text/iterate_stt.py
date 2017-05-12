#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import utilities.recurse.recurse as recurse
import openSMILE_preprocessing.speech_to_text.speech as speech

top_dirs = ["/Volumes/Jon.Clucas/recorders/sentences/last_15_seconds", "/Volumes/Jon.Clucas/recorders/word_list/last_15_seconds"]
for top_dir in top_dirs:
	file_list = recurse.filter_recurse(top_dir, ".endswith('.flac')")
	for file in file_list:
	    speech.google_speech(file)