import json

from elasticsearch import Elasticsearch


skus = json.load(open('./skus_insitu_im2vec.json'))

sku = skus[0]

all_dist =  \
  [{
    "script_score": {
      "script": {
        "source": "euclidean_distance",
        "lang": "yg-scripts",
        "params": {
          "field": "image_vec",
          "values":  [float(x) for x in sku['image_vec'].split(' ')]  # need slight caution
        }
      }
    },
    "weight": -1
  }]
# image tokens
all_fun = [
  {
    'filter': {
      'term': {
        'image_tkn': xx
      }
    },
    'weight': 1
  } for xx in sku['image_tkn']
]

k = 10
es_size = 10
all_filter = []

body = \
  {
    "size": k,
    "_source": [
      "title",
      "label",
      "image_src",
      "image_vec",
      "image_tkn",
      "_score"
    ],
    "query": {
      "function_score": {
        "query": {
          "bool": {
            "must": all_filter  # can use QSU for filter
          }
        },
        "functions": all_fun,
        "score_mode": "sum"
      }
    },
    "rescore": {
      "window_size": es_size,
      "query": {
        "rescore_query": {
          "function_score": {
            "query": {
              "match_all": {}
            },
            "functions": all_dist,
            "score_mode": "sum",
            "boost_mode": "replace"
          }
        },
        "query_weight": 0,
        "rescore_query_weight": 1
      }
    }
  }

es = Elasticsearch('http://127.0.0.1:9200')

hits = es.search(index='yg-vs-es-index', body=body)


