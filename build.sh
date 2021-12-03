#!/bin/bash

if [ -z "$(git status --porcelain)" ]; then
  echo "start builds."
else
  git status
  echo "commit first before build."
  exit 1
fi

function build_image(){
    imgname=$1
    docker build --tag=$imgname .
    docker push $imgname
}

tag=`git rev-parse --short HEAD`
build_image sammrai/fetch_ohlcv:$tag
build_image sammrai/fetch_ohlcv:latest