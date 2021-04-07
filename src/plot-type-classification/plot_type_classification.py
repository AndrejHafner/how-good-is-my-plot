import torch
import numpy as np
import joblib
from torch.utils.data import DataLoader

from torchvision import models, transforms, datasets
from torchvision.models.resnet import Bottleneck


class ResNet101Extract(models.ResNet):

    def __init__(self, path_to_weights):  #, num_classes=1500):
        super().__init__(Bottleneck, [3, 4, 23, 3])
        self.load_state_dict(torch.load(path_to_weights))
        # num_ftrs = self.fc.in_features
        # self.fc = nn.Linear(num_ftrs, num_classes)

    def feature_extract_avg_pool(self, x):
        # See note [TorchScript super()]
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.maxpool(x)

        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)

        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        return x


def make_embeddings(path):
    model = ResNet101Extract('cnn_weights/resnet101-5d3b4d8f.pth')
    input_size = 224

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model.to(device)
    model.eval()

    transform = transforms.Compose([
        transforms.Resize((input_size, input_size)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    dataset = datasets.ImageFolder(path, transform)
    test_data = DataLoader(dataset, batch_size=20, num_workers=3)

    embeddings = {i: [] for i in range(7)}

    for photos, ids in test_data:
        print(ids)
        photos = photos.to(device)
        emb = model.feature_extract_avg_pool(photos).cpu().detach().numpy()
        ids_n = ids.detach().numpy()
        for i in range(len(ids_n)):
            embeddings[ids_n[i]].append(emb[i])

    joblib.dump(embeddings, f"embeddings.joblib")





if __name__ == '__main__':

    make_embeddings('./data')
