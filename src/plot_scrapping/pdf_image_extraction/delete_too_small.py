import os
import cv2

from pathlib import Path

# A script that deletes the images from the target directory that are below the size threshold

dir = "D:/project/extracted_images/fri_bachelor_thesis"

Path(dir).mkdir(parents=True, exist_ok=True)

files = [file for file in os.listdir(dir) if ".jpeg" in file]

for file in files:
    img = cv2.imread(os.path.join(dir, file))
    (height, width) = img.shape[:2]

    if height < 100 or width < 100 or (height < 200 and width < 200):
        os.remove(os.path.join(dir, file))
        json = file.strip('.jpeg') + '.json'
        if os.path.exists(os.path.join(dir, json)):
            os.remove(os.path.join(dir, json))


