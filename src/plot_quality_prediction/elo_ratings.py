import numpy as np
import pandas as pd
from scipy.optimize import minimize, fmin_l_bfgs_b
import matplotlib.pyplot as plt


def tgt_fn(x, matches):
    xr = np.hstack([0, x])
    prob = (1 / (1 + np.exp(-(xr[matches[:, 0]] - xr[matches[:, 1]]))))
    loss = matches[:, 2] * np.log(prob) + (1 - matches[:, 2]) * np.log(1 - prob)
    return -np.sum(loss)


if __name__ == '__main__':

    ### TOY DATASET
    n = 10  # number of objects
    m = 1000  # number of games
    z = np.random.uniform(-1, 1, n)  # latent strengths of objects
    games = np.zeros([m, 3], dtype=int)

    for i in range(m):
        id1 = np.random.randint(0, 9)
        id2 = np.random.randint(0, 9)
        while id1 == id2:
            id2 = np.random.randint(0, 9)
        win = np.random.uniform(0, 1) < 1 / (1 + np.exp(-(z[id1] - z[id2])))
        games[i, :] = id1, id2, win

    x0 = np.zeros(n - 1)

    res = minimize(tgt_fn, x0, games, method='L-BFGS-B')

    plt.plot(z, np.hstack([0, res['x']]), '.')
    plt.show()

    # plot matches
    scores = pd.read_csv('data/final_scores.csv')
    all_matches = pd.read_csv('data/all_matches.csv')

    names_to_idx = dict(zip(scores['plot_name'].values, scores.index.values))
    all_matches['id1'] = all_matches['name1'].map(names_to_idx)
    all_matches['id2'] = all_matches['name2'].map(names_to_idx)

    matches = all_matches[['id1', 'id2', 'win']].values

    x0 = np.zeros(scores.shape[0] - 1)

    print(tgt_fn(np.zeros(scores.shape[0]), matches))
    # res = minimize(tgt_fn, x0, matches, method='L-BFGS-B', options={'maxfun': 50000})
    res = minimize(tgt_fn, x0, matches, method='CG')
    # res = fmin_l_bfgs_b(tgt_fn, x0, args=[matches], approx_grad=True)
    s = 0