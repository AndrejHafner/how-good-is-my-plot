import os
from shutil import copy
import random
from pathlib import Path

def sample_pictures(dir,n, new_dir):
    '''
    Samples n instances from dir and move it to new_dir
    :param dir: dir path
    :param n: int, sample size
    :param new_dir: new_dir path
    '''
    files = [f for f in os.listdir(dir)]
    sample = random.sample(files, n)
    for file in sample:
        try:
            copy(dir + '/' + file, new_dir + '/' + file)
        except:
            print('-')


if __name__ == '__main__':
    #set seed so sampling will be reproducible
    random.seed(0)

    # all the plot types you want to sample from
    plot_types = ['bar_plot', 'line_plot']

    # size of each sample
    size = 1200

    for plot_type in plot_types:
        # Here write the dir, where folders with all plots are
        dir = f'C:/Users/Acer/Desktop/Data science/1 letnik/Project/data/filtered_images/{plot_type}'

        # Here write the dir, where you want your sampled files to be copied to
        new_dir = f'C:/Users/Acer/Desktop/Data science/1 letnik/Project/data/filtered_images/{plot_type}/sampled'

        Path(new_dir).mkdir(parents=True, exist_ok=True)

        sample_pictures(dir, size, new_dir)


