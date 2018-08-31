# Visual Search with Tensorflow Serving Inception-Resnet-V2, Elasticsearch, VueJS and Nginx

- version 1.0.0 sketch

```
# start with //docker-compose.yml yg-vs-<bd|es|fd>:skeleton

# start docker yg-vs_bd w. tensorflow-serving grpc at 9000 and rest at 9020
# start docker yg-vs_es w. elasticsearch at 9200
# start docker yg-vs_fd w. nginx at 80 w. reverse proxy to bd at /bd and es at /es

docker-compose -p yg-vs build

docker-compose -p yg-vs build <service_name[bd|es|fd]>

docker-compose -p yg-vs up
```

```
# inspect fd, es, and bd

fd: http://127.0.0.1/#/ 
es: http://127.0.0.1/es/ (nginx) or http://127.0.0.1:9200/ (direct)
bd: http://127.0.0.1/bd/ (nginx) or http://127.0.0.1:9020/ (direct)
```

```
# get assets images and skus info

cd //releases/v1.0.0/scripts/

pip install tensorflow tensorflow-gpu elasticsearch

# retrive images and docker cp insitu to yg-vs-fd container 

python scrape2skus.py

# src_path end with /. so that copy the content within directory, instead of directory.
docker cp ./assets/insitu/. yg-vs-fd:/app/dist/images/

# process images into vector and tokens

python im2vec.py

# set index and insert datum into yg-vs-es elasticsearch service

python set_index.py

curl http://127.0.0.1/es/_cat/indices

curl http://127.0.0.1:9200/_cat/indices

python write_skus_into_index.py
```

```
# commit docker containers into docker images

docker commit yg-vs-bd gyang274/yg-vs-bd:v1.0.0

docker commit yg-vs-es gyang274/yg-vs-es:v1.0.0

docker commit yg-vs-fd gyang274/yg-vs-fd:v1.0.0
```

```
# push image into docker hub repository
docker push gyang274/yg-vs-bd:v1.0.0
docker push gyang274/yg-vs-es:v1.0.0
docker push gyang274/yg-vs-fd:v1.0.0
```
