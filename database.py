import mysql.connector


def order_into_db(method, operation, current_price, amount):
    db = mysql.connector.connect(user='root',
                                 password='root',
                                 host='127.0.0.1',
                                 port='3306')
    cursor = db.cursor()
    insert_request_1 = 'CREATE DATABASE IF NOT EXISTS orders;'
    insert_request_2 = 'USE orders;'
    insert_request_3 = 'CREATE TABLE IF NOT EXISTS orders ('\
                       'method VARCHAR(50),'\
                       'operation VARCHAR(50),'\
                       'current_price FLOAT,'\
                       'amount INT);'
    insert_request_4 = 'INSERT INTO orders (method, operation,'\
                       'current_price, amount)'\
                       'VALUES (%s, %s, %s, %s);'
    cursor.execute(insert_request_1)
    cursor.execute(insert_request_2)
    cursor.execute(insert_request_3)
    cursor.execute(insert_request_4, (str(method), operation,
                                      float(current_price), float(amount)))
    db.commit()
    db.close()
