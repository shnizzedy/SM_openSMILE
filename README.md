# SM_openSMILE
Scripts to analyze waveform files with openSMILE for the study of selective mutism.

## [openSMILE_preprocessing](https://github.com/shnizzedy/SM_openSMILE/tree/master/openSMILE_preprocessing "functions to prepare files for openSMILE analysis")

## [openSMILE_runSM](https://github.com/shnizzedy/SM_openSMILE/tree/master/openSMILE_runSM "batch process SM dataset with user-entered openSMILE configuration file")

## iterate_ursis
Script to iterate through [top_directory]/URSI/[subdirectory]/files structure
and return a list of included files.

### i_ursi(top_in, sub_in)
Function to iterate through [top_directory]/URSI/[subdirectory]/files structure
and return a list of included files.

## make_long_soundfiles
Create mylist.txt and run ffmpeg -f concat for each (particpant + condition).

### make_long_wav(ursi_dir, mylist_txt)
Function to run "ffmpeg -f concat" on mylist_txt.

### make_file_list(topdir, ursi, condition)
Function to make a *.txt file for each (ursi + condtion)

### create_long_soundfiles()
Function to take 3" sound files and splice them back together.

## openSMILE_csv
Script to format openSMILE emobase *.csv output combined with dx data into a
set of new [participant × file × feature × dx] *.csv files, one for each
experimental condition.

Short (segmented) and long (concatenated) outputs are handled separately.

### get_features(csv_file)
Function to get features from openSMILE emobase configuration file csv outputs.

### get_dx(ursi, dx_dictionary = None)
Function to get a participant's diagnosis from a dictionary of diagnoses.

### get_dx_dictionary()
Function to create a diagnosis dictionary from a csv file containing diagnoses.

### create_sample_row(ursi, condition, config_file)
Function to create a row for a training set.

### create_samples(config_file)
Function to create samples for a training set based on trial condition.