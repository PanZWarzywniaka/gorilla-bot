from util.connectors.alpaca_connector import AlpacaConnector
import json
API_KEY_ID = "PKC5LZY4HEJ9BL9EGHXE"
API_SECRET_KEY = "gJsV346k4dhS65hvWvj58Knlb5wfgMLjLPgGTeNZ"
API_URL = 'https://paper-api.alpaca.markets'

conn = AlpacaConnector(API_URL, API_KEY_ID, API_SECRET_KEY)
symbol = "BTCUSD"
buy_resp = conn.place_buy_order(symbol, "100").json()
conn.close_position(symbol)
# print(buy_resp)
# order_id = buy_resp['id']
# for i in range(100):
#     print(i)
#     order_info = conn.get_order(order_id).json()
#     if order_info['filled_at']:
#         break


# print(order_info)
# print("Order filled!")
# print(f"Tried to buy for {order_info['notional']} USD")
# print(f"But bought {order_info['filled_qty']} {order_info['symbol']}")
# print(f"For {order_info['filled_avg_price']}")
# spent = float(order_info['filled_qty'])*float(order_info['filled_avg_price'])
# print(f"We spent: {spent} USD")


# qty = buy_resp['qty']
# print(qty)
# sell_resp = conn.place_sell_order("BTCUSD", qty).json()
# print(sell_resp)
