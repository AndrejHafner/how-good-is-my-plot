import pandas as pd
import numpy as np

import os
from pathlib import Path
import shutil

from sklearn.model_selection import KFold

# Script for copying all plots into correct folders in final folds.
plots_path = 'D:/project/final'
dst_path = 'D:/project/final_folds'

nr_folds = 5

for f in range(nr_folds):
    Path(os.path.join(dst_path, f'fold{f+1}', 'train')).mkdir(parents=True, exist_ok=True)
    Path(os.path.join(dst_path, f'fold{f + 1}', 'val')).mkdir(parents=True, exist_ok=True)

Path(os.path.join(dst_path, 'test')).mkdir(parents=True, exist_ok=True)

test_data = pd.read_csv('data/test_data.csv', index_col=0)
test_plots = test_data['plot_name'].values

all_data = pd.read_csv('data/final_scores.csv')
all_plots = all_data['plot_name'].values

train_plots = np.setdiff1d(all_plots, test_plots)

kf = KFold(n_splits=nr_folds, shuffle=True)
fold = 0
for train_id, val_id in kf.split(train_plots):
    fold += 1
    train = train_plots[train_id]
    val = train_plots[val_id]

    for plot in train:
        shutil.copy(os.path.join(plots_path, plot), os.path.join(dst_path, f'fold{fold}', 'train', plot))
    for plot in val:
        shutil.copy(os.path.join(plots_path, plot), os.path.join(dst_path, f'fold{fold}', 'val', plot))

for plot in test_plots:
    shutil.copy(os.path.join(plots_path, plot), os.path.join(dst_path, 'test', plot))
