from connector import Connector

API_KEY_ID = "PKC5LZY4HEJ9BL9EGHXE"
API_SECRET_KEY = "gJsV346k4dhS65hvWvj58Knlb5wfgMLjLPgGTeNZ"
API_URL = 'https://paper-api.alpaca.markets'

conn = Connector(API_URL, API_KEY_ID, API_SECRET_KEY)
# conn.place_order("BTCUSD", "1000", "buy")
buy_resp = conn.place_buy_order("BTCUSD", "100").json()
print(buy_resp)
qty = buy_resp['qty']

sell_resp = conn.place_sell_order("BTCUSD", qty).json()
print(sell_resp)
