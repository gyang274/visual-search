"""Set index in Elasticsearch
Author: yg <gyang274@gmail.com>
"""

from elasticsearch import Elasticsearch

index = 'yg-vs-es-index'

body = {
  'settings': {
    'index': {
      'refresh_interval': -1,
      'number_of_shards': 1,
      'number_of_replicas': 0
    }
  },
  'mappings': {
    '_doc': {
      'properties': {
        'title': {
          'type': 'text',
          'index': True,
        },
        'label': {
          'type': 'keyword',
          'index': True,
        },
        'image_src': {
          'type': 'keyword',
          'index': False,
        },
        'image_vec': {
          'type': 'keyword',
          'index': True,
        },
        'image_tkn': {
          'type': 'keyword',
          'index': True,
        }
      }
    }
  }
}

es = Elasticsearch('http://127.0.0.1:9200')

es.indices.create(index=index, body=body)

es.cat.indices()

