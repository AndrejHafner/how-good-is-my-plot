import numpy as np
import pandas as pd
from scipy.optimize import minimize
import matplotlib.pyplot as plt


def tgt_fn(x, matches):
    xr = np.hstack([0, x])
    prob = (1 / (1 + np.exp(xr[matches[:, 0]] - xr[matches[:, 1]])))
    loss = matches[:, 2] * np.log(prob) + (1 - matches[:, 2]) * np.log(1 - prob)
    return -np.sum(loss)


def tgt_grad(x, matches):
    xr = np.hstack([0, x])
    prob = (1 / (1 + np.exp(xr[matches[:, 0]] - xr[matches[:, 1]])))
    dt = prob - matches[:, 2]
    grad_x = np.zeros(len(x))
    for i in range(len(x)):
        grad_x[i] = - np.sum(dt[np.where(matches[:, 1] == i + 1)]) + np.sum(dt[np.where(matches[:, 0] == i + 1)])
    return - grad_x


if __name__ == '__main__':

    # TOY DATASET
    n = 10  # number of objects
    m = 1000  # number of games
    z = np.random.uniform(-1, 1, n)  # latent strengths of objects
    games = np.zeros([m, 3], dtype=int)

    for i in range(m):
        id1 = np.random.randint(0, 10)
        id2 = np.random.randint(0, 10)
        while id1 == id2:
            id2 = np.random.randint(0, 9)
        win = np.random.uniform(0, 1) < 1 / (1 + np.exp(z[id1] - z[id2]))
        games[i, :] = id1, id2, win

    x0 = np.zeros(n - 1)

    res = minimize(tgt_fn, x0, games, method='L-BFGS-B', jac=tgt_grad)

    # testing for toy data
    plt.plot(z, np.hstack([0, res['x']]), '.')
    plt.show()

    for i in range(10):
        print(z[i], np.mean(
            np.hstack([1 - games[np.where(games[:, 0] == i), 2][0], games[np.where(games[:, 1] == i), 2][0]])))

    # PLOT RATINGS
    scores = pd.read_csv('data/final_scores.csv')
    all_matches = pd.read_csv('data/all_matches.csv')

    names_to_idx = dict(zip(scores['plot_name'].values, scores.index.values))
    all_matches['id1'] = all_matches['name1'].map(names_to_idx)
    all_matches['id2'] = all_matches['name2'].map(names_to_idx)

    matches = all_matches[['id1', 'id2', 'win']].values

    x0 = np.zeros(scores.shape[0] - 1)

    res = minimize(tgt_fn, x0, matches, method='L-BFGS-B', jac=tgt_grad)
    ratings = np.hstack([0, res['x']])

    # mean ratings for plots with same number of wins
    for i in range(10):
        print(i, np.mean(ratings[scores[scores['score'] == i].index.values]))
