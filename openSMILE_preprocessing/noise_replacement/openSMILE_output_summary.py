#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
openSMILE_output_summary.py

Functions to combine and plot emobase and ComParE_2016 summary outputs.

Author:
        – Jon Clucas, 2017 (jon.clucas@childmind.org)
© 2017, Child Mind Institute, Apache v2.0 License
"""
from urllib.request import urlretrieve
import nr_box_plots as nbp, os, pandas as pd

def get_df(config_summary_url):
    """
    Function to get a summary table from a web-accessible URL.
    
    Parameters
    ----------
    config_summary_url : string
        url of table to import
        
    Returns
    -------
    config_summary_df : pandas dataframe
        table from url
    """
    return pd.read_csv(urlretrieve(config_summary_url)[0])

def main():
    compare_url = 'https://osf.io/pgevr/?action=download&version=1'
    emobase_url = 'https://osf.io/rdn82/?action=download&version=1'
    dfs = []
    for url in [compare_url, emobase_url]:
        dfs.append(get_df(url))
    summary = pd.merge(pd.concat((dfs[0], dfs[1])).groupby('method').sum(
              ).filter(regex='sum*'), pd.concat((dfs[0], dfs[1])).groupby(
              'method').mean().filter(regex='mean*'), left_index=True,
              right_index=True)
    summary['method'] = summary.index
    summary = summary[['method', 'sum(MAD)', 'mean(MAD)', 'rank(sum(MAD))',
              'rank(mean(MAD))']]
    summary.sort_values('rank(mean(MAD))', inplace=True)
    out = os.path.join('.', 'replacement_test_outputs',
          'adults_replaced_summary')
    if not os.path.exists(out):
        os.makedirs(out)
    summary.to_csv(os.path.join(out, 'mad_rank_summary.csv'), index=False)
    for y in ["sum(MAD)", "mean(MAD)"]:
        nbp.plot(summary, out, y)
    
# ============================================================================
if __name__ == '__main__':
    main()