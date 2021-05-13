import os
import shutil
from pathlib import Path

if __name__ == '__main__':

    start_path = "D:/project/filtered"
    dst_path = "D:/project/filtered_all_sure"

    for c in os.listdir(os.path.join(start_path, 'ef', 'phd', 'sure')):
        Path(os.path.join(dst_path, c)).mkdir(parents=True, exist_ok=True)

    for f in ['ef', 'fmf', 'fri']:
        for t in ['bachelor', 'master', 'other', 'phd']:
            for c in os.listdir(os.path.join(start_path, f, t, 'sure')):
                if c != 'not_plot':
                    path = os.path.join(start_path, f, t, 'sure', c)
                    for image in os.listdir(path):
                        shutil.copy(os.path.join(path, image), os.path.join(dst_path, c, image))

