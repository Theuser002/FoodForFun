#!/bin/bash

echo "Vietnamese Food Recognition project is credited by HoHuHuPhuHo. Let's start!"

if [[ $(docker ps -a | grep foodforfun-$1) ]]; then
    echo 'Food for fun exists'
    docker rm -f foodforfun-$1
else 
    echo 'No food for fun'
fi

docker build -t foodforfun:$1 .

docker run \
--name foodforfun-$1 \
-p $2:4321 \
--restart always \
foodforfun:$1