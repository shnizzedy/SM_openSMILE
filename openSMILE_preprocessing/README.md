# openSMILE-preprocessing
functions to prepare files for openSMILE analysis

These functions were written to determine appropriate masking options for analyzing noise-polluted waveforms in openSMILE.

# [`arff_csv_to_pandas.py`](https://github.com/shnizzedy/SM_openSMILE/tree/master/openSMILE_preprocessing/arff_csv_to_pandas.py "functions to import openSMILE outputs to Python pandas")
functions to import openSMILE outputs to Python pandas

## arff_to_pandas(arff_data,method,config_file,condition)
function to convert python arff data into a pandas series

## build_dataframe(wd,config_file,condition,methods)
function to pull openSMILE output csv into a pandas series
   
## get_oS_data(csvpath,method,config_file,condition)
function to pull openSMILE output csv into a pandas series

# [`condition_comparison.py`](https://github.com/shnizzedy/SM_openSMILE/tree/master/openSMILE_preprocessing/condition_comparison.py "functions to compare openSMILE outputs for various noise replacement methods")
functions to compare openSMILE outputs for various noise replacement methods

## iterate_through()
function to iterate through openSMILE configuration files and noise conditions

## mean_absolute_deviation_rank(dataframe)
function to calculate the number of full mean average deviations each value is across each config_file+condition.

# [`condition_comparison2.py`](https://github.com/shnizzedy/SM_openSMILE/tree/master/openSMILE_preprocessing/condition_comparison2.py "functions to compare openSMILE outputs for two recording methods.")
functions to compare openSMILE outputs for two recording methods

## build_dataframe(wd, config_file, condition, methods, entity)
Function to pull openSMILE output csv into a pandas dataframe

## iterate_through()
Function to iterate through openSMILE configuration files and noise conditions.

## mean_absolute_deviation_rank(dataframe)
Function to calculate the number of full mean average deviations each value is across each config_file+condition.

# [`convert_dir_to_flac.py`](https://github.com/shnizzedy/SM_openSMILE/tree/master/openSMILE_preprocessing/convert_dir_to_flac.py "script to quickly convert all mp3 and mxf files in a directory to flac files")
script to quickly convert all mp3 and mxf files in a directory to flac files

# [`convert_dir_to_wav.py`](https://github.com/shnizzedy/SM_openSMILE/tree/master/openSMILE_preprocessing/convert_dir_to_wav.py "script to quickly convert all mp3 and mxf files in a directory to waveform files")
script to quickly convert all mp3 and mxf files in a directory to waveform files

# [`make_long_soundfiles.py`](https://github.com/shnizzedy/SM_openSMILE/blob/master/make_long_soundfiles.py)
Create mylist.txt and run ffmpeg -f concat for each (particpant + condition).

## make_long_wav(ursi_dir, mylist_txt)
Function to run "ffmpeg -f concat" on mylist_txt.

## make_file_list(topdir, ursi, condition)
Function to make a *.txt file for each (ursi + condtion)

## create_long_soundfiles()
Function to take 3" sound files and splice them back together.

# [`mp3_to_wav.py`](https://github.com/shnizzedy/SM_openSMILE/tree/master/openSMILE_preprocessing/mp3_to_wav.py "script to quickly convert an mp3 file to a waveform file")
script to quickly convert an mp3 file to a waveform file

## mp3_to_wav(in_file)
get the mp3; make an output filename; do the conversion verbosely

# [`mxf_to_wav.py`](https://github.com/shnizzedy/SM_openSMILE/tree/master/openSMILE_preprocessing/mxf_to_wav.py "script to quickly convert an mxf file to a waveform file")
script to quickly convert an mxf file to a waveform file

## mxf_to_wav(in_file)
get the mxf; make an output filename; do the conversion verbosely

# [`noise_replacement`](https://github.com/shnizzedy/SM_openSMILE/tree/master/openSMILE_preprocessing/noise_replacement "scripts to replace unwanted noise with reasonable ambient replacement noise")
scripts to replace unwanted noise with reasonable ambient replacement noise

# [`openSMLIE_outputs`](https://github.com/shnizzedy/SM_openSMILE/tree/master/openSMILE_preprocessing/openSMILE_outputs "outputs from openSMILE to compare noise replacement conditions")
outputs from openSMILE to compare noise replacement conditions

