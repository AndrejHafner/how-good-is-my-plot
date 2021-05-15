import networkx as nx
import pandas as pd
import os
import random
from shutil import copyfile

def sample_pictures(dir,n, new_dir):
    '''
    Samples n instances from dir
    :param dir: dir path
    :param n: int, sample size
    '''
    files = [f for f in os.listdir(dir)]
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

    #now we have all plots in new_dir, should we shuffle them?
    names = [f for f in os.listdir(new_dir) if f.lower().endswith(('.jpg', '.jpeg'))]
    write_csv(names, k, csv_filename)


if __name__ == '__main__':
    #Here write the dir, where folders with all plots are
    dir = 'C:/Users/Acer/Desktop/Data science/1 letnik/Project/filtered_images'

    #Here write the dir, where you want your sampled files to be copied to
    new_dir = 'C:/Users/Acer/Desktop/Data science/1 letnik/Project/filtered_images/sampled'

    #all the plot types you want to sample from
    plot_types = ['bar_plot', 'box_plot', 'histogram', 'line_plot', 'scatter_plot']

    #size of each sample
    sizes = [2,1,1,2,2]

    #how many times each plot is compared, has to be even number
    k = 4

    #filename of the csv file, where plot pairs will be written
    csv_filename = 'test_final'

    generate_plot_pairs(plot_types, sizes, k, dir, new_dir, csv_filename)
