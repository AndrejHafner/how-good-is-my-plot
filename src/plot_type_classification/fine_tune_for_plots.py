from __future__ import print_function
from __future__ import division

import torch
import torch.nn as nn
from torchvision import models
import time
import copy


def train_model(model, dataloader, criterion, optimizer, device, num_epochs=50, regression=False):
    """
    Training model on data from dataloader with given optimizer, optimizing by criterion for num_epochs epochs.
    :param model: model we are optimizing
    :param dataloader: loader of data on which we want to train the model
    :param criterion: loss function based on which we optimize the model and choose the best one
    :param optimizer: optimizer whit which we optimize our model
    :param device: device that is used for calculations
    :param num_epochs: number of epochs of training
    :return: trained model
    """
    since = time.time()

    best_model_wts = copy.deepcopy(model.state_dict())
    best_loss = 1e10

    for epoch in range(num_epochs):
        print('Epoch {}/{}'.format(epoch, num_epochs - 1))
        print('-' * 10)

        # Each epoch has a training and validation phase
        for phase in ['train', 'val']:
            if phase == 'train':
                model.train()  # Set model to training mode
            else:
                model.eval()   # Set model to evaluate mode

            running_loss = 0
            running_corrects = 0

            # Iterate over data.
            for inputs, labels in dataloader[phase]:
                inputs = inputs.to(device)
                labels = labels.to(device)

                # zero the parameter gradients
                optimizer.zero_grad()

                # forward
                # track history if only in train
                with torch.set_grad_enabled(phase == 'train'):
                    # Get model outputs and calculate loss
                    outputs = model(inputs)
                    loss = criterion(outputs, labels)

                    if not regression:
                        _, preds = torch.max(outputs, 1)

                    # backward + optimize only if in training phase
                    if phase == 'train':
                        loss.backward()
                        optimizer.step()

                # statistics
                running_loss += loss.item() * inputs.size(0)
                if not regression:
                    running_corrects += torch.sum(preds == labels.data)

            epoch_loss = running_loss / len(dataloader[phase].dataset)
            if regression:
                print('{} Loss: {:.4f}'.format(phase, epoch_loss))

            else:
                epoch_acc = running_corrects.double() / len(dataloader[phase].dataset)
                print('{} Loss: {:.4f} Acc: {:.4f}'.format(phase, epoch_loss, epoch_acc))

            # deep copy the model
            if phase == 'val' and epoch_loss < best_loss:
                best_loss = epoch_loss
                best_model_wts = copy.deepcopy(model.state_dict())

        print()

    time_elapsed = time.time() - since
    print('Training complete in {:.0f}m {:.0f}s'.format(time_elapsed // 60, time_elapsed % 60))
    print('Best val Loss: {:4f}'.format(best_loss))

    # load best model weights
    model.load_state_dict(best_model_wts)
    return model, best_loss


def initialize_model(num_classes, use_pretrained=True):
    """
    Initialization of the ResNet101 network.
    :param num_classes: number of neurons that the network should have in the last layer
    :param use_pretrained: if True, the initialized network is pretrained on ImageNet dataset
    :return: network
    """
    model_ft = models.resnet101(pretrained=use_pretrained)
    num_ftrs = model_ft.fc.in_features
    model_ft.fc = nn.Linear(num_ftrs, num_classes)

    return model_ft

