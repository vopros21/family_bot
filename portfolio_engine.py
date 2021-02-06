import yfinance as yf
from datetime import datetime


# Get array of close prices for stock
def get_close_prices(stock, start_date='2020-01-01'):
    today = datetime.today().strftime('%Y-%m-%d')
    data = yf.download(stock, start_date, today)
    return list(data.to_dict().get('Close').values())


def get_close_price(stock):
    return get_close_prices(stock)[-1]


# TODO: add function for getting profit/loss for all stock in the portfolio
def get_total_plvalue():
    pass


def get_plvalue(stock):
    current_price = float(get_close_price(stock))
    buying_price, quantity = average_price(stock)
    return quantity * (current_price - float(buying_price))


def average_price(stock, filename='portfolio.csv'):
    portfolio_dict = read_portfolio(filename)
    if stock in portfolio_dict.keys():
        total_number = portfolio_dict[stock][1]
        total_spending = portfolio_dict[stock][0]
        return total_spending / total_number, total_number
    else:
        return 0, 0


# read the whole portfolio into a dictionary
def read_portfolio(filename):
    portfolio_dict = {}
    with open(f'data/{filename}', 'r', encoding='UTF-8') as file:
        for line in file.readlines():
            current_stock, date, price, number = line.split(',')
            stock_pn = portfolio_dict.get(current_stock, (0, 0))
            stock_pn = stock_pn[0] + float(price), stock_pn[1] + int(number)
            portfolio_dict[current_stock] = stock_pn
    return portfolio_dict


if __name__ == '__main__':
    print(average_price('aapl'))
    print(get_plvalue('aapl'))
