import json
import os
import cv2

from PIL import Image

# Script containing utility functions

def remove_corrupted_images(directory):
    """
    A function that tries to open images in a repository, if an error occurs we remove them (corrupted image files)
    :param directory:  Target directory
    :return:
    """
    files = [file for file in os.listdir(directory) if ".json" not in file]
    for file in files:
        file_path = os.path.join(directory, file)
        try:
            Image.open(file_path)
        except:
            print(f"Failed for file {file}. Removing...")
            os.remove(file_path)


def remove_file_type(filename, file_endings=None):
    """
    Removes the file endings from the file
    :param filename: String containing the filename
    :return: Filename stripped of the file_endings
    """

    if file_endings is None:
        file_endings = [".jpg", ".png", ".gif"]
    for f_ending in file_endings:
        filename = filename.replace(f_ending, "")

    return filename


def save_json_metadata(dir, filename, obj):
    """
    Save the object in JSON format to the given directory with the given filename
    :param dir: Target directory
    :param filename: Filename to store the JSON file to
    :param obj: Data object
    :return:
    """
    with open(f"{os.path.join(dir, filename)}.json", "w") as f:
        json.dump(obj, f)


def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    """
    Resize the image to the target width or height, respecting the original aspect ratio
    :param image: Image to resize
    :param width: Target width
    :param height: Target height
    :param inter: Interplation technique
    :return: Resized image
    """

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