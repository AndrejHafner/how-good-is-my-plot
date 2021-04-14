import os
import cv2

from utils import image_resize

def perform_action(key, file, dir):
    if key == 13: # enter - continue
        return True
    elif key == 113: # q - delete
        os.remove(os.path.join(dir, file))
        os.remove(os.path.join(dir, file.replace(".jpeg", ".json")))
        print(f"Deleted file: {file}")
        return True
    elif key == 27: # esc - quit
        exit(-1)
    else:
        return False


if __name__ == '__main__':
    dir = "./duckduckgo_scrapper/downloaded/scatter_plot"
    files = [file for file in os.listdir(dir) if ".jpeg" in file]

    for file in files:
        img = cv2.imread(os.path.join(dir, file))
        img_resized = image_resize(img, height=900)
        cv2.putText(img_resized, "q - delete image", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)
        cv2.putText(img_resized, "enter - continue", (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)
        cv2.putText(img_resized, "esc - quit", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)
        cv2.imshow("scrapped", img_resized)

        while True:
            key = cv2.waitKey(0)
            if perform_action(key, file, dir):
                break
