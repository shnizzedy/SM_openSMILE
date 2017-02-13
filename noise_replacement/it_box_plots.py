#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
it_box_plots.py

Functions to draw boxplots comparing the fidelity of different noise
replacement methods across a single test file.

Author:
        – Jon Clucas, 2017 (jon.clucas@childmind.org)

© 2017, Child Mind Institute, Apache v2.0 License
"""
import csv, os, pandas as pd, nr_box_plots as nbp

def main():
    top_dir = "replacement_test_outputs/initial_test"
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
    nbp.plot(frames.loc[frames['csv'] == 'ambient'], top_dir, "sum(MAD)")
    nbp.plot(frames.loc[frames['csv'] == 'ambient'], top_dir, "mean(MAD)")
    
                    

# ============================================================================
if __name__ == '__main__':
    main()