from datetime import datetime
import calendar
import ccxt.async_support as ccxt
import asyncio
import argparse
import ccxt as ccxt_sync


class HelpSymbolsAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if values:
            self.sample_symbols(values)
        else:
            print("Usage: --help-symbols <exchange>")
        parser.exit()

    def sample_symbols(self, exchange_id):
        if exchange_id in ccxt_sync.exchanges:
            try:
                exchange_class = getattr(ccxt_sync, exchange_id)
                exchange = exchange_class()
                markets = exchange.load_markets()
                print("Available symbols for {}: {}".format(exchange_id, ", ".join(list(markets.keys()))))
            except Exception as e:
                print(f"Error loading symbols for {exchange_id}: {e}")
        else:
            print(f"Exchange `{exchange_id}` is not supported.")

parser = argparse.ArgumentParser(description='A tool to fetch OHLCV data.')
parser.add_argument('--exchanges', required=True, nargs="*", type=str, help='List of exchanges. Available: {}'.format(", ".join(ccxt.exchanges)))
parser.add_argument('--symbols', required=True, nargs="*", type=str, help='Specify symbols to fetch data for. Use --help-symbols <exchange> to view available symbols.')
parser.add_argument('--timeframe', required=False, default="1m", type=str, help='Timeframe options: 1m, 1h, 1d')
parser.add_argument('--help-symbols', action=HelpSymbolsAction, nargs='?', type=str, help='Show available symbols for a specified exchange')

args = parser.parse_args()

def cleanNullTerms(d):
    return {
      k:v
      for k, v in d.items()
      if v is not None
   }

class InfluxDBClientText():
    def __init__(self,url=None, token=None, org=None, bucket=None):
        self.url=url
        self.token=token
        self.org=org
        self.params={"bucket":bucket ,"org":org}
        self.headers={"Authorization":"Token {}".format(token)}
        self.conveq=lambda x: ["{}={}".format(k,v) for k,v in x.items()]
    
    def write(self,point,measurement,tag=None,time=None):
        measurement = cleanNullTerms(measurement)
        if not tag: tag = {}
        data=[str(point)]+self.conveq(tag)
        data=",".join(data)
        
        data=data+" "+",".join(self.conveq(measurement))
        if time:
            time=str(time).replace(".","")
            time=time+"0"*(19-len(time))
            data+=" "+str(time)
        print(data)

c=InfluxDBClientText()

exchanges = {e:{"rate_limit" : 1} for e in args.exchanges}
exchanges = [getattr(ccxt,exchange)(keys) for exchange,keys in exchanges.items()]

keys=["time","open","high","low","close","volume"]
symbols=args.symbols
timeframe=args.timeframe

now = datetime.utcnow()
unixtime = calendar.timegm(now.utctimetuple())
since = (unixtime - 60 * 5) * 1000

async def print_ohlcv(exchange, symbol, timeframe, since):
    ohlcvs = await exchange.fetch_ohlcv(symbol=symbol, timeframe=timeframe, since=since)
    ohlcvs = [dict(zip(keys,ohlcv)) for ohlcv in ohlcvs]
    tag={"exchange":exchange.name,"symbol":symbol,"timeframe":timeframe}
    for ohlcv in ohlcvs:
        t_ = ohlcv.pop("time")
        r = c.write(point="exchange",measurement=ohlcv,tag=tag,time=t_)

async def main():

    cors=[]
    for exchange in exchanges:
        await exchange.load_markets()
        for symbol in symbols:
            if symbol not in exchange.symbols : continue
            cors.append(print_ohlcv(exchange,symbol=symbol, timeframe=timeframe, since=since))

    await asyncio.gather(*cors)
    for exchange in exchanges:
        await exchange.close()


asyncio.get_event_loop().run_until_complete(main())

