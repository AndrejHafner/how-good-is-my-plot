import pandas as pd
import numpy as np
import os
import torch
from torch.utils.data import Dataset
from torchvision.datasets.folder import default_loader


class RegressionDataset(Dataset):
    """Dataset for regression data given to CNN."""

    def __init__(self, plot_dir, csv_file, transform=None):
        """
        Args:
            csv_file (string): Path to the csv file with elo scores.
            plot_dir (string): Directory with all the images.
            transform (callable, optional): Optional transform to be applied
                on a sample.
        """
        self.elo_scores = pd.read_csv(csv_file)
        self.plot_dir = plot_dir
        self.transform = transform

    def __len__(self):
        return self.elo_scores.shape[0]

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        img_name = self.elo_scores.loc[idx, 'plot_name']

        image = default_loader(os.path.join(self.plot_dir, img_name))
        if self.transform:
            image = self.transform(image)

        target = self.elo_scores.loc[idx, 'elo']

        # return torch.unsqueeze(image, 0), target
        return image, np.array([target], dtype=np.float32)