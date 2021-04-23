from google_images_search import GoogleImagesSearch
from env import *
from pathlib import Path
from src.plot_scrapping.utils import remove_corrupted_images, remove_file_type, save_json_metadata


def google_image_download(query, download_folder):
    """
    Download images from the Google Images using the Custom Search API
    :param query: Query string
    :param download_folder: Directory to save the images to
    :return:
    """
    gis = GoogleImagesSearch(GOOGLE_API_KEY, PROJECT_CX)

    search_params = {
        'q': query,
        'num': 100,
        'fileType': 'jpg|gif|png',
    }

    # Ensure that the download_folder exists
    Path(download_folder).mkdir(parents=True, exist_ok=True)

    # Query the API
    gis.search(search_params=search_params)

    # Iterate over the results and try to download them. Successfully downloaded images are accompanied with a JSON file containing the metadata.
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
    download_folder = "./downloaded/bar_plot"
    query = "bar plot", # bar plot, histogram
    # query = "scatter plot, scatter chart, scatter diagram"
    google_image_download(query, download_folder)
    remove_corrupted_images(download_folder)