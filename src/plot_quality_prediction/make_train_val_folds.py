import pandas as pd
import numpy as np

from sklearn.model_selection import KFold

# Script for copying all plots into correct folders in final folds.
plots_path = 'D:/project/final'

nr_folds = 5

test_data = pd.read_csv('data/test_data.csv', index_col=0)
test_plots = test_data['plot_name'].values

all_data = pd.read_csv('data/final_scores.csv')
all_plots = all_data['plot_name'].values

train_plots = np.setdiff1d(all_plots, test_plots)

scores = pd.read_csv('data/scores_elo.csv', index_col=0)

kf = KFold(n_splits=nr_folds, shuffle=True, random_state=0)
fold = 0
for train_id, val_id in kf.split(train_plots):
    fold += 1
    train = train_plots[train_id]
    val = train_plots[val_id]

    train_scores = scores[scores['plot_name'].isin(train)]
    val_scores = scores[scores['plot_name'].isin(val)]

    train_scores.to_csv(f'data/csv_splits/split{fold}_train.csv', index=False)
    val_scores.to_csv(f'data/csv_splits/split{fold}_val.csv', index=False)

test_scores = scores[scores['plot_name'].isin(test_plots)]
test_scores.to_csv(f'data/csv_splits/test.csv', index=False)

