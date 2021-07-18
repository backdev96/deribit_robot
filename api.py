from credentials import (client_id, client_secret, auth_url,
                get_order_book_url,
                cancel_orders_url, trade_url, get_open_orders_url)

import requests
import json

class Robot(object):
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth_url = auth_url
        self.get_order_book_url = get_order_book_url
        self.cancel_orders_url = cancel_orders_url
        self.session = requests.Session()
        self.trade_url = trade_url
        self.get_open_orders_url = get_open_orders_url


    def auth(self):
        context = {
            'client_id' : self.client_id,
            'client_secret' : self.client_secret,
            'grant_type' : 'client_credentials',
        }
        response = self.session.get(self.auth_url, params=context)
        return json.loads(response.text)['result']['access_token']


    def request(self, url, context):
        auth_token = self.auth()
        response = self.session.get(url, params=context, headers = {
            'Accept':'application/json', 
            'Authorization': f'bearer {auth_token}'})
        return response


    def trade(self, instrument_name, amount, price, method):
        context = {
            'instrument_name' : instrument_name,
            'amount' : amount,
            'price' : price
        }
        if method == 'sell':
            return self.request(self.trade_url + method, context)
        elif method == 'buy':
            return self.request(self.trade_url + method, context)

                

    def get_order_book(self, instrument_name, depth):
        context = {
            'instrument_name' : instrument_name,
            'depth' : depth
        }
        return self.request(self.get_order_book_url, context)
    

    def cancel_orders(self, typeDef='all'):
        return self.request(cancel_orders_url, {'type': typeDef})
    

    def get_open_orders(self, instrument_name):
        context = {
            'instrument_name' : instrument_name,
        }
        return self.request(self.get_open_orders_url, context)

robot = Robot(client_id, client_secret)

# robot.auth()
# robot.cancel_orders()
# robot.buy_order('BTC-PERPETUAL', 40, 'market', 'market0000234')
# robot.sell_order(10, 'BTC-PERPETUAL', 145.61, 'last_price', 145)
#robot.get_order_book('BTC-PERPETUAL', 5)
# headers = {
#             'Accept':'application/json', 
#             'Authorization':  self.auth()
#         }
# self.request(self.private_buy_url, context)