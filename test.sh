#!/bin/bash


function build_image(){
    imgname=$1
    docker build --tag=$imgname .
    docker push $imgname
}

imgname=sammrai/fetch_ohlcv:test
docker build --tag=$imgname .

if [ "$1" = "login" ];then
  docker run --rm -it -v $(pwd):/work -w /work --entrypoint '' $imgname bash
else
  docker run --rm $imgname --exchanges kucoin kraken --symbols BTC/USDT ETH/USDT
fi