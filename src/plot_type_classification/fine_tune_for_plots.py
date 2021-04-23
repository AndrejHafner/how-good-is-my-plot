from __future__ import print_function
from __future__ import division

import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, models, transforms
import time
import os
import copy


def train_model(model, dataloader, criterion, optimizer, device, num_epochs=50):
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

                    _, preds = torch.max(outputs, 1)

                    # backward + optimize only if in training phase
                    if phase == 'train':
                        loss.backward()
                        optimizer.step()

                # statistics
                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels.data)

            epoch_loss = running_loss / len(dataloader[phase].dataset)
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
    return model


def initialize_model(num_classes, use_pretrained=True):
    """
    Initializes ResNet101 network and changes the number of neurons in the last layer to correspond with the number of
    classes we want it to classify in.
    :param num_classes: number of classes
    :param use_pretrained: if True, the initialized model uses weights pretrained on ImageNet dataset
    :return: model
    """
    model_ft = models.resnet101(pretrained=use_pretrained)
    num_ftrs = model_ft.fc.in_features
    model_ft.fc = nn.Linear(num_ftrs, num_classes)

    return model_ft


# FOR GOOGLE COLAB
# from drive.MyDrive.how_good_is_my_plot.fine_tune_for_plots import train_model, initialize_model
#
# # Data directory on which you want to train the model
# data_dir = "drive/MyDrive/how_good_is_my_plot/data"


if __name__ == '__main__':

    # Data directory on which you want to train the model
    data_dir = "./data/proba"

    # Number of classes in the dataset
    num_classes = 8

    # Batch size for training (change depending on how much memory you have)
    batch_size = 48

    # Number of epochs to train for  -> can leave this on 50 - the model with best validation accuracy will be saved.
    num_epochs = 50

    # Initialize the model for this run
    input_size = 224
    model_ft = initialize_model(num_classes, use_pretrained=True)

    # Resizing and normalizing data
    data_transforms = {
        'train': transforms.Compose([
            transforms.Resize((input_size, input_size)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
        'val': transforms.Compose([
            transforms.Resize((input_size, input_size)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
    }

    print("Initializing Datasets and Dataloaders...")

    # Create training and validation datasets
    image_datasets = {x: datasets.ImageFolder(os.path.join(data_dir, x), data_transforms[x]) for x in ['train', 'val']}

    # Create training and validation dataloaders
    dataloaders_dict = {
        x: torch.utils.data.DataLoader(image_datasets[x], batch_size=batch_size, shuffle=True, num_workers=3) for x in
        ['train', 'val']}

    # Detect if we have a GPU available
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    # Send the model to GPU
    model_ft = model_ft.to(device)

    params_to_update = model_ft.parameters()

    # you can change learning rate here
    learning_rate = 0.0001
    optimizer_ft = optim.Adam(params_to_update, lr=learning_rate)

    # Setup the loss fxn
    criterion = nn.CrossEntropyLoss()

    # Train and evaluate
    model_ft = train_model(model_ft, dataloaders_dict, criterion, optimizer_ft, device, num_epochs=num_epochs)

    torch.save(model_ft.state_dict(), f"cnn_weights/resnet101_ft.pth")

