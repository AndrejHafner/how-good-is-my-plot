from google_images_search import GoogleImagesSearch
from env import *
from pathlib import Path
from utils import remove_corrupted_images, remove_file_type, save_json_metadata


def google_image_download(query, download_folder):
    gis = GoogleImagesSearch(GOOGLE_API_KEY, PROJECT_CX)

    # define search params:
    _search_params = {
        'q': query,
        'num': 200,
        # 'safe': 'high|medium|off',
        'fileType': 'jpg|gif|png',
        # 'imgType': 'clipart|face|lineart|news|photo',
        # 'imgSize': 'huge|icon|large|medium|small|xlarge|xxlarge',
        # 'imgDominantColor': 'black|blue|brown|gray|green|pink|purple|teal|white|yellow',
        # 'rights': 'cc_publicdomain|cc_attribute|cc_sharealike|cc_noncommercial|cc_nonderived'
    }

    Path(download_folder).mkdir(parents=True, exist_ok=True)

    gis.search(search_params=_search_params)
    for image in gis.results():
        try:
            image.download(download_folder)
        except:
            print("Error while downloading: ", image.url)
            continue
        path_split = image.path.split("\\")
        image_name = remove_file_type(path_split[len(path_split) - 1])
        save_json_metadata(download_folder, image_name, {"url": image.url, "name": image_name})


if __name__ == '__main__':
    download_folder = "./downloaded/scatter_plot"
    query = "scatter plot, scatter chart, scatterplot, scatter diagram"
    google_image_download(query, download_folder)
    remove_corrupted_images(download_folder)