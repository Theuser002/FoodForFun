#!/bin/bash

echo "This project is credited by HoHuHuPhuHo. Let's start!"

if [[ $(docker ps -a | grep foodforfun) ]]; then
    echo 'Food for fun exists'
    docker rm -f foodforfun
else 
    echo 'No food for fun'
fi

docker build -t foodforfun:1.0 .