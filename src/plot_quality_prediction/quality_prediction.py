import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split, KFold
from sklearn.svm import SVR
from sklearn.decomposition import PCA
from sklearn.metrics import mean_squared_error as mse

data = pd.read_csv('data/scores_with_embeddings.csv', index_col=0)

train, test = train_test_split(data, test_size=0.2, shuffle=True, random_state=1)

X_train, y_train = train[[f'x{i}' for i in range(2048)]], train['elo']
X_test, y_test = test[[f'x{i}' for i in range(2048)]], test['elo']

# fitting
pca = PCA(n_components=0.9)
X_small = pca.fit_transform(X_train)

svr = SVR(kernel='rbf')
svr.fit(X_small, y_train)

# predicting
X_test_small = pca.transform(X_test)
prediction = svr.predict(X_test_small)

# evaluation
y_val = y_test.values
print(mse(prediction, y_val))
print(mse(np.repeat(0, len(y_test)), y_val))