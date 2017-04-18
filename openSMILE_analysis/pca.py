#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pca.py

Run PCA analyses on
[n_participants × n_files × n_features × n_Dxs]
*.csv file from openSMILE_csv.py

Authors:
	– Jon Clucas, 2017 (jon.clucas@childmind.org)

@author: jon.clucas
"""

from sklearn.decomposition import FactorAnalysis, PCA
from sklearn.preprocessing import LabelEncoder
import ast, csv, numpy as np, os, sys
if os.path.abspath('../../') not in sys.path:
    if os.path.isdir(os.path.join(os.path.abspath('../..'), 'SM_openSMILE')):
        sys.path.append(os.path.abspath('../..'))
    elif os.path.isdir(os.path.join(os.path.abspath('..'), 'SM_openSMILE')):
        sys.path.append(os.path.abspath('..'))
    elif os.path.isdir('SM_openSMILE'):
        sys.path.append(os.path.abspath('.'))
from itertools import zip_longest
from SM_openSMILE.cfg import conditions, configs, oSdir, replacements

def main():
    for cfg in configs:
        labels = []
        with open(os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(
                  oSdir)), 'configs', cfg, ''.join([cfg, '_features.csv']))),
                  'r') as lp:
            lreader = csv.reader(lp)
            for row in lreader:
                labels.append(row[1])
        np_labels = np.array(labels)
        for replacement in replacements:
            for condition in conditions:
                print(cfg, end=" : \n\t")
                print(replacement, end=" : ")
                print(condition.strip('_'))
                pca = PCA(n_components=12)
                fa = FactorAnalysis(n_components=12)
                features = []
                dx = []
                n_samples = 0
                n_features = 0
                rpath = os.path.join(oSdir, cfg, ''.join([replacement,
                       condition, 'feature_data.csv']))
                opath = os.path.join(oSdir, cfg, ''.join(['original',
                        condition, 'feature_data.csv']))
                if(os.path.exists(rpath)):
                    # fill in unaltered rows when no altered row exists
                    with open(rpath, 'r') as rf, open(opath, 'r') as of:
                        rreader = csv.reader(rf)
                        oreader = csv.reader(of)
                        for rrow, orow in zip_longest(rreader, oreader):
                            if rrow:
                                if len(rrow) > 0:
                                    row = rrow
                            else:
                                row = orow
                            for column in row:
                                column = ast.literal_eval(column)
                                if (column[0] != "['unknown']"):
                                    enc = LabelEncoder()
                                    enc.fit(np.array(column[0]))
                                    for feature in list(column[0]):
                                        try:
                                            feature = float(feature)
                                        except:
                                            feature = enc.transform(np.array([
                                                  feature]))[0]
                                        features.append(feature)
                                        if n_samples == 0:
                                            n_features = n_features + 1
                                    dx.append(column[1])
                                    n_samples = n_samples + 1
                np_features = np.array(features).reshape(n_samples, n_features)
                np_dx = np.array(dx).reshape(n_samples)
                pca.fit(np_features, np_dx)
                fa.fit(np_features, np_dx)
                print(pca.components_)
                print(pca.explained_variance_ratio_)
                print(fa.components_)

# ============================================================================
if __name__ == '__main__':
    main()