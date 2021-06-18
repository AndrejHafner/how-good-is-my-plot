import numpy as np
import pandas as pd
import math
from sklearn import linear_model, tree
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.svm import SVR
from sklearn.decomposition import PCA
from sklearn.metrics import mean_squared_error as mse
from sklearn.base import BaseEstimator
from sklearn.neighbors import KNeighborsRegressor

class Model(BaseEstimator):
    '''
    Model that first do PCA on the data before it fits's data on the model
    '''

    def __init__(self, model = None, pca_components = 1, model_params = {} ):
        '''
        :param model: model to fit, predict
        :param pca_components: param for PCA
        :param model_params: parameters for the model
        '''
        self.model = model
        self.pca_components = pca_components
        self.model_params = model_params

    def fit(self, X, y):
        '''
        First transform the data with PCA and then fits the model
        '''
        self.model_final = self.model.set_params(**self.model_params)
        self.pca = PCA(n_components=self.pca_components)
        X_small = self.pca.fit_transform(X)
        self.model_final.fit(X_small, y)

    def predict(self, X):
        '''
        Trandform the data with PCA and predicts
        '''
        X_small = self.pca.transform(X)
        prediction = self.model_final.predict(X_small)
        return prediction



def CV(model, parameters, X_train, y_train, X_test, y_test):
    '''
    Performs GridSearchCV for determing the best parameters for the model. It prints the final error on the test set.
    :param model: model to fit
    :param parameters: parameters for the model
    :param X_train: data attributes to fit the model
    :param y_train: labels for X_train
    :param X_test: data attributes to test the model
    :param y_test: labels for X_test
    '''

    clf = GridSearchCV(estimator = model(), param_grid= parameters, scoring= 'neg_mean_squared_error')
    clf.fit(X_train,y_train)

    print(clf.best_params_)
    m = model(**clf.best_params_)
    m.fit(X_train, y_train)

    p = m.predict(X_test)

    y_val = y_test.values
    SE = np.subtract(p, y_val)**2
    print(np.mean(SE))
    print(np.std(SE)/math.sqrt(len(y_test)))
    print(mse(p, y_val))
    print(mse(np.repeat(np.mean(y_train.values), len(y_test)), y_val))
    print('--------')





if __name__ == '__main__':
    # path to where the files are
    files = ['data/scores_with_embeddings.csv', 'data/scores_with_embeddings_ft.csv']
    for f in files:
        print('------')
        print(f'Now starting: {f}')
        data = pd.read_csv(f, index_col=0)

        train, test = train_test_split(data, test_size=0.2, shuffle=True, random_state=1)

        X_train, y_train = train[[f'x{i}' for i in range(2048)]], train['elo']
        X_test, y_test = test[[f'x{i}' for i in range(2048)]], test['elo']

        print('SVR with rbf kernel')
        model_params = []
        for i in range(5):
            model_params.append({'kernel': 'rbf', 'gamma': i / 10})
        param = {'model': [SVR()], 'pca_components': [1, 0.9, 0.8, 0.7, 0.6, 0.5], 'model_params': model_params}
        CV(Model, param, X_train, y_train, X_test, y_test)

        print('SVR with poly kernel')
        model_params = []
        for i in range(5):
            model_params.append({'kernel': 'poly', 'degree': i})
        param = {'model': [SVR()], 'pca_components': [1, 0.3, 0.9, 0.8, 0.7, 0.6, 0.5], 'model_params': model_params}
        CV(Model, param, X_train, y_train, X_test, y_test)

        print('Linear regression')
        param = {'model': [linear_model.LinearRegression()], 'pca_components': [1, 0.3, 0.9, 0.8, 0.7, 0.6, 0.5],
                 'model_params': [{}]}
        CV(Model, param, X_train, y_train, X_test, y_test)

        print('Bayesian Ridge')
        param = {'model': [linear_model.BayesianRidge()], 'pca_components': [1, 0.3, 0.9, 0.8, 0.7, 0.6, 0.5],
                 'model_params': [{}]}
        CV(Model, param, X_train, y_train, X_test, y_test)

        print('KNN')
        model_params = []
        for i in range(1,11):
            model_params.append({'n_neighbors': i})
        param = {'model': [KNeighborsRegressor()], 'pca_components': [1, 0.3, 0.9, 0.8, 0.7, 0.6, 0.5],
                 'model_params': model_params}
        CV(Model, param, X_train, y_train, X_test, y_test)

        print('Tree')
        model_params = []
        for i in range(2,11):
            model_params.append({'min_samples_split': i})
        param = {'model': [tree.DecisionTreeRegressor()], 'pca_components': [1, 0.3, 0.9, 0.8, 0.7, 0.6, 0.5],
                 'model_params': model_params}
        CV(Model, param, X_train, y_train, X_test, y_test)


