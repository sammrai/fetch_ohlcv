# this is
an ohlcv fetcher for influx data format.

# usage:
docker run --rm sammrai/fetch_ohlcv:latest [-h] --exchanges [EXCHANGES [EXCHANGES ...]] --symbols
                      [SYMBOLS [SYMBOLS ...]] [--timeframe TIMEFRAME]

or run it in your environment:

python fetch_ohlcv.py [-h] --exchanges [EXCHANGES [EXCHANGES ...]] --symbols
                      [SYMBOLS [SYMBOLS ...]] [--timeframe TIMEFRAME]

# example:

```
docker run --rm sammrai/fetch_ohlcv:latest --exchanges kucoin kraken --symbols BTC/USDT ETH/USDT
```

```
exchange,exchange=KuCoin,symbol=ETH/USDT,timeframe=1m open=3029.67,high=3029.67,low=3029.51,close=3029.52,volume=2.7097698 1715316240000000000
exchange,exchange=KuCoin,symbol=ETH/USDT,timeframe=1m open=3029.26,high=3029.52,low=3029.13,close=3029.14,volume=8.2534245 1715316300000000000
exchange,exchange=KuCoin,symbol=ETH/USDT,timeframe=1m open=3029.14,high=3029.75,low=3029.14,close=3029.52,volume=6.1275113 1715316360000000000
exchange,exchange=KuCoin,symbol=ETH/USDT,timeframe=1m open=3029.52,high=3029.52,low=3029.52,close=3029.52,volume=0.0028895 1715316420000000000
exchange,exchange=KuCoin,symbol=ETH/USDT,timeframe=1m open=3029.52,high=3029.89,low=3029.51,close=3029.52,volume=7.6272211 1715316480000000000
exchange,exchange=KuCoin,symbol=BTC/USDT,timeframe=1m open=62832.1,high=62862.0,low=62832.0,close=62862.0,volume=0.44281948 1715316240000000000
exchange,exchange=KuCoin,symbol=BTC/USDT,timeframe=1m open=62861.9,high=62861.9,low=62835.1,close=62835.1,volume=0.58980588 1715316300000000000
exchange,exchange=KuCoin,symbol=BTC/USDT,timeframe=1m open=62835.1,high=62862.7,low=62835.1,close=62857.3,volume=0.60533189 1715316360000000000
exchange,exchange=KuCoin,symbol=BTC/USDT,timeframe=1m open=62858.9,high=62859.0,low=62852.9,close=62857.7,volume=0.44976205 1715316420000000000
exchange,exchange=KuCoin,symbol=BTC/USDT,timeframe=1m open=62857.6,high=62900.0,low=62857.6,close=62900.0,volume=0.59224226 1715316480000000000
exchange,exchange=Kraken,symbol=BTC/USDT,timeframe=1m open=62902.9,high=62902.9,low=62902.9,close=62902.9,volume=0.0 1715316240000000000
exchange,exchange=Kraken,symbol=BTC/USDT,timeframe=1m open=62902.9,high=62902.9,low=62902.9,close=62902.9,volume=0.0 1715316300000000000
exchange,exchange=Kraken,symbol=BTC/USDT,timeframe=1m open=62867.9,high=62867.9,low=62867.3,close=62867.4,volume=0.0348973 1715316360000000000
exchange,exchange=Kraken,symbol=BTC/USDT,timeframe=1m open=62868.1,high=62868.4,low=62860.2,close=62866.7,volume=0.20599718 1715316420000000000
exchange,exchange=Kraken,symbol=BTC/USDT,timeframe=1m open=62887.6,high=62887.6,low=62882.1,close=62886.2,volume=0.1005 1715316480000000000
exchange,exchange=Kraken,symbol=BTC/USDT,timeframe=1m open=62886.2,high=62886.2,low=62886.2,close=62886.2,volume=0.0 1715316540000000000
exchange,exchange=Kraken,symbol=ETH/USDT,timeframe=1m open=3031.74,high=3031.74,low=3031.74,close=3031.74,volume=0.0 1715316240000000000
exchange,exchange=Kraken,symbol=ETH/USDT,timeframe=1m open=3031.74,high=3031.74,low=3031.74,close=3031.74,volume=0.0 1715316300000000000
exchange,exchange=Kraken,symbol=ETH/USDT,timeframe=1m open=3031.74,high=3031.74,low=3031.74,close=3031.74,volume=0.0 1715316360000000000
exchange,exchange=Kraken,symbol=ETH/USDT,timeframe=1m open=3031.74,high=3031.74,low=3031.74,close=3031.74,volume=0.0 1715316420000000000
exchange,exchange=Kraken,symbol=ETH/USDT,timeframe=1m open=3031.74,high=3031.74,low=3031.74,close=3031.74,volume=0.0 1715316480000000000
exchange,exchange=Kraken,symbol=ETH/USDT,timeframe=1m open=3031.74,high=3031.74,low=3031.74,close=3031.74,volume=0.0 1715316540000000000
```

# telegraf integration
simply write the following settings to your telegraf config file:

```:telegraf.conf
[[inputs.exec]]
  commands = ["docker run --rm sammrai/fetch_ohlcv:latest --exchanges ftx kraken --symbols BTC/USD ETH/USD"]
  timeout = "10s"
  data_format = "influx"
  interval = "10s"
```

> In order to use the docker command inside the telegraf container, 
> you need to install the docker command in it, and mount the process file (/var/run/docker.sock:/var/run/docker.sock).
> following is an example Dockerfile.
> ```Dockerfile.telegraf
> FROM telegraf
> RUN apt update && apt install -y jq
> COPY --from=docker /usr/local/bin/docker /usr/local/bin/
> RUN groupadd -g 133 docker # 133 is docker group id of your host machine.
> RUN gpasswd -a telegraf docker
> ```

# optional arguments:
##  -h, --help
show this help message and exit

## --exchanges [EXCHANGES [EXCHANGES ...]]
List of exchanges. Available: ace, alpaca, ascendex,
                        bequant, bigone, binance, binancecoinm, binanceus,
                        binanceusdm, bingx, bit2c, bitbank, bitbay, bitbns,
                        bitcoincom, bitfinex, bitfinex2, bitflyer, bitget,
                        bithumb, bitmart, bitmex, bitopro, bitpanda, bitrue,
                        bitso, bitstamp, bitteam, bitvavo, bl3p,
                        blockchaincom, blofin, btcalpha, btcbox, btcmarkets,
                        btcturk, bybit, cex, coinbase, coinbaseinternational,
                        coinbasepro, coincheck, coinex, coinlist, coinmate,
                        coinmetro, coinone, coinsph, coinspot, cryptocom,
                        currencycom, delta, deribit, digifinex, exmo, fmfwio,
                        gate, gateio, gemini, hitbtc, hitbtc3, hollaex, htx,
                        huobi, huobijp, hyperliquid, idex, independentreserve,
                        indodax, kraken, krakenfutures, kucoin, kucoinfutures,
                        kuna, latoken, lbank, luno, lykke, mercado, mexc,
                        ndax, novadax, oceanex, okcoin, okx, onetrading, p2b,
                        paymium, phemex, poloniex, poloniexfutures, probit,
                        timex, tokocrypto, tradeogre, upbit, wavesexchange,
                        wazirx, whitebit, woo, yobit, zaif, zonda

## --symbols [SYMBOLS [SYMBOLS ...]]
an example of symbols: AVA/USDT, FET/BTC, FET/ETH, ANKR/BTC, XMR/BTC, XMR/ETH, MTV/BTC, MTV/ETH, CRO/BTC, MTV/USDT, KMD/BTC, KMD/USDT, RFOX/USDT, TEL/USDT, TT/USDT, AERGO/USDT, XMR/USDT, TRX/KCS, ATOM/BTC, ATOM/ETH, ATOM/USDT...

## --timeframe TIMEFRAME
timeframe: ['1m', '1h', '1d']
