import os
import cv2
import itertools
import numpy as np


def remove_duplicates(folder):
    images = {os.path.join(folder, filename): cv2.imread(os.path.join(folder, filename), cv2.IMREAD_GRAYSCALE) for filename
              in os.listdir(folder) if not os.path.isdir(os.path.join(folder, filename))}

    all_groups = [list(grouper) for _, grouper in itertools.groupby(list(images.items()), key=lambda x: x[1].shape)]

    duplicates = set()
    for group in all_groups:
        for ((path1, img1), (path2, img2)) in itertools.combinations(group, 2):
            img_diff_sum = np.sum(np.abs(img1 - img2))
            if img_diff_sum == 0:
                duplicates.add(path2)

    if len(duplicates) == 0:
        print(f"Found 0 duplicates.")
    else:
        print(f"Found {len(duplicates)} duplicates. Removing...")

    for el in duplicates:
        os.remove(el)
        # print(el)


if __name__ == '__main__':

    start_path = "D:/project/filtered"

    for f in ['ef', 'fmf', 'fri']:
        for t in ['bachelor', 'master', 'other', 'phd']:
            for s in ['almost_sure', 'sure']:
                for c in os.listdir(os.path.join(start_path, f, t, s)):
                    path = os.path.join(start_path, f, t, s, c)
                    print(f'Currently at {path}.')
                    remove_duplicates(path)

            remove_duplicates(os.path.join(start_path, f, t, 'not_sure'))


