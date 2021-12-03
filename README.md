# this is
an ohlcv fetcher for influx data format.

# usage:
docker run --rm fetch_ohlcv:latest [-h] --exchanges [EXCHANGES [EXCHANGES ...]] --symbols
                      [SYMBOLS [SYMBOLS ...]] [--timeframe TIMEFRAME]

or run it in your environment:

python fetch_ohlcv.py [-h] --exchanges [EXCHANGES [EXCHANGES ...]] --symbols
                      [SYMBOLS [SYMBOLS ...]] [--timeframe TIMEFRAME]

# example:

```
$ docker run --rm fetch_ohlcv:latest --exchanges ftx kraken --symbols BTC/USD ETH/USD
market_test,exchange=FTX,symbol=BTC/USD,timeframe=1m open=55846.0,high=55950.0,low=55766.0,close=55843.0,volume=1460420.5062 1638547320000000000
market_test,exchange=FTX,symbol=BTC/USD,timeframe=1m open=55851.0,high=55893.0,low=55701.0,close=55755.0,volume=1636610.0936 1638547380000000000
market_test,exchange=FTX,symbol=BTC/USD,timeframe=1m open=55754.0,high=55920.0,low=55731.0,close=55823.0,volume=1690945.4552 1638547440000000000
market_test,exchange=FTX,symbol=BTC/USD,timeframe=1m open=55821.0,high=55823.0,low=55571.0,close=55671.0,volume=2053419.5758 1638547500000000000
market_test,exchange=FTX,symbol=BTC/USD,timeframe=1m open=55664.0,high=55707.0,low=55544.0,close=55544.0,volume=1578248.4863 1638547560000000000
market_test,exchange=FTX,symbol=ETH/USD,timeframe=1m open=4449.1,high=4453.7,low=4444.7,close=4448.3,volume=2177670.3817 1638547320000000000
market_test,exchange=FTX,symbol=ETH/USD,timeframe=1m open=4448.4,high=4454.6,low=4416.0,close=4422.2,volume=5542374.1859 1638547380000000000
market_test,exchange=FTX,symbol=ETH/USD,timeframe=1m open=4422.2,high=4444.8,low=4416.4,close=4436.1,volume=5344918.8095 1638547440000000000
market_test,exchange=FTX,symbol=ETH/USD,timeframe=1m open=4436.4,high=4437.3,low=4407.3,close=4412.3,volume=4715969.4813 1638547500000000000
market_test,exchange=FTX,symbol=ETH/USD,timeframe=1m open=4412.3,high=4416.3,low=4381.0,close=4383.8,volume=4898206.5443 1638547560000000000
market_test,exchange=Kraken,symbol=BTC/USD,timeframe=1m open=55880.0,high=55932.2,low=55801.3,close=55820.0,volume=3.97647873 1638547320000000000
market_test,exchange=Kraken,symbol=BTC/USD,timeframe=1m open=55820.0,high=55882.8,low=55556.0,close=55754.4,volume=43.77752412 1638547380000000000
market_test,exchange=Kraken,symbol=BTC/USD,timeframe=1m open=55754.4,high=55882.7,low=55736.2,close=55813.5,volume=3.69913319 1638547440000000000
market_test,exchange=Kraken,symbol=BTC/USD,timeframe=1m open=55813.5,high=55829.6,low=55630.0,close=55666.6,volume=3.2201925 1638547500000000000
market_test,exchange=Kraken,symbol=BTC/USD,timeframe=1m open=55650.8,high=55667.3,low=55556.0,close=55557.2,volume=9.16245644 1638547560000000000
market_test,exchange=Kraken,symbol=ETH/USD,timeframe=1m open=4451.19,high=4451.81,low=4447.0,close=4447.0,volume=57.45203599 1638547320000000000
market_test,exchange=Kraken,symbol=ETH/USD,timeframe=1m open=4447.0,high=4454.1,low=4420.0,close=4425.76,volume=598.85125035 1638547380000000000
market_test,exchange=Kraken,symbol=ETH/USD,timeframe=1m open=4421.16,high=4445.09,low=4420.73,close=4432.61,volume=126.11416368 1638547440000000000
market_test,exchange=Kraken,symbol=ETH/USD,timeframe=1m open=4432.61,high=4437.15,low=4411.0,close=4414.2,volume=290.83162068 1638547500000000000
market_test,exchange=Kraken,symbol=ETH/USD,timeframe=1m open=4412.6,high=4417.61,low=4390.0,close=4390.0,volume=548.47544983 1638547560000000000
```

# telegraf integration
simply write the following settings to your telegraf config file:

```:telegraf.conf
[[inputs.exec]]
  commands = ["docker run --rm fetch_ohlcv:latest --exchanges ftx kraken --symbols BTC/USD ETH/USD"]
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
available exchanges: ['aax', 'aofex', 'ascendex',
'bequant', 'bibox', 'bigone', 'binance',
'binancecoinm', 'binanceus', 'binanceusdm', 'bit2c',
'bitbank', 'bitbay', 'bitbns', 'bitcoincom',
'bitfinex', 'bitfinex2', 'bitflyer', 'bitforex',
'bitget', 'bithumb', 'bitmart', 'bitmex', 'bitpanda',
'bitrue', 'bitso', 'bitstamp', 'bitstamp1', 'bittrex',
'bitvavo', 'bl3p', 'btcalpha', 'btcbox', 'btcmarkets',
'btctradeua', 'btcturk', 'buda', 'bw', 'bybit',
'bytetrade', 'cdax', 'cex', 'coinbase',
'coinbaseprime', 'coinbasepro', 'coincheck', 'coinex',
'coinfalcon', 'coinmarketcap', 'coinmate', 'coinone',
'coinspot', 'crex24', 'currencycom', 'delta',
'deribit', 'digifinex', 'eqonex', 'equos', 'exmo',
'flowbtc', 'ftx', 'ftxus', 'gateio', 'gemini',
'hitbtc', 'hitbtc3', 'hollaex', 'huobi', 'huobijp',
'huobipro', 'idex', 'independentreserve', 'indodax',
'itbit', 'kraken', 'kucoin', 'kuna', 'latoken',
'latoken1', 'lbank', 'liquid', 'luno', 'lykke',
'mercado', 'mexc', 'ndax', 'novadax', 'oceanex',
'okcoin', 'okex', 'okex3', 'okex5', 'paymium',
'phemex', 'poloniex', 'probit', 'qtrade', 'ripio',
'stex', 'therock', 'tidebit', 'tidex', 'timex',
'upbit', 'vcc', 'wavesexchange', 'whitebit', 'xena',
'yobit', 'zaif', 'zb']

## --symbols [SYMBOLS [SYMBOLS ...]]
an example of symbols: ['BTC/USD', 'ETH/USD',
'ETH/JPY', 'BTC/JPY', 'XRP/JPY']

## --timeframe TIMEFRAME
timeframe: ['1m', '1h', '1d']