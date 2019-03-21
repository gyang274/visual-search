# Visual Search with Tensorflow Serving, Elasticsearch, VueJS and Nginx

## [Demo Video on Youtube](https://www.youtube.com/watch?v=f_ZRX3mC6RI&t=1s)

[Integrate Textual and Visual Search using Tensorflow Serving and Elasticsearch](https://www.youtube.com/watch?v=f_ZRX3mC6RI&t=1s)

This demo is created from visual-search-v2.0, which includes color filter, numeric filter and text search. We are going to update this git repo (visual-search-v1.0) soon.

## One Step Setup 

Create a visual search platform in one step:

```
# git clone git@github.com:gyang274/visual-search.git
git clone https://github.com/gyang274/visual-search.git

cd visual-search

docker-compose up
```

Open your favorite browser with http://127.0.0.1/#/, try some URL and local file with visual search, e.g., https://www.potterybarn.com/pbimgs/ab/images/dp/wcm/201824/0483/trieste-dining-chair-o.jpg

The docker image contains 1080 furniture images by default. You can add your own images using the `Manage` page, or using the scripts provided by this repository. 

## TODO

- How to add images using the `Manage` page.

- How to add images in bulk using docker cp and python scripts.

