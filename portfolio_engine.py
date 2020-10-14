import yfinance as yf
from datetime import datetime


# Get array of close prices for stock
def get_close_prices(stock, start_date):
    today = datetime.today().strftime('%Y-%m-%d')
    data = yf.download(stock, start_date, today)
    return list(data.to_dict().get('Close').values())


# Get profit / loss value for a portfolio position
def get_plvalue(stock, price, number, start_date):
    close_prices = get_close_prices(stock, start_date)
    return number * (close_prices[-1] - price)


def newone():
    close_prices = get_close_prices('AAPL', '2020-10-09')
    print(close_prices)
    print(f"Profit/Loss value: {get_plvalue('AAPL', 116.03, 1, '2020-10-09')}")


if __name__ == '__main__':
    newone()
