import yfinance as yf
from datetime import datetime


# Get array of close prices for stock
def get_close_prices(stock, start_date='2020-01-01'):
    today = datetime.today().strftime('%Y-%m-%d')
    data = yf.download(stock, start_date, today)
    return list(data.to_dict().get('Close').values())


def get_close_price(stock):
    return get_close_prices(stock)[-1]


def get_plvalue(stock):
    current_price = float(get_close_price(stock))
    buying_price, quantity = average_price(stock)
    return quantity * (current_price - float(buying_price))


# TODO: change function for using different data files
def average_price(stock):
    total_number = 0
    total_spending = 0
    with open('data/portfolio.csv', 'r', encoding='UTF-8') as file:
        for line in file.readlines():
            current_stock, date, price, number = line.split(',')
            if current_stock.lower() == stock.lower():
                total_number += int(number)
                total_spending += float(price)
    if total_number > 0:
        return total_spending / total_number, total_number
    else:
        return 0, 0


if __name__ == '__main__':
    print(average_price('aapl'))
    print(get_plvalue('aapl'))
