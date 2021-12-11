#!/bin/bash

echo "This project is credited by HoHuHuPhuHo. Let's start!"

docker build -t foodforfun:1.0 .

docker run -n foodforfun \
-p 8080:8080 \
--restart always \
foodforfun:1.0