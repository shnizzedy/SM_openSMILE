==============================================================================
mhealthx feature extraction software pipeline
==============================================================================
The mhealthx software package automates features extraction from sensor data.
Behind the scenes, open source Python 3 and other code run within a modular
Nipype pipeline framework on Linux (tested with Python 3.5 on Ubuntu 14.04).

  - For help in a terminal window:  mhealthx -h
  - `GitHub repository <https://github.com/binarybottle/mhealthx>`_
  - `Apache v2.0 license <http://www.apache.org/licenses/LICENSE-2.0>`_

..
    1. Inputs
    2. Processing
    3. Outputs

:Release: |version|
:Date: |today|

Links:

.. toctree::
    :maxdepth: 1

    FAQ <faq.rst>
    license

- `GitHub <http://github.com/binarybottle/mhealthx>`_

* :ref:`modindex`
* :ref:`genindex`

------------------------------------------------------------------------------
_`Inputs`
------------------------------------------------------------------------------
All data are optionally accessed from Synapse tables in a project on synapse.org:

  - Voice: WAV files
  - Tapping: JSON files
  - Accelerometry: JSON files

------------------------------------------------------------------------------
_`Processing`
------------------------------------------------------------------------------
  - Run different feature extraction software packages on the input data.
  - Output features to new tables.

------------------------------------------------------------------------------
_`Outputs`
------------------------------------------------------------------------------
  - Tables
