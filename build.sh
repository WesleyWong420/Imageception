#!/bin/bash
docker rm -f imageception
docker build --tag=imageception . && \
docker run -p 1005:1337 --restart=on-failure --name=imageception --detach imageception
