import re
import matplotlib.pyplot as plt


# form link to generated image
def link_to_image(name: str):
    return f'data/ple_images/{name}'


# return path to image
def print_profit_loss(tickers: list, time_period='1y'):
    image_title = ''

    return link_to_image(name=image_title)


# TODO: create set of dates, ask PL for each date and form the result dictionary
def get_ticker_data(ticker: str, time_period: str):

    return {}


# TODO: assemble information for several different tickers
def get_all_data(time_period):
    return {}


if __name__ == '__main__':
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

