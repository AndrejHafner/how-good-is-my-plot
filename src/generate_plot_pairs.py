import networkx as nx
import pandas as pd

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

def write_csv(list_names, k):
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

    df.to_csv('test.csv', index=False)


if __name__ == '__main__':
    write_csv([f'slika_{i}.jpg' for i in range(10)], 4)

