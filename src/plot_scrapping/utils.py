import json
import os
import cv2

from PIL import Image


def remove_corrupted_images(directory):
    files = [file for file in os.listdir(directory) if ".json" not in file]
    for file in files:
        file_path = os.path.join(directory, file)
        try:
            Image.open(file_path)
        except:
            print(f"Failed for file {file}. Removing...")
            os.remove(file_path)


def remove_file_type(filename):
    file_endings = [".jpg", ".png", ".gif"]
    for f_ending in file_endings:
        filename = filename.replace(f_ending, "")

    return filename


def save_json_metadata(dir, filename, obj):
    with open(f"{os.path.join(dir, filename)}.json", "w") as f:
        json.dump(obj, f)


def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized