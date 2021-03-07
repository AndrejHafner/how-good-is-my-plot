from google_images_search import GoogleImagesSearch
from env import *
from pathlib import Path


# you can provide API key and CX using arguments,
# or you can set environment variables: GCS_DEVELOPER_KEY, GCS_CX
gis = GoogleImagesSearch(GOOGLE_API_KEY, PROJECT_CX)

# define search params:
_search_params = {
    'q': 'ursa zrimsek',
    'num': 20
    # 'safe': 'high|medium|off',
    # 'fileType': 'jpg|gif|png',
    # 'imgType': 'clipart|face|lineart|news|photo',
    # 'imgSize': 'huge|icon|large|medium|small|xlarge|xxlarge',
    # 'imgDominantColor': 'black|blue|brown|gray|green|pink|purple|teal|white|yellow',
    # 'rights': 'cc_publicdomain|cc_attribute|cc_sharealike|cc_noncommercial|cc_nonderived'
}

# this will only search for images:
# try:
Path(f'./downloaded/{_search_params["q"]}').mkdir(parents=True, exist_ok=True)
gis.search(search_params=_search_params, path_to_dir=f'./downloaded/{_search_params["q"]}')
# except:
#     print("err")
# b = gis.results()
# a = 0
# this will search and download:
# gis.search(search_params=_search_params, path_to_dir='/path/')
#
# # this will search, download and resize:
# gis.search(search_params=_search_params, path_to_dir='/path/', width=500, height=500)
#
# # search first, then download and resize afterwards:
# gis.search(search_params=_search_params)
# for image in gis.results():
#     image.download('/path/')
#     image.resize(500, 500)