import re
import matplotlib.pyplot as plt
import datetime
import db_engine as de


# form link to generated image
def link_to_image(name: str):
    return f'data/ple_images/{name}'


# return path to image
def print_profit_loss(tickers=(), time_period='1y'):
    today = int(datetime.datetime.now().timestamp() // 100 * 100)
    image_title = f'graph_{today}.png'
    image_path = link_to_image(image_title)
    pl_data = {}
    if len(tickers) > 0:
        for ticker in tickers:
            current_dict_data = get_ticker_profit_data(ticker, time_period)
            for key in current_dict_data.keys():
                pl_data[key] = pl_data.get(key, 0) + current_dict_data[key]
    else:
        pl_data = get_all_data(time_period)

    # print graph for PL
    dates = list(pl_data.keys())
    values = list(pl_data.values())
    fig, axs = plt.subplots(1, 1, figsize=(3, 3))
    axs.bar(dates, values)
    plt.savefig(image_path)
    return image_path


# TODO: create set of dates, ask PL for each date and form the result dictionary
def get_ticker_profit_data(ticker: str, time_period: str):
    market_data = de.select_market_data(ticker, time_period)
    buy_prices = de.get_buy_prices(ticker)
    pldata = {}
    for row in market_data:

    return pldata


# assemble information for several different tickers
def get_all_data(time_period: str):
    symbols_in_portfolio = de.portfolio_tickers()
    pl_data = {}
    for symbol in symbols_in_portfolio:
        current_dict = get_ticker_profit_data(symbol, time_period)
        for key in current_dict.keys():
            pl_data[key] = pl_data.get(key, 0) + current_dict[key]
    return pl_data


def sample():
    data = {'apple': 10, 'orange': 15, 'lemon': 5, 'lime': 20}
    names = list(data.keys())
    values = list(data.values())

    fig, axs = plt.subplots(1, 1, figsize=(3, 3))
    axs.bar(names, values)
    # axs[1].scatter(names, values)
    # axs[2].plot(names, values)
    fig.suptitle('Categorical Plotting')
    # plt.show()
    plt.savefig('data/ple_images/graph.png')


if __name__ == '__main__':
    # print(print_profit_loss())
    pass
