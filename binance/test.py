from binance.spot import Spot
from include import print_json
import time

base_url = "https://testnet.binance.vision"  # "https://api.binance.com"
#status = '/sapi/v1/system/status'
#coins = "/sapi/v1/capital/config/getall"
key = "s73DXQrcslRPRsS3m79QhPFQKG28fP3qx0kTMSEBQTsMWCcn9LMh45kWHWMsoMpB"
secret = "Nlu6mSnVsWillR6RUhPFLlDfunIO4IdvLDZPKIejaBH9riUBuPoNRPbfxerPv9pT"
# x = requests.get(base_url+status)
# print(x.text)

client = Spot(base_url=base_url,
              key=key,
              secret=secret)

#x = client.exchange_info(None, ["BTCUSDT", "ETHUSDT"])
x = client.klines("BTCUSDT", "1m", limit=1000)

print(print_json(x))
print(type(x))

last_time = x[-1][0]
now = time.time()*1000
print(f"Last time {last_time}")
print(f"Now {now}")
diff = now-last_time
print(f"Time diff: {diff} ms.")
diff /= 1000
print(f"Time diff: {diff} s.")
diff /= 60
print(f"Time diff: {diff} .")
