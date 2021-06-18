import os
import cv2
import shutil

from pathlib import Path
from utils import image_resize

# A script/tool used for filtering the scrapped images (removing them from the set if inappropriate)

def perform_action(key, file, dir, wrong_dir, not_plot_dir, cut_dir, plot3d_dir, not_sure_dir):
    """
    Perform a certain action based on a keypress
    :param key: Number of the keyboard key pressed
    :param file: Filename to remove/move (if the appropriate key is pressed)
    :param dir: Directory with existing files
    :param wrong_dir: Directory where the wrong classified plots are moved to
    :param not_plot_dir: Directory where the files that are not plots are moved to
    :param cut_dir: Directory where the plots, that are cut, are moved to
    :param plot3d_dir: Directory where the 3D plots are moved to
    :param not_sure_dir: Directory where the plots, that you are unsure what they are, are moved to
    :return: A boolean whether an action key was pressed
    """
    if key == 13:  # enter - continue
        return True
    elif key == 113:  # q - delete
        os.remove(os.path.join(dir, file))
        #metadata_file = file.replace(".jpeg", ".json").replace(".jpg", ".json")
        #shutil.move(os.path.join(dir, metadata_file), os.path.join(deleted_dir, metadata_file))
        print(f"Deleted file: {file}")
        return True
    elif key == 97: #a - move to a wrongly classified folder
        print(f"Wrong class")
        shutil.move(os.path.join(dir, file), os.path.join(wrong_dir, file))
        return True
    elif key == 115: #s - move to a not plot folder
        print(f"Not plot")
        shutil.move(os.path.join(dir, file), os.path.join(not_plot_dir, file))
        return True
    elif key == 100: #d - move to a cut plot folder
        print(f"Cut plot")
        shutil.move(os.path.join(dir, file), os.path.join(cut_dir, file))
        return True
    elif key == 102: #f - move to a 3d plots folder
        print(f"3D plot")
        shutil.move(os.path.join(dir, file), os.path.join(plot3d_dir, file))
        return True
    elif key == 103: #g - move to a not_sure folder
        print(f"Not sure")
        shutil.move(os.path.join(dir, file), os.path.join(not_sure_dir, file))
        return True
    elif key == 27:  # esc - quit
        exit(-1)
    else:
        return False


if __name__ == '__main__':


    # !IMPORTANT! Rename these two directories before cleaning!
    plot_type = 'line_plot'
    dir = f"C:/Users/Acer/Desktop/Data science/1 letnik/Project/data/filtered_images/{plot_type}/sampled"
    #deleted_dir = "C:/Users/Acer/Desktop/Data science/1 letnik/Project/filtered_images/moved"
    wrong_dir = f"C:/Users/Acer/Desktop/Data science/1 letnik/Project/data/filtered_images/{plot_type}/wrong_plot"
    not_plot_dir = f"C:/Users/Acer/Desktop/Data science/1 letnik/Project/data/filtered_images/{plot_type}/not_plot"
    cut_dir = f"C:/Users/Acer/Desktop/Data science/1 letnik/Project/data/filtered_images/{plot_type}/cut_plot"
    plot3d_dir = f"C:/Users/Acer/Desktop/Data science/1 letnik/Project/data/filtered_images/{plot_type}/plot_3d"
    not_sure_dir = f"C:/Users/Acer/Desktop/Data science/1 letnik/Project/data/filtered_images/{plot_type}/not_sure"

    #Path(deleted_dir).mkdir(parents=True, exist_ok=True)
    Path(wrong_dir).mkdir(parents=True, exist_ok=True)
    Path(not_plot_dir).mkdir(parents=True, exist_ok=True)
    Path(cut_dir).mkdir(parents=True, exist_ok=True)
    Path(plot3d_dir).mkdir(parents=True, exist_ok=True)
    Path(not_sure_dir).mkdir(parents=True, exist_ok=True)

    # Iterate over the files and filter them
    files = [file for file in os.listdir(dir) if ".jpeg" in file]
    print(len(files))
    for idx, file in enumerate(files):
        img = cv2.imread(os.path.join(dir, file))
        img_resized = image_resize(img, height=500)
        cv2.putText(img_resized, "q - delete image", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)
        cv2.putText(img_resized, "enter - continue", (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)
        cv2.putText(img_resized, "wrong class - a", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)
        cv2.putText(img_resized, "not plot - s", (10, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)
        cv2.putText(img_resized, "cut plot - d", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)
        cv2.putText(img_resized, "3d plot - f", (10, 95), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)
        cv2.putText(img_resized, "not sure - g", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)
        cv2.putText(img_resized, "esc - quit", (10, 125), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)
        cv2.putText(img_resized, f"Progress: {idx+1}/{len(files)}", (10, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)
        cv2.imshow("scrapped", img_resized)

        while True:
            key = cv2.waitKey(0)
            if perform_action(key, file, dir, wrong_dir, not_plot_dir, cut_dir, plot3d_dir, not_sure_dir):
                break

    #uncomment this if you would like to get the key value number
    '''
    img = cv2.imread('C:/Users/Acer/Desktop/Data science/1 letnik/Project/filtered_images/bar_plot/99_efb_42.jpeg')  # load a dummy image
    while (1):
        cv2.imshow('img', img)
        k = cv2.waitKey(33)
        if k == 27:  # Esc key to stop
            break
        elif k == -1:  # normally -1 returned,so don't print it
            continue
        else:
            print(f'Your key number: {k}')  # else print its value
    '''