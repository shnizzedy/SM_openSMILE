==============================================================================
mhealthx feature extraction software pipeline
==============================================================================<h1>
The mhealthx software package automates features extraction from sensor data.
Behind the scenes, open source Python 3 and other code run within a modular
Nipype pipeline framework on Linux (tested with Python 3.5 on Ubuntu 14.04).

The `Child Mind Institute <http://childmind.org>`_ is developing mhealthx 
as an open source feature extraction pipeline for sensor data. 
`Arno Klein <http://binarybottle.com>`_ originally created mhealthx at 
`Sage Bionetworks <http://sagebase.org>`_ to extract features from mobile 
health research apps such as `mPower <http://parkinsonmpower.org>`_, 
the Parkinson disease symptom tracking app built on top of Apple's ResearchKit.
See our `GitHub repository <https://github.com/binarybottle/mhealthx>`_.

In particular, please see:

    `Gait <http://binarybottle.github.io/mhealthx/api/generated/mhealthx.extractors.pyGait.html>`_: feature extraction from accelerometer data
    `Tapping <http://binarybottle.github.io/mhealthx/api/generated/mhealthx.extractors.tapping.html>`_: feature extraction from touchscreen data
    `Main function <http://binarybottle.github.io/mhealthx/api/generated/mhealthx.extract.html>`_ that calls all the feature extraction methods

Also, see preliminary 
`data-driven information visualizations <http://binarybottle.github.io/mhealthx/reports/index.html>`_ displaying mock data

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
