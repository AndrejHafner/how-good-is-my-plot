import os
import cv2
import numpy as np

from pathlib import Path
from tqdm import tqdm


def generate_homogeneous_comparisons(plot_types, dir, type_samples = 20):
    plot_type_samples = []
    for plot_type in plot_types.keys():
        for _ in range(type_samples):
            sample = [os.path.join(dir, plot_type, sample) for sample in np.random.choice(plot_types[plot_type], 2)]
            plot_type_samples.append(sample)

    return plot_type_samples

def generate_heterogeneous_comparisons(plot_types, dir, k_samples = 10000):
    samples = []
    for _ in range(k_samples):
        plot_types_sampled = np.random.choice(list(plot_types.keys()), 2, replace=True)
        samples.append([os.path.join(dir, plot_type, np.random.choice(plot_types[plot_type], 1)[0]) for plot_type in plot_types_sampled])

    return samples


def image_resize_window_fit(image, size, inter = cv2.INTER_AREA):
    (h, w) = image.shape[:2]
    window = np.ones((*size, 3), dtype="uint8") * 255

    if w > h: # Reduce width to the window size and h accordingly
        new_width = size[0]
        new_height = round(h * (new_width / w))
        image_resized = cv2.resize(image, (new_width, new_height), interpolation = inter)
        height_idx = round((size[1] - new_height) / 2)
        window[height_idx:height_idx+new_height, :] = image_resized

    else: # Opposite
        new_height = size[1]
        new_width = round(w * (new_height / h))
        image_resized = cv2.resize(image, (new_width, new_height), interpolation = inter)
        width_idx = round((size[0] - new_width) / 2)
        window[:, width_idx:width_idx + new_width] = image_resized

    return window


def create_comparison_images(path1, path2, windows_shape=(1000, 500)):
    img1 = cv2.imread(path1)
    img2 = cv2.imread(path2)
    single_plot_size = (round(windows_shape[0] / 2), windows_shape[1])

    img1_placed = image_resize_window_fit(img1, single_plot_size)
    img2_placed = image_resize_window_fit(img2, single_plot_size)

    separator = np.zeros(shape=(windows_shape[1], 5, 3), dtype="uint8")
    return np.hstack([img1_placed, separator, img2_placed])



if __name__ == '__main__':
    np.random.seed(31)
    dir = "../data/plots/"
    homo_dir = "../data/homogeneous_comp"
    hetero_dir = "../data/heterogeneous_comp"

    Path(homo_dir).mkdir(exist_ok=True, parents=True)
    Path(hetero_dir).mkdir(exist_ok=True, parents=True)

    plot_types = { plot_type: list(filter(lambda x: ".jpeg" in x, os.listdir(os.path.join(dir, plot_type)))) for plot_type in os.listdir(dir) }

    homogeneous_comp = generate_homogeneous_comparisons(plot_types, dir, type_samples=30)
    heterogeneous_comp = generate_heterogeneous_comparisons(plot_types, dir, k_samples=1000)

    print("Creating homogeneous comparisons...")
    for idx, pair in tqdm(enumerate(homogeneous_comp)):
        comparison_img = create_comparison_images(*pair)
        cv2.imwrite(os.path.join(homo_dir, f"{idx}.jpeg"), comparison_img)

    print("Creating heterogeneous comparisons...")
    for idx, pair in tqdm(enumerate(heterogeneous_comp)):
        comparison_img = create_comparison_images(*pair)
        cv2.imwrite(os.path.join(hetero_dir, f"{idx}.jpeg"), comparison_img)



