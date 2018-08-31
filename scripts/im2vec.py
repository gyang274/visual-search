"""im2vec.py: get image vector via inception-resnet-v2 tensorflow serving rest api at yg-vs-bd.
Author: yg <gyang274@gmail.com>
"""

import base64
import json
import requests

import numpy as np

from tqdm import tqdm


# image_vec from image_src
def get_vector_from_source(image_src):

  tfs_endpoint = 'http://127.0.0.1/bd/v1/models/slim_inception_resnet_v2:predict'

  # image_str = requests.get(image_src).content
  image_str = open(image_src, 'rb').read()

  image_b64 = base64.b64encode(image_str).decode('utf-8')

  signature = dict(
    signature_name='omnium',
    instances=list([
      dict(
        images=dict(
          b64=image_b64
        )
      )
    ])
  )

  responses = requests.post(
    tfs_endpoint, json=signature
  )

  image_vec = responses.json().get('predictions', list([dict()]))[0].get('vector')

  return image_vec


# image_tkn from image_vec
def get_sign(x):
  if x >= 0:
    return '+'
  else:
    return '-'


def get_tokens_from_vector_sign(vector, n=256):

  assert vector is not None and n != 0, 'Invalid vector, or n.'

  tokens = [
    'i{index}v{value}'.format(
      index=i, value=get_sign(vector[i])
    ) for i in np.argpartition(
      np.abs(vector), -n)[-n:]
  ]

  return tokens


def get_tokens_from_vector_round(vector, n=256, ndigits=0):

  assert vector is not None and n != 0 and ndigits >= -1, 'Invalid vector, n, or ndigits.'

  if ndigits == -1:
    return get_tokens_from_vector_sign(vector, n)

  tokens = [
    'i{index}v{value}'.format(
      index=i, value=round(vector[i], ndigits)
    ) for i in np.argpartition(
      np.abs(vector), -n)[-n:]
  ]

  return tokens


def get_vecstr_from_vector(vector, precision=4):
  return ' '.join([str(round(v, precision)) for v in vector])


# main
def main():
  skus = json.load(open('./skus_insitu.json'))
  for sku in tqdm(skus):
    image_vec = get_vector_from_source(sku['image_src'].replace('http://127.0.0.1/images', './assets/insitu'))
    if image_vec is not None:
      sku['image_vec'] = get_vecstr_from_vector(image_vec)
      sku['image_tkn'] = get_tokens_from_vector_sign(image_vec)
    else:
      print('Invalid im2vec: {}'.format(sku['image_src']))
  with open('./skus_insitu_im2vec.json', 'w') as fp:
    json.dump(skus, fp)

  skus = json.load(open('./skus_onsite.json'))
  for sku in tqdm(skus):
    image_vec = get_vector_from_source(sku['image_src'].replace('http://127.0.0.1/images', './assets/onsite'))
    if image_vec is not None:
      sku['image_vec'] = get_vecstr_from_vector(image_vec)
      sku['image_tkn'] = get_tokens_from_vector_sign(image_vec)
    else:
      print('Invalid im2vec: {}'.format(sku['image_src']))
  with open('./skus_onsite_im2vec.json', 'w') as fp:
    json.dump(skus, fp)


if __name__ == '__main__':
  main()

