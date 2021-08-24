# Get array of close prices for stock
import db_engine as de


def get_close_price(stock):
    return de.get_last_close_price(stock)


def get_total_plvalue():
    portfolio_dict = de.portfolio_tickers()
    total_pl = 0
    for key in portfolio_dict:
        total_pl += get_plvalue(key)
    return total_pl


def get_plvalue(stock):
    current_price = float(get_close_price(stock))
    buying_price, quantity = average_price(stock)
    return quantity * (current_price - float(buying_price))


def average_price(stock):
    portfolio_dict = read_portfolio()
    if stock in portfolio_dict.keys():
        total_number = portfolio_dict[stock][1]
        total_spending = portfolio_dict[stock][0]
        return total_spending / total_number, total_number
    else:
        return 0, 0


# read the whole portfolio into a dictionary
def read_portfolio():
    portfolio_dict = {}
    portfolio = de.db_read_portfolio()
    for line in portfolio:
        current_stock, date, price, number = line
        stock_pn = portfolio_dict.get(current_stock, (0, 0))
        stock_pn = stock_pn[0] + price, stock_pn[1] + int(number)
        portfolio_dict[current_stock] = stock_pn
    return portfolio_dict
