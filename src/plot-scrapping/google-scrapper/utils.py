import json
import os
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