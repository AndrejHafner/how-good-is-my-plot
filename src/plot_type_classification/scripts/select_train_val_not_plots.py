import os
import random
from pathlib import Path
import shutil

if __name__ == '__main__':
    dir = "D:/project/extracted_images/fri_bachelor_thesis"
    train_dir = "D:/project/extracted_images/fri_bachelor_thesis_train"
    val_dir = "D:/project/extracted_images/fri_bachelor_thesis_val"

    train_size = 350
    val_size = round(0.25 * train_size)

    file_names = [el.replace(".jpeg", "") for el in os.listdir(dir) if ".jpeg" in el]
    random.shuffle(file_names)

    train = file_names[:train_size]
    val = file_names[train_size:train_size+val_size]

    Path(train_dir).mkdir(parents=True, exist_ok=True)
    Path(val_dir).mkdir(parents=True, exist_ok=True)

    for file in train:
        shutil.copy(os.path.join(dir, f"{file}.jpeg"), os.path.join(train_dir, f"{file}.jpeg"))

    for file in val:
        shutil.copy(os.path.join(dir, f"{file}.jpeg"), os.path.join(val_dir, f"{file}.jpeg"))
