#!/bin/bash


function build_image(){
    imgname=$1
    docker build --tag=$imgname .
    docker push $imgname
}

if [ "$1" = "test" ];then
  imgname=sammrai/fetch_ohlcv:test
  docker build --tag=$imgname .
  docker run --rm $imgname --exchanges ftx kraken --symbols BTC/USD ETH/USD
  exit
fi


if [ -z "$(git status --porcelain)" ]; then
  echo "start builds."
else
  git status
  echo "commit first before build."
  exit 1
fi

tag=`git rev-parse --short HEAD`
build_image sammrai/fetch_ohlcv:$tag
build_image sammrai/fetch_ohlcv:latest