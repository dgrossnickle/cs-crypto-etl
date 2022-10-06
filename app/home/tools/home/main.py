import cbpro
from binance.client import Client
import csv
import datetime
import pandas as pd


def write_results_to_csv(file_name, timestamp, exchange, product, order_type, data):

    usd_value = data['usd_value'].sum()
    size = data['size'].sum()
    mid_price = usd_value / size
    num_orders = len(data)

    my_csv_row = [timestamp, exchange, product, order_type, usd_value, size, mid_price, num_orders]
    print(my_csv_row)
    with open('_results.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(my_csv_row)


def run_coinbase():

    c = cbpro.PublicClient()
    list_products = ['BTC-USD', 'ETH-USD']
    list_order_types = ['bids', 'asks']

    for product in list_products:

        dtmz_start = datetime.datetime.utcnow()
        order_book = c.get_product_order_book(product, level=3)

        for order_type in list_order_types:
            df = pd.DataFrame(order_book[order_type], columns=['price', 'size', 'code'])
            df = df.astype({'price': float, 'size': float, 'code': object})
            df = df.head(200)

            df['usd_value'] = df['price'] * df['size']
            df['cumsum'] = df['usd_value'].cumsum()
            df['abs_100k_var'] = abs(df['cumsum'] - 100000)
            idx_closest_100k = df[['abs_100k_var']].idxmin()['abs_100k_var']
            df = df.head(idx_closest_100k + 1)

            write_results_to_csv(
                file_name='_results.csv',
                timestamp=dtmz_start.strftime('%Y-%m-%d %H:%M:%S'),
                exchange='coinbase',
                product=product,
                order_type=order_type,
                data=df
            )


def run_binance():

    client = Client()
    list_products = ['BTCUSDT', 'ETHUSDT']
    list_order_types = ['bids', 'asks']

    for product in list_products:

        dtmz_start = datetime.datetime.utcnow()
        order_book = client.get_order_book(symbol=product, limit=300)

        for order_type in list_order_types:

            df = pd.DataFrame(order_book[order_type], columns=['price', 'size'])
            df = df.astype({'price': float, 'size': float})

            df['usd_value'] = df['price'] * df['size']
            df['cumsum'] = df['usd_value'].cumsum()
            df['abs_100k_var'] = abs(df['cumsum'] - 100000)
            idx_closest_100k = df[['abs_100k_var']].idxmin()['abs_100k_var']
            df = df.head(idx_closest_100k + 1)

            write_results_to_csv(
                file_name='_results.csv',
                timestamp=dtmz_start.strftime('%Y-%m-%d %H:%M:%S'),
                exchange='binance',
                product=product,
                order_type=order_type,
                data=df
            )