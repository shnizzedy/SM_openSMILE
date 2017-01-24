# openSMILE_runSM
Batch process SM dataset with user-entered openSMILE configuration file.

Load the contents of this folder into openSMILE home directory.

Run runSM() to run openSMILE config file on all Waveform files with
extension *.wav in [openSMILE home directory]/all_audio_files/[URSI]/recorded_audio_files/ .

It will ask for config_file. Just give it the filename. The file should live in [openSMILE home directory]/config .

## [`openSMILE_csv.py`](https://github.com/shnizzedy/SM_openSMILE/blob/master/openSMILE_csv.py)
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