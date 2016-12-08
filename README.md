# openSMILE-preprocessing
functions to prepare files for openSMILE analysis

These functions were written to determine appropriate masking options for analyzing noise-polluted waveforms in openSMILE.

# arff_csv_to_pandas
functions to import openSMILE outputs to Python pandas

## arff_to_pandas(arff_data,method,config_file,condition)
function to convert python arff data into a pandas series

## build_dataframe(wd,config_file,condition,methods)
function to pull openSMILE output csv into a pandas series
   
## get_oS_data(csvpath,method,config_file,condition)
function to pull openSMILE output csv into a pandas series

# condition_comparison
functions to compare openSMILE outputs for various noise replacement methods

## iterate_through()
function to iterate through openSMILE configuration files and noise conditions
