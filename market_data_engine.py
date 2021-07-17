from urllib.request import urlopen
import json
import ssl

connection_point = 'https://query1.finance.yahoo.com/v8/finance/chart/'

# ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def get_ticker_quotes(ticker, interval='1d', time_range='1y'):
    try:
        url_connection = urlopen('{url}{ticker}?interval={ap}&range={time_range}'.format(url=connection_point,
                                                                                         ticker=ticker,
                                                                                         ap=interval,
                                                                                         time_range=time_range))
    except Exception as err:
        print('Connection error: ', err)
        return None
    if url_connection.getcode() == 200:
        market_data = url_connection.read().decode()
        market_data = clean_market_data(market_data)
        return market_data


def clean_market_data(market_data):
    market_data_json = json.loads(market_data)
    quotes = {}
    result_timestamp = market_data_json['chart']['result'][0]['timestamp']
    result_quote = market_data_json['chart']['result'][0]['indicators']['quote'][0]
    index = 0
    for day in result_timestamp[:-1]:
        day = int(day)
        quotes[day] = []
        try:
            quotes[day].append(result_quote['open'][index])
        except IndexError:
            pass
        try:
            quotes[day].append(result_quote['high'][index])
        except IndexError:
            pass
        try:
            quotes[day].append(result_quote['low'][index])
        except IndexError:
            pass
        try:
            quotes[day].append(result_quote['close'][index])
        except IndexError:
            pass
        index += 1
    return quotes
