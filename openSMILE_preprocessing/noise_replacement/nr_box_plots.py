#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
nr_box_plots.py

Functions to draw boxplots comparing the fidelity of different noise
replacement methods across a complete set of files.

Author:
        – Jon Clucas, 2017 (jon.clucas@childmind.org)

© 2017, Child Mind Institute, Apache v2.0 License
"""
import csv, os, pandas as pd, matplotlib.pyplot as plt, seaborn as sns, sys
if os.path.abspath('../../../../') not in sys.path:
    if os.path.isdir(os.path.join(os.path.abspath('../../..'), 'SM_openSMILE')
       ):
        sys.path.append(os.path.abspath('../../..'))
    elif os.path.isdir(os.path.join(os.path.abspath('../..'), 'SM_openSMILE')):
        sys.path.append(os.path.abspath('../..'))
    elif os.path.isdir(os.path.join(os.path.abspath('..'), 'SM_openSMILE')):
        sys.path.append(os.path.abspath('..'))
    elif os.path.isdir('SM_openSMILE'):
        sys.path.append(os.path.abspath('.'))
from SM_openSMILE.utilities.cmi_color_pallette import cmi_colors
sns.set_palette(cmi_colors())

def plot(dataframe, directory, y="sum(MAD)", hue=""):
    plt.xticks(rotation=300, ha="left")
    plt.figsize=(22,17)
    plt.dpi=200
    dataframe.loc[:, y] = pd.to_numeric(dataframe.loc[:, y])
    if len(hue) > 0:
        g = sns.boxplot(x="method", y=y, hue=hue, data=dataframe)
        plt.gca().legend_.remove()
        out_name = ''.join(['mad_rank_boxplot_', y, '_by_', hue, '.svg'])
    else:
        g = sns.boxplot(x="method", y=y, data=dataframe)
        out_name = ''.join(['mad_rank_boxplot_', y, '.svg'])
    plt.tight_layout()
    fig = g.get_figure()
    fig.savefig(os.path.join(directory, out_name), dpi=300)
    plt.close()

def main():
    top_dir = "replacement_test_outputs/ambient_clip_replaced"
    header_row = []
    frames = []
    with open(os.path.join(top_dir, "mad_rank_summary_all.csv"), 'r') as f:
        reader = csv.reader(f)
        for index, row in enumerate(reader):
            # get header row
            if index == 0:
                if len(header_row) == 0:
                    header_row = ["config", "csv", "method", *row[1:]]
                    frames.append(header_row)
            # get data rows
            else:
                frames.append(["", "", "", *row[1:]])
                frames[index][0], frames[index][1], frames[index][2] = row[0
                       ].split(" > ")
    # put frames into pandas dataframe
    frames = pd.DataFrame(frames[1:], columns=frames[0])
    for y in ["sum(MAD)", "mean(MAD)"]:
        plot(frames, top_dir, y, "csv")
        plot(frames, top_dir, y)
    """
    for frame in frames['csv'].unique():
        plot(frames.loc[frames['csv'] == frame])
    """
    """
    np.set_printoptions(threshold=np.inf)
    URSI_count = {}
    for index, frame in frames.iterrows():
        URSI = frame['csv'].split("_")[0]
        if URSI in URSI_count:
            URSI_count[URSI] = URSI_count[URSI] + 1
        else:
            URSI_count[URSI] = 1
    print(URSI_count)
    """

                    

# ============================================================================
if __name__ == '__main__':
    main()