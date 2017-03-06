============
SM_openSMILE
============

Scripts to analyze waveform files with openSMILE for the study of selective mutism.

`openSMILE_preprocessing`_
--------------------------

These functions were written to determine appropriate masking options for analyzing noise-polluted waveforms in openSMILE.

`openSMILE_runSM`_
------------------
Batch process SM dataset with user-entered openSMILE configuration file.

Load the contents of this folder into openSMILE home directory.

Run runSM() to run openSMILE config file on all Waveform files with extension `*.wav` in `[openSMILE home directory]/all_audio_files/[URSI]/recorded_audio_files/`.

It will ask for config_file. Just give it the filename. The file should live in `[openSMILE home directory]/config`.

`recurse`_
----------
script to recursively collect files

`test_equimpent`_
-----------------
equipment tests

`utilities`_
------------
batch process SM dataset with user-entered openSMILE configuration file

.. _`openSMILE_preprocessing`: https://github.com/shnizzedy/SM_openSMILE/tree/master/openSMILE_preprocessing

.. _`openSMILE_runSM`: https://github.com/shnizzedy/SM_openSMILE/tree/master/openSMILE_runSM

.. _`recurse`: https://github.com/shnizzedy/SM_openSMILE/tree/master/recurse

.. _`test_equipment`: https://github.com/shnizzedy/SM_openSMILE/tree/master/test_equipment

.. _`utilities`: https://github.com/shnizzedy/SM_openSMILE/tree/master/utilities