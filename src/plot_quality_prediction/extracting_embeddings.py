import torch
import numpy as np
import pandas as pd
import joblib

from torch.utils.data import DataLoader
from torchvision import models, transforms, datasets
from torchvision.models.resnet import Bottleneck
import torch.nn as nn

from src.plot_type_classification.filter_extracted_images import scrapped_image_generator

class ResNet101Extract(models.ResNet):

    def __init__(self, path_to_weights, fine_tuned=False, num_classes=8):
        super().__init__(Bottleneck, [3, 4, 23, 3])

        # if we are loading a finetuned network we need to change the number of neurons in the last layer
        if fine_tuned:
            num_ftrs = self.fc.in_features
            self.fc = nn.Linear(num_ftrs, num_classes)
        self.load_state_dict(torch.load(path_to_weights))

    def feature_extract_avg_pool(self, x):
        """
        Extracting features from the previous-to-last layer of the network - making a forward pass without last layer.
        :param x: input image that we want to extract features from
        :return: output of the previous-to-last, an average pool layer
        """
        # forward pass through the network
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.maxpool(x)

        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)

        x = self.avgpool(x)

        # finish at the average pool layer and flatten the result
        x = torch.flatten(x, 1)
        return x


def make_embeddings(path, fine_tuned=False):
    """
    Make embeddings for all images from folder given with path.
    :param path: path to folder of images we want to make embeddings of
    """

    if fine_tuned:
        model = ResNet101Extract('../plot_type_classification/cnn_weights/resnet101_phase3.pth', True, 8)
    else:
        model = ResNet101Extract('../plot_type_classification/cnn_weights/resnet101-5d3b4d8f.pth')

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model.to(device)
    model.eval()

    data = scrapped_image_generator(path)

    embeddings = {}

    # calculating the embedding and saving it to dict
    for photo, name in data:
        photo = photo.to(device)
        emb = model.feature_extract_avg_pool(photo).cpu().detach().numpy()
        embeddings[name] = emb[0]

    scores = pd.read_csv('data/final_scores.csv')

    for name, emb in zip(embeddings.keys(), embeddings.values()):
        scores.loc[scores['plot_name'] == name, [f'x{i}' for i in range(2048)]] = emb

    if fine_tuned:
        scores.to_csv('data/scores_with_embeddings_ft.csv')
    else:
        scores.to_csv('data/scores_with_embeddings.csv')


# def embeddings_to_dataframe(embeddings_file):
#     """
#     Reading the embeddings file and saving it to dataframe
#     :param embeddings_file: json file in which the embeddings are saved
#     :return: dataframe of embeddings
#     """
#     embeddings = joblib.load(embeddings_file)
#     col = ['class', 'cons_nr'] + [f'x{i}' for i in range(2048)]
#     df = pd.DataFrame(columns=col)
#
#     for c in embeddings.keys():
#         n = len(embeddings[c])
#         embeddings_matrix = np.stack(embeddings[c], axis=0)
#         classes = np.stack([np.repeat(c, n), 2 * np.arange(n) + 1]).T
#         combined = np.concatenate([classes, embeddings_matrix], axis=1)
#         df_add = pd.DataFrame(combined, columns=col)
#
#         df = df.append(df_add)
#
#     return df


if __name__ == '__main__':

    make_embeddings('D:/project/final')

    make_embeddings('D:/project/final', True)


