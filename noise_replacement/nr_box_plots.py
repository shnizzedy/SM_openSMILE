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
import csv, os, seaborn as sns

global cmi_colors
cmi_colors = ["#0067a0", "#919d9d", "#00c1d5", "#b5bd00", "#a31c3f", "#ea234b",
              "#eeae30", "#f2cd32", "#4db789", "#90d9b9", "#404341", "#e4e4e4",
              "#090e3c", "#242a6a", "#97e2ef", "#f9e28a", "#d3da5f"]
sns.set_palette(cmi_colors)

def plot(URSI, dataframe):
    print(dataframe)

def main():
    # TODO
    tippy_top = "replacement_test_outputs/ambient_clip_replaced"
    for URSI in os.listdir(tippy_top):
        if URSI != ".DS_Store":
            top_dir = os.path.join(tippy_top, URSI, "mad_ranks/ComParE_2016")
            if os.path.exists(top_dir):
                with open(os.path.join(top_dir, "mad_rank_summary_all.csv"),
                          'r') as f:
                    # TODO
                    pass

# ============================================================================
if __name__ == '__main__':
    main()