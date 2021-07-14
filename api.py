import json
import websockets
import asyncio

from credentials import client_id, client_secret, url


class client(object):
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.url = url
        self.json = {
            "jsonrpc" : "2.0",
        }


    async def public_auth(self, request):
        '''
        Retrieve an Oauth access token, to be used
        for authentication of 'private' requests.
        '''
        context = {
            "grant_type" : "client_credentials",
            "client_id" : self.client_id,
            "client_secret" : self.client_secret
        }
        self.json["id"] = 9929
        self.json["method"] = "public/auth"
        self.json["params"] = context
        async with websockets.connect(self.url) as websocket:
            await websocket.send(request)
            while websocket.open:
                response = await websocket.recv()
                response = json.loads(response)
                print(response)
        return response


    async def cancel_order(self, request):
        '''
        This method cancels all users orders and trigger
        orders within all currencies and instrument kinds.
        This method takes no parameters.
        '''
        self.json["id"] = 8748
        self.json["method"] = "private/cancel_all"
        async with websockets.connect(self.url) as websocket:
            await websocket.send(request)
            response = await websocket.recv()
            response = json.loads(response)
            print(response)
        return asyncio.get_event_loop().run_until_complete(self.order_canceling(json.dumps(request)))
    

    async def buy_order(self, request, instrument_name, amount, type, label):
        '''
        This method cancels all users orders and trigger
        orders within all currencies and instrument kinds.
        This method takes no parameters.
        '''
        context = {
            "instrument_name" : instrument_name,
            "amount" : amount,
            "type" : type,
            "label" : label
        }
        self.json["id"] = 5275
        self.json["method"] = "private/buy"
        self.json["params"] = context
        async with websockets.connect(self.url) as websocket:
            await websocket.send(request)
            response = await websocket.recv()
            response = json.loads(response)
            print(response)
        return asyncio.get_event_loop().run_until_complete(self.buy_order(json.dumps(request)))


    async def sell_order(self, request, instrument_name, amount, type, price, trigger_price, trigger):
        context = {
            "instrument_name" : instrument_name,
            "amount" : amount,
            "type" : type,
            "price" : price,
            "trigger_price" : trigger_price,
            "trigger" : trigger
        }
        self.json["id"] = 2148
        self.json["method"] = "private/sell"
        self.json["params"] = context
        async with websockets.connect(self.url) as websocket:
            await websocket.send(request)
            response = await websocket.recv()
            response = json.loads(response)
            print(response)
        return asyncio.get_event_loop().run_until_complete(self.sell_order(json.dumps(request)))



