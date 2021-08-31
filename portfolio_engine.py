import db_engine as de


def get_close_price(stock):
    """The method returns an array of close prices for specified stock"""
    return de.get_last_close_price(stock)


def get_total_plvalue():
    """The method returns profit/loss value for the whole portfolio"""
    portfolio_dict = de.portfolio_tickers()
    total_pl = 0
    for stock in portfolio_dict:
        total_pl += get_plvalue(stock)
    return total_pl


def get_plvalue(stock):
    """The method returns profit/loss value for a specified stock"""
    current_price = float(get_close_price(stock))
    buying_price, quantity = average_price(stock)
    return quantity * (current_price - float(buying_price))


def average_price(stock):
    """The method returns an average price for a specified symbol"""
    portfolio_dict = read_portfolio()
    if stock in portfolio_dict.keys():
        total_number = portfolio_dict[stock][1]
        total_spending = portfolio_dict[stock][0]
        return total_spending / total_number, total_number
    else:
        return 0, 0


# read the whole portfolio into a dictionary
def read_portfolio():
    """Get all stocks in the portfolio"""
    portfolio_dict = {}
    portfolio = de.db_read_portfolio()
    for line in portfolio:
        current_stock, date, price, number = line
        stock_pn = portfolio_dict.get(current_stock, (0, 0))
        stock_pn = stock_pn[0] + price, stock_pn[1] + int(number)
        portfolio_dict[current_stock] = stock_pn
    return portfolio_dict
