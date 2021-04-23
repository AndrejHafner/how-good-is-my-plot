import os
import random
from pathlib import Path
import shutil
from tqdm import tqdm

# A script that splits the dataset into a train and validation set

if __name__ == '__main__':
    dir = "../data/plots"
    plot_dirs = os.listdir(dir)

    for plot_dir in tqdm(plot_dirs):
        file_names = [el.replace(".jpeg", "") for el in os.listdir(os.path.join(dir, plot_dir)) if ".jpeg" in el]
        random.shuffle(file_names)

        train = file_names[:round(len(file_names) * 0.8)]
        val = file_names[round(len(file_names) * 0.8):]

        Path(os.path.join("../data", "train", plot_dir)).mkdir(parents=True, exist_ok=True)
        Path(os.path.join("../data", "val", plot_dir)).mkdir(parents=True, exist_ok=True)

        for file in train:
            shutil.copy(os.path.join(dir, plot_dir, f"{file}.jpeg"), os.path.join("../data", "train", plot_dir, f"{file}.jpeg"))

        for file in val:
            shutil.copy(os.path.join(dir, plot_dir, f"{file}.jpeg"), os.path.join("../data", "val", plot_dir, f"{file}.jpeg"))
