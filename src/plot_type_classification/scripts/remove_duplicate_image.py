import os
import cv2
import itertools
import numpy as np

def remove_duplicates(folder):
    images = {os.path.join(folder, filename): cv2.imread(os.path.join(folder, filename), cv2.IMREAD_GRAYSCALE) for filename
              in os.listdir(folder)}

    all_groups = [list(grouper) for _, grouper in itertools.groupby(sorted(list(images.items()), key=lambda x: x[1].shape), key=lambda x: x[1].shape)]

    duplicates = set()
    for group in all_groups:
        for ((path1, img1), (path2, img2)) in itertools.combinations(group, 2):
            img_diff_sum = np.sum(np.abs(img1 - img2))
            if img_diff_sum == 0:
                duplicates.add(path2)

    print(f"Found {len(duplicates)} duplicates. Removing...")

    for el in duplicates:
        os.remove(el)

if __name__ == '__main__':

    path = "../data/remove_dups_test"
    remove_duplicates(path)


