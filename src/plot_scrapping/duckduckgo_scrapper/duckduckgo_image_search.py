import requests
import re
import json
import os

from pathlib import Path
from tqdm import tqdm
from io import BytesIO
from PIL import Image
from src.plot_scrapping.utils import save_json_metadata


class DuckduckgoImageSearch:
    """
    A class that contains the utilites for searching on the DuckDuckGo image search and downloading the images in the results
    """

    def __init__(self):
        self.url = 'https://duckduckgo.com/'
        self.search_results = []

    def search(self, keywords, max_results=100):
        """
        Perform a search query
        :param keywords: Query string used in search
        :param max_results: Maximum number of results to return
        :return:
        """

        # Acquire the token
        vqd_token = self.fetch_token(keywords)

        params = self.get_params(keywords, vqd_token)
        headers = self.get_headers()

        request_url = self.url + "i.js"
        self.search_results = []

        # Fetch the results and query the next page until we accumulate max_results of hits
        try:
            while len(self.search_results) < max_results:
                res = requests.get(request_url, headers=headers, params=params)
                data = json.loads(res.text)
                self.search_results += data["results"]

                if "next" not in data:
                    print(f"No further results found. Collected {len(self.search_results)} search results.")
                    break

                request_url = self.url + data["next"]

        except:
            print("Error while fetching image search results.")

        print(f"Collected {len(self.search_results)} search results.")

    def download_images_gen(self):
        """
        Returns a generator object that yields the downloaded images and search results, from the previous call of search()
        :yield:
        """
        for result in tqdm(self.search_results):
            image = self.download_image(result["image"])
            if image is None:
                continue

            yield result, image

    def download_image(self, url):
        """
        Download the image from the given URL
        :param url: Target URL
        :return: Downloaded images in PIL format
        """
        try:
            img_data = requests.get(url)
            bytes_data = BytesIO(img_data.content)
            image = Image.open(bytes_data).convert("RGB")
            return image
        except:
            print(f"\nFailed to download image. Url: {url}")
        return None

    def fetch_token(self, keywords):
        """
        Pre-fetch the token required for the given keyword search
        :param keywords: Query string used in subsequent search call
        :return: Qvd token
        """
        response = requests.post(self.url, data={'q': keywords})
        re_search_res = re.search(r'vqd=([\d-]+)\&', response.text, re.M | re.I)
        if not re_search_res:
            print("Couldn't find vqd token. Exiting.")
            exit(-1)

        return re_search_res.group(1)

    def get_headers(self):
        """
        Returns an object containing the headers used for search query
        :return: Headers object
        """
        return {
            'authority': 'duckduckgo.com',
            'accept': 'application/json, text/javascript, */* q=0.01',
            'sec-fetch-dest': 'empty',
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'referer': 'https://duckduckgo.com/',
            'accept-language': 'en-US,enq=0.9',
        }

    def get_params(self, keywords, token):
        """
        Returns the parameters object based on the input
        :param keywords: Query string
        :param token: Qvd token
        :return: Parameters object
        """
        return (
            ('l', 'us-en'),
            ('o', 'json'),
            ('q', keywords),
            ('vqd', token),
            ('f', ',,,'),
            ('p', '1'),
            ('v7exp', 'a'),
        )


if __name__ == '__main__':
    # query = "scatter plot, scatter chart"
    # query = "histogram"
    # query = "bar plot, bar chart, bar graph"
    # query = "violin plot"
    # query = "line plot, line chart, line graph, curve chart"
    # query = "box plot, boxplot"
    query = "pie chart, circle chart"
    dir = "D:/project/plots_duckduckgo/pie_chart"
    max_results = 500

    Path(dir).mkdir(parents=True, exist_ok=True)

    image_search = DuckduckgoImageSearch()
    image_search.search(query, max_results=max_results)

    # Download the images and save them
    for idx, (data, image) in enumerate(image_search.download_images_gen()):
        image.save(os.path.join(dir, f"{idx}.jpeg"))
        save_json_metadata(dir, str(idx), {"url": data["image"], "name": str(idx)})
