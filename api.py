from credentials import client_id, client_secret, auth_url, private_buy_url, get_order_book_url, private_sell_url
import requests
import json

class Robot(object):
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth_url = auth_url
        self.private_buy_url = private_buy_url
        self.get_order_book_url = get_order_book_url
        self.private_sell_url = private_sell_url
        self.session = requests.Session()


    def auth(self):
        context = {
            'client_id' : self.client_id,
            'client_secret' : self.client_secret,
            'grant_type' : 'client_credentials',
        }
        response = self.session.get(self.auth_url, params=context)
        dict = json.loads(response.text)
        return dict['result']['access_token']

    def request(self, url, context):
        auth_token = self.auth()
        response = self.session.get(url, params=context, headers = {
            'Accept':'application/json', 
            'Authorization': f'bearer {auth_token}'})
        return print(response.json())

    def buy_order(self, instrument_name:str, amount:int, type:str, label:str):
        context = {
            'instrument_name' : instrument_name,
            'amount' : amount,
            'type' : type,
            'label' : label
        }
        return self.request(self.private_buy_url, context)
    

    def sell_order(self, amount, instrument_name, price, trigger, trigger_price):
        context = {
            'amount' : amount,
            'instrument_name' : instrument_name,
            'price' : price,
            'trigger' : trigger,
            'trigger_price' : trigger_price
        }
        return self.request(self.private_sell_url, context)
    


    def get_order_book(self, instrument_name:str, depth:int):
        context = {
            'instrument_name' : instrument_name,
            'depth' : depth
        }
        return self.request(self.get_order_book_url, context)
    

robot = Robot(client_id, client_secret)

# robot.auth()
# robot.buy_order('BTC-PERPETUAL', 40, 'market', 'market0000234')
# robot.sell_order(10, 'BTC-PERPETUAL', 145.61, 'last_price', 145)
robot.get_order_book('BTC-PERPETUAL', 5)
# headers = {
#             'Accept':'application/json', 
#             'Authorization':  self.auth()
#         }
# self.request(self.private_buy_url, context)