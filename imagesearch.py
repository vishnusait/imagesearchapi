# create a output directory to place the images and specify it at -o
# prequsites include pyhton, opencv2 etc.,
# USAGE
# python imagesearch.py --q cats --o cats

import requests
import random
import argparse
import cv2
import os

ap = argparse.ArgumentParser()
ap.add_argument("-q", "--query", required=True,
	help="search query to search API for")
ap.add_argument("-o", "--output", required=True,
	help="path to output directory of images")
args = vars(ap.parse_args())
total = 0
search = requests.get("https://api.qwant.com/api/search/images",
    params={
        'count': 50,
        'q': args["query"],
        't': 'images',
        'safesearch': 0,
        'locale': 'en_US',
        'uiv': 4
    },
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    }
)
search.raise_for_status()
response = search.json().get('data').get('result').get('items')
urls = [search.get('media') for search in response]
#results = search["result"]
print(urls)
for v in urls:
    print("[INFO] fetching")
    r = requests.get(v, timeout=30)
    ext = ".jpg"
    p = os.path.sep.join([args["output"], "{}{}".format(str(total).zfill(8), ext)])
    # write the image to disk
    f = open(p, "wb")
    f.write(r.content)
    f.close()
    image = cv2.imread(p)
    if image is None:
        print("[INFO] deleting: {}".format(p))
        os.remove(p)
        continue
    total += 1
print("[DONE] your images are ready in {}".format([args["output"]))