import requests
import re
import json
import os

from pathlib import Path
from tqdm import tqdm
from io import BytesIO
from PIL import Image


class DuckduckgoImageSearch:

    def __init__(self):
        self.url = 'https://duckduckgo.com/'
        self.search_results = []

    def search(self, keywords, max_results=100):
        vqd_token = self.fetch_token(keywords)

        params = self.get_params(keywords, vqd_token)
        headers = self.get_headers()

        request_url = self.url + "i.js"
        self.search_results = []

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
        for result in tqdm(self.search_results):
            image = self.download_image(result["image"])
            if image is None:
                continue

            yield result, image

    def download_image(self, url):
        try:
            img_data = requests.get(url)
            bytes_data = BytesIO(img_data.content)
            image = Image.open(bytes_data).convert("RGB")
            return image
        except:
            print(f"\nFailed to download image. Url: {url}")
        return None



    def fetch_token(self, keywords):
        response = requests.post(self.url, data={'q': keywords})
        re_search_res = re.search(r'vqd=([\d-]+)\&', response.text, re.M | re.I)
        if not re_search_res:
            print("Couldn't find vqd token. Exiting.")
            exit(-1)

        return re_search_res.group(1)

    def get_headers(self):
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
    query = "scatter plot, scatter chart"
    dir = "./downloaded/scatter_plot"
    Path(dir).mkdir(parents=True, exist_ok=True)

    image_search = DuckduckgoImageSearch()
    image_search.search(query, max_results=500)

    for idx, (data, image) in enumerate(image_search.download_images_gen()):
        image.save(os.path.join(dir, f"{idx}.jpeg"))




# def search(keywords, max_results=None):
#     url = 'https://duckduckgo.com/'
#
#     #   First make a request to above URL, and parse out the 'vqd'
#     #   This is a special token, which should be used in the subsequent request
#     res = requests.post(url, data=params)
#     searchObj = re.search(r'vqd=([\d-]+)\&', res.text, re.M|re.I)
#
#     if not searchObj:
#         print("Couldn't find vqd token. Exiting.")
#         exit(-1)
#
#     return searchObj.group(1)
#
#
#     headers = {
#         'authority': 'duckduckgo.com',
#         'accept': 'application/json, text/javascript, */* q=0.01',
#         'sec-fetch-dest': 'empty',
#         'x-requested-with': 'XMLHttpRequest',
#         'user-agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
#         'sec-fetch-site': 'same-origin',
#         'sec-fetch-mode': 'cors',
#         'referer': 'https://duckduckgo.com/',
#         'accept-language': 'en-US,enq=0.9',
#     }
#
#     params = (
#         ('l', 'us-en'),
#         ('o', 'json'),
#         ('q', keywords),
#         ('vqd', searchObj.group(1)),
#         ('f', ',,,'),
#         ('p', '1'),
#         ('v7exp', 'a'),
#     )
#
#     requestUrl = url + "i.js"
#
#
#     while True:
#         while True:
#             try:
#                 res = requests.get(requestUrl, headers=headers, params=params)
#                 data = json.loads(res.text)
#                 break
#             except ValueError as e:
#                 time.sleep(5)
#                 continue
#
#
#         if "next" not in data:
#             exit(0)
#
#         requestUrl = url + data["next"]
#
#
# search("audi q6")