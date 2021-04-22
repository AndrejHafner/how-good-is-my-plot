import os

import torch
from torchvision import datasets, models, transforms
from torch.nn.functional import softmax
import numpy as np
import cv2
from torchvision.datasets.folder import default_loader

from pathlib import Path
import shutil


def load_model(model_name, saved_model, num_classes):

    model = None
    input_size = 0

    if model_name == "resnet101":
        model = models.resnet101(num_classes=num_classes)
        input_size = 224
        model.load_state_dict(torch.load(saved_model))

    elif model_name == "resnet34":
        model = models.resnet34(num_classes=num_classes)
        input_size = 224
        model.load_state_dict(torch.load(saved_model))

    else:
        print("Invalid model name, exiting...")
        exit()

    return model, input_size


def scrapped_image_generator(dir, nr_of_images=None):
    list_dir = os.listdir(dir)

    # resizing images and normalizing them with ImageNet parameters
    transform = transforms.Compose([
        transforms.Resize((input_size, input_size)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    if nr_of_images is not None:
        list_dir = list_dir[:nr_of_images*2]
    for filename in list_dir:
        if ".jpeg" not in filename:
            continue
        img = default_loader(os.path.join(dir, filename))
        yield torch.unsqueeze(transform(img), 0), filename


def show_image(image, probabilities, predicted_ids, class_dict):
    img_show = image[0].numpy()
    img_show = np.moveaxis(img_show, 0, -1)
    img_show = cv2.cvtColor(img_show, cv2.COLOR_RGB2BGR)

    p1 = str(round(probabilities[predicted_ids[0]], 3))
    p2 = str(round(probabilities[predicted_ids[1]], 3))
    c1 = class_dict[predicted_ids[0]]
    c2 = class_dict[predicted_ids[1]]
    cv2.putText(img_show, f"{c1}: {p1}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(img_show, f"{c2}: {p2}", (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    # cv2.putText(img_show, f"{class_dict[predicted_ids[2]]}: {round(probabilities[predicted_ids[2]], 3)}",
    #             (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)

    cv2.imshow("image", img_show)
    cv2.waitKey()


if __name__ == '__main__':

    show_image_with_predictions = False
    copy_images = True

    model_name = "resnet101"
    saved_model = "cnn_weights/resnet101_phase2.pth"

    images_path = "D:/project/extracted_images/fri_master_thesis"
    nr_of_images = None

    filtered_images_path = "D:/project/filtered_master"

    num_classes = 8
    class_dict = {0: 'bar_plot', 1: 'box_plot', 2: 'histogram', 3: 'line_plot', 4: 'not_plot', 5: 'pie_chart',
                  6: 'scatter_plot', 7: 'violin_plot'}
    a = torch.cuda.is_available()
    model, input_size = load_model(model_name, saved_model, num_classes)

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model.to(device)
    model.eval()

    data = scrapped_image_generator(images_path, nr_of_images)

    for c in class_dict.values():
        if c != 'not_plot':
            Path(os.path.join(filtered_images_path, "sure", c)).mkdir(parents=True, exist_ok=True)
        Path(os.path.join(filtered_images_path, "almost_sure", c)).mkdir(parents=True, exist_ok=True)
        Path(os.path.join(filtered_images_path, "not_sure/not_plot")).mkdir(parents=True, exist_ok=True)

    # dict of filenames sorted in categories depending on their highest probabilities --> maybe try later
    # filtering_data = {'sure': [], 'almost_sure': [], 'not_sure': [], 'dont_know': []}

    for image, filename in data:
        img = image.to(device)

        prediction = model(img).cpu()
        probabilities = softmax(prediction, dim=1).detach().numpy()[0]
        predicted_ids = np.argsort(probabilities)[::-1]

        # show images together with their probabilities
        if show_image_with_predictions:
            show_image(image, probabilities, predicted_ids, class_dict)

        file_path = os.path.join(images_path, filename)

        predicted_class = class_dict[predicted_ids[0]]
        prob = probabilities[predicted_ids[0]]

        if copy_images:
            if prob > 0.99:
                if predicted_class != 'not_plot':
                    shutil.copy(file_path, os.path.join(filtered_images_path, "sure", predicted_class,
                                                        f"{round(prob*100)}_fribt_" + filename))

            elif prob > 0.9:
                shutil.copy(file_path, os.path.join(filtered_images_path, "almost_sure", predicted_class,
                                                    f"{round(prob*100)}_fribt_" + filename))

            else:
                if predicted_class == 'not_plot':
                    shutil.copy(file_path, os.path.join(filtered_images_path, "not_sure/not_plot",
                                                        f"{class_dict[predicted_ids[1]]}_not_{round(prob*100)}_fribt_" + filename))
                else:
                    shutil.copy(file_path, os.path.join(filtered_images_path, "not_sure",
                                                        f"{predicted_class}_{round(prob*100)}_fribt_" + filename))

