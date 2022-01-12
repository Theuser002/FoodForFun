#!/bin/bash

echo "This project is credited by HoHuHuPhuHo. Let's start!"

if [[ $(docker ps -a | grep foodforfun-1.2) ]]; then
    echo 'Food for fun exists'
    docker rm -f foodforfun-1.2
else 
    echo 'No food for fun'
fi

docker build -t foodforfun:1.2 .

docker run \
--name foodforfun-1.2 \
-p 4321:4321 \
--restart always \
foodforfun:1.2