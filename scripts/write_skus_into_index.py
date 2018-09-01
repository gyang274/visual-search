"""write skus into index
Author: yg <gyang274@gmail.com>
"""

import json

from tqdm import tqdm

from elasticsearch import Elasticsearch

es = Elasticsearch('http://127.0.0.1:9200')


def main():
  skus = json.load(open('./skus_insitu_im2vec.json'))
  payload = []
  for sku in tqdm(skus):
    payload.append(json.dumps({'index': {}}))
    payload.append(json.dumps(sku))
  es.bulk('\n'.join(payload), index='yg-vs-es-index', doc_type='_doc')
  es.indices.refresh(index='yg-vs-es-index')


if __name__ == '__main__':
  main()

