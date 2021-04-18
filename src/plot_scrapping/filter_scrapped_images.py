import os
import cv2
import shutil

from pathlib import Path
from utils import image_resize

def perform_action(key, file, dir, deleted_dir):
    if key == 13:  # enter - continue
        return True
    elif key == 113:  # q - delete
        os.remove(os.path.join(dir, file))
        metadata_file = file.replace(".jpeg", ".json").replace(".jpg", ".json")
        shutil.move(os.path.join(dir, metadata_file), os.path.join(deleted_dir, metadata_file))

        print(f"Deleted file: {file}")
        return True
    elif key == 27:  # esc - quit
        exit(-1)
    else:
        return False


if __name__ == '__main__':
    # !IMPORTANT! Rename these two directories before cleaning!
    dir = "D:/project/plots_google/violin_plot"
    deleted_dir = "D:/project/plots_google/deleted/violin_plot"

    Path(deleted_dir).mkdir(parents=True, exist_ok=True)

    files = [file for file in os.listdir(dir) if ".jpg" in file]
    for idx, file in enumerate(files):
        img = cv2.imread(os.path.join(dir, file))
        img_resized = image_resize(img, height=900)
        cv2.putText(img_resized, "q - delete image", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)
        cv2.putText(img_resized, "enter - continue", (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)
        cv2.putText(img_resized, "esc - quit", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)
        cv2.putText(img_resized, f"Progress: {idx+1}/{len(files)}", (10, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)
        cv2.imshow("scrapped", img_resized)

        while True:
            key = cv2.waitKey(0)
            if perform_action(key, file, dir, deleted_dir):
                break
