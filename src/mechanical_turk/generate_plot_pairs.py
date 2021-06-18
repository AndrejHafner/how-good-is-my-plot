# This code was not used at the end. Instead of this, we generated pairs with generate_pairs_based_on_scores.py


import networkx as nx
import pandas as pd
import os
import random
from shutil import copyfile
import matplotlib.pyplot as plt
import random

def sample_pictures(dir,n, new_dir):
    '''
    Samples n instances from dir
    :param dir: dir path
    :param n: int, sample size
    '''
    files = [f for f in os.listdir(dir) if f.lower().endswith(('.jpg', '.jpeg'))]
    sample = random.sample(files, n)
    for file in sample:
        copyfile(dir + '/' + file, new_dir + '/' + file)


def ring_graph(n,k):
    '''
    Creates a ring graph on n nodes with k edges
    :param n: int, number of nodes
    :param k: int, node degree, has to be an even number
    '''
    G = nx.MultiGraph()
    for i in range(n):
        G.add_node(i)
    for i in range(n):
        for j in range(1,int(k/2+1)):
            G.add_edge(i, (i+j) % n)

    return G

def rename_nodes(G,names):
    '''
    Renames graph nodes
    :param G: graph
    :param names: list of names to rename nodes
    '''
    map = {}
    for i, name in enumerate(names):
        map[i] = name
    G = nx.relabel_nodes(G,map)
    return G

def write_csv(list_names, k, csv_filename):
    '''
    Writes csv of pairs of names in list_names, each name has n pairs.
    :param list_names: list of names
    :param k: int, number of pairs for each name
    '''
    n = len(list_names)
    G = ring_graph(n,k)
    G = rename_nodes(G,list_names)
    pairs = list(G.edges)
    random.shuffle(pairs)
    df = pd.DataFrame(columns=['first','second'])
    for first,second,_ in pairs:
        df = df.append({'first':first, 'second':second}, ignore_index=True)

    df.to_csv(f'{csv_filename}.csv', index=False)

def generate_plot_pairs(plot_types, sizes, k, dir, new_dir, csv_filename):
    '''
    Samples plots from directory dir that are listed in plot_types, each with size listed in sizes.
     Sampled plots are moved to new_dir. From plots in new_dir generates pairs, where each plot is compared k-times.
     Writes csv in csv_filename.
     :param plot_types: list of plot folders
     :param sizes: list of sample sizes
     :param k: int, how many times each plot is compared
     :param dir: directory, where plot folders are
     :param new_dir: in which directory sampled plots will be copied
     :param csv_filename: name of csv file
    '''
    if not os.path.exists(new_dir):
        os.mkdir(new_dir)

    for n, plot in zip(sizes, plot_types):
        sample_pictures(dir + '/' + plot, n, new_dir)

    plot_names = os.listdir(new_dir)
    random.shuffle(plot_names)
    #now we have all plots in new_dir, should we shuffle them?
    names = [f for f in plot_names if f.lower().endswith(('.jpg', '.jpeg'))]
    write_csv(names, k, csv_filename)


if __name__ == '__main__':

    random.seed(0)
    #Here write the dir, where folders with all plots are
    dir = 'C:/Users/Acer/Desktop/Data science/1 letnik/Project/data/filtered_images'

    #Here write the dir, where you want your sampled files to be copied to
    new_dir = 'C:/Users/Acer/Desktop/Data science/1 letnik/Project/data/filtered_images/sampled_toy'

    #all the plot types you want to sample from
    plot_types = ['bar_plot/sampled', 'box_plot', 'histogram', 'line_plot/sampled', 'scatter_plot', 'pie_chart']

    #size of each sample
    sizes = [15,15,15,15,15,15]

    #how many times each plot is compared, has to be even number
    k = 6

    #filename of the csv file, where plot pairs will be written
    csv_filename = 'toy_mt'

    generate_plot_pairs(plot_types, sizes, k, dir, new_dir, csv_filename)

