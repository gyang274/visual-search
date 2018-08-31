# Visual Search with Tensorflow Serving, Elasticsearch, VueJS and Nginx

## One Step Setup 

Create a visual search platform in one step:

```
# git clone git@github.com:gyang274/visual-search.git
git clone https://github.com/gyang274/visual-search.git

cd visual-search

docker-compose up
```

Open a your faviorate browser, http://127.0.0.1/#/, try some URL and local file with visual search

https://www.potterybarn.com/pbimgs/ab/images/dp/wcm/201824/0483/trieste-dining-chair-o.jpg

The docker image contains 1080 furniture images by default, you can add your own images using the `Manage` page, or using the scripts provided by this repository. 

## TODO

- How to add images using `Manage` page.

- How to add images in bulk using docker cp and python scripts.

