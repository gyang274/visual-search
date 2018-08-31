import json
import os
import random
import requests
import string

from io import BytesIO
from PIL import Image
from tqdm import tqdm

from logger import logger


# def fetch_url(url):
#   try:
#     response = urlopen(url)
#     return url, response.read(), None
#   except Exception as e:
#     return url, None, e

def fetch_url(args):
  """download image with src into path.
  """

  src, path = args

  headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36',
  }

  status_code = 1

  if not os.path.exists(path):
    try:
      response = requests.get(
        src, allow_redirects=True, timeout=60, headers=headers
      )
    except:
      logger.warning(
        'Failed to fetch image at src: {}'.format(src)
      )
      return status_code
    try:
      content = response.content
      image = Image.open(BytesIO(content))
    except:
      logger.warning(
        'Failed to capture image at src: {}.'.format(src)
      )
      return status_code
    if not image.format == 'JPEG':
      try:
        image = image.convert('RGB')
      except:
        logger.warning(
          'Failed to convert into RGB image at src: {}'.format(src)
        )
        return status_code
    try:
      image.save(path, format='JPEG', quality=100)
    except:
      logger.warning(
        'Failed to save image at src: {}'.format(src)
      )
      return status_code

  status_code = 0

  return status_code


skus = json.load(
  open('scrape_results.json')
)

labels = sorted(list(set([x['product'] for x in skus])))

lbdict = {}

for lb in labels:
  lbdict[lb] = 0

random.shuffle(skus)

skus_insitu = []

skus_onsite = []

# num_each = 12
num_each = 108

for sku in tqdm(skus):

  sku_label = sku['product']

  if lbdict[sku_label] < num_each:
    status_code = fetch_url([sku['image_url'], './assets/images/'+sku['id']+'.jpg'])
    if status_code == 0:
      lbdict[sku_label] += 1
      if sku_label in ('entertainment set', 'recliner and rocker'):
        sku_dict = dict(
          title=string.capwords(sku['title']),
          label=sku_label,
          image_src='http://127.0.0.1/images/' + sku['id'] + '.jpg',
        )
        os.rename(
          './assets/images/' + sku['id'] + '.jpg',
          './assets/onsite/' + sku['id'] + '.jpg'
        )
        skus_onsite.append(sku_dict)
      else:
        sku_dict = dict(
          title=string.capwords(sku['title']),
          label=sku_label,
          image_src='http://127.0.0.1/images/' + sku['id'] + '.jpg',
        )
        os.rename(
          './assets/images/' + sku['id'] + '.jpg',
          './assets/insitu/' + sku['id'] + '.jpg'
        )
        skus_insitu.append(sku_dict)

with open('./skus_insitu.json', 'w') as fp:
  json.dump(skus_insitu, fp, indent=2)

with open('./skus_onsite.json', 'w') as fp:
  json.dump(skus_onsite, fp, indent=2)


