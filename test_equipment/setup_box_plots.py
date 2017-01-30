#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
setup_box_plots.py

Functions to draw boxplots of the features with the worst parity from the data
output by openSMILE_dir_to_csv for recorder comparisons.

Author:
        – Jon Clucas, 2017 (jon.clucas@childmind.org)

© 2017, Child Mind Institute, Apache v2.0 License
"""
import openSMILE_dir_to_csv as odtc, os, pandas as pd, matplotlib.pyplot as \
       plt, seaborn as sns, subprocess

def plot(dataframe, directory):
    cmi_colors = ["#0067a0", "#919d9d", "#00c1d5", "#b5bd00", "#a31c3f",
                  "#ea234b", "#eeae30", "#f2cd32", "#4db789", "#90d9b9",
                  "#404341", "#e4e4e4", "#090e3c", "#242a6a", "#97e2ef",
                  "#f9e28a", "#d3da5f"]
    sns.set_palette(cmi_colors)
    dataframe = dataframe.drop(['mean', 'median', 'std', 'mad'], axis=1)
    dataframe = dataframe.T
    indices = list(dataframe.index)
    distances = []
    screen = []
    for index in indices:
        distance, on_off = index.split('_', 1)
        distances.append(distance)
        screen.append(on_off)
    dataframe.insert(0, "distance", distances)
    dataframe.insert(0, "screen", screen)
    dataframe = dataframe.drop([dataframe.columns[len(dataframe.columns)-1],
                dataframe.columns[len(dataframe.columns)-2]], axis=1)
    df_long = pd.melt(dataframe, ["distance", "screen"], var_name="features",
                      value_name="openSMILE outputs")
    print(df_long.head(140))
    plt.xticks(rotation=300, ha="left")
    plt.figsize=(22,17)
    plt.dpi=200
    g = sns.boxplot(x="features", y="openSMILE outputs", data=
        df_long.head(n=140), palette=cmi_colors)
    plt.title(''.join(["Worst parity: ", os.path.basename(directory)]))
    plt.tight_layout()
    fig = g.get_figure()
    fig.savefig(os.path.join(directory, "collected/boxplot.png"), dpi=300)
    plt.close()

def main():
    tippy_top = "PMAV"
    top_dirs = [os.path.join(tippy_top, "ComParE_2016"),
                os.path.join(tippy_top, "emobase")]
    for directory in top_dirs:
        if os.path.exists(os.path.join(directory, ".DS_Store")):
            shell_command = ''.join(['rm ', os.path.join(directory,
                            ".DS_Store")])
            print(shell_command)
            subprocess.run(shell_command, shell = True)
        plot(odtc.oS_dir_to_csv(directory), directory)
# ============================================================================
if __name__ == '__main__':
    main()