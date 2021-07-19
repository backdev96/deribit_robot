import time

import yaml

from api import *
from database import order_into_db


def trade():
    """
    Описание алгоритма
    1. Робот выставляет ордер номер 1 на покупку по цене
     buy price = current price - gap / 2.
    (a) Если цена уменьшается до buy price, то ордер номер 1,
     скорее всего, будет исполнен. В этом случае перейти к пункту 3.
    (b) Если цена увеличивается до такого значения,
     что становится истинным условие current price > buy price + gap + gap ignore,
     то робот должен отменить ордер номер 1. Далее, вернуться к пункту 1.
    3. Робот выставляет ордер  на продажу по цене sell price = current price + gap.
    4. (a) Если цена увеличивается до sell price,
     то ордер номер 2, скорее всего, будет исполнен. В этом
     случае вернуться к пункту 1.
    (b) Если цена уменьшается до такого значения, что становится истинным
     условие current price < sell price - gap - gap ignore,
     то робот должен отменить ордер номер 2.
     После этого следует вернуться к пункту 3.
    """
    method = 'buy'
    current_price = None
    robot.cancel_orders()
    while True:
        time.sleep(4)
        current_price = float(json.loads(robot.get_order_book(
                                         instrument_name, depth).text)\
                                         ['result']['mark_price'])
        orders_count = len(json.loads(robot.get_open_orders(
                        instrument_name).text)['result'])
        print(f'New iteration started....{orders_count}.....{method}')

        if method == 'buy':
            if orders_count == 0:
                # Buy order creation.
                buy_price = current_price - gap/2
                robot.trade(instrument_name, amount, buy_price, method)
                orders_count += 1
                print(f'Buy order created, buy price is {buy_price}')
                method = 'sell'
            else:
                print('Sell order located')
                # Sell order cancelling, completing.
                if current_price < sell_price - gap - gap_ignore:
                    robot.cancel_orders()
                    print('Sell order canceled')
                    orders_count -= 1
                    method = 'sell'
                    # order_into_db(method, 'Order canceled',
                elif sell_price > current_price:
                    orders_count = 0
                    print(f'Sold, current price is {current_price}')
                    method = 'sell'
                    method = 'buy'
                else:
                    print('waiting for sell_price < current_price')

        else:
            if orders_count == 0:
                # Sell order creation.
                sell_price = current_price - gap/2
                robot.trade(instrument_name, amount, sell_price, method)
                print(f'Sell order created, sell price is {sell_price}')
                method = 'buy'
                orders_count += 1
            else:
                print('Buy order located')
                # Buy order cancelling, completing.
                if buy_price > current_price:
                    print(f'Bought, current price is {current_price}')
                    orders_count -= 1
                    method = 'buy'
                    method = 'sell'
                elif current_price > buy_price + gap + gap_ignore:
                    robot.cancel_orders()
                    print('Buy order canceled')
                    method = 'buy'
                    orders_count = 0
                else:
                    print('waiting for buy_price < current_price')


if __name__ == '__main__':
    with open('settings.yaml') as file:
        settings = yaml.full_load(file)
        gap = float(settings['gap'])
        gap_ignore = float(settings['gap_ignore'])
        instrument_name = settings['instrument_name']
        depth = int(settings['depth'])
        amount = int(settings['amount'])

    trade()
