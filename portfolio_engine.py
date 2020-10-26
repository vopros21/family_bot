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
    current_price = int(get_close_price(stock))
    buying_price, quantity = average_price(stock)
    return quantity * (current_price - float(buying_price))


def average_price(stock):
    with open('data/portfolio.csv', 'r', encoding='UTF-8') as file:
        for line in file.readlines():
            current_stock, date, price, number = line.split(',')
            total_number = 0
            total_spending = 0
            if current_stock.lower() == stock.lower():
                total_number += int(number)
                total_spending += float(price)
    return total_spending / total_number, total_number


def newone():
    pass
#     close_prices = get_close_prices('AAPL', '2020-10-09')
#     print(close_prices)
#     print(f"Profit/Loss value: {get_plvalue('AAPL', 116.03, 1, '2020-10-09')}")


if __name__ == '__main__':
    # newone()
    print(average_price('aapl'))
    print(get_plvalue('aapl'))
