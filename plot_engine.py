import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import db_engine as de
import portfolio_engine as pe


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
                # pl_data[key] = pl_data.get(key, 0) + current_dict_data[key]
                pl_data[key] += current_dict_data[key]
    else:
        pl_data = get_all_data(time_period)

    # print graph for PL
    dates = list(pl_data.keys())
    values = list(pl_data.values())
    fig, axs = plt.subplots(1, 1, figsize=(15, 5))
    axs.plot(dates, values, label="total")
    axs.set_xlabel('time')
    axs.set_ylabel('profit, $')

    # grid settings
    axs.grid(True)
    fmt_month = mdates.MonthLocator(interval=30)
    ftm_week = mdates.MonthLocator(interval=7)
    axs.xaxis.set_major_locator(fmt_month)
    axs.xaxis.set_minor_locator(ftm_week)
    # Text in the x axis will be displayed in 'YYYY-mm' format.
    # axs.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    fig.autofmt_xdate()
    # plt.savefig(image_path)
    plt.show()
    return image_path


# create set of dates, ask PL for each date and form the result dictionary
def get_ticker_profit_data(ticker: str, time_period: str):
    market_data = de.select_market_data(ticker, time_period)
    average_buy_price, quantity = pe.average_price(ticker)
    pldata = {}
    for row in market_data:
        date = row[0]
        profit = (row[1] - average_buy_price) * quantity
        pldata[date] = profit
    return pldata


# assemble information for several different tickers
def get_all_data(time_period: str):
    symbols_in_portfolio = de.portfolio_tickers()
    pl_data = {}
    for symbol in symbols_in_portfolio:
        current_dict = get_ticker_profit_data(symbol, time_period)
        for key in current_dict.keys():
            pl_data[str(key)] = pl_data.get(str(key), 0) + current_dict[key]
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
    print_profit_loss()
