import yfinance as yf
import datetime as dt
import time
import pandas as pd
import requests


def coingecko_data(ticker, f, t):

    url = 'https://api.coingecko.com/api/v3'

    data = f'/coins/{ticker}/market_chart/range?vs_currency=usd&from={f}&to={t}'
    r = requests.get(url+data)
    js = r.json()

    return js


def df_crypto(ticker, f, t):

    try:

        data = coingecko_data(ticker=ticker, f=f, t=t)['prices']
        data = pd.DataFrame(data)
        data.rename({0: 'date', 1: ticker}, axis=1, inplace=True)
        data['date'] = pd.to_datetime(data['date'], unit='ms')
        data.set_index('date', inplace=True)

    except:
        data = pd.DataFrame()

    return data


def data_crypto(tickers, years_data=7):

    start = (dt.datetime.today() - dt.timedelta(days=365*years_data)).date()
    end = dt.datetime.today().date()
    start_timestamp = int(time.mktime(start.timetuple()))
    end_timestamp = int(time.mktime(end.timetuple()))
    dfs = []

    for ticker in tickers:

        data = df_crypto(ticker=ticker, f=start_timestamp, t=end_timestamp)

        print(f'Descargando data {ticker}')

        if data.empty:
            print(f'Error con ticker {ticker}')
            continue

        dfs.append(data)

    data_all = pd.concat(dfs, axis=1)

    return data_all


def yfinance_data(ticker, interval='1d', years_data=7):

    """
    DATES EXAMPLE = '2022-10-06'
    """

    try:

        start = dt.datetime.today() - dt.timedelta(365*years_data)
        start = start.strftime('%Y-%m-%d')

        end = dt.datetime.today() + dt.timedelta(1)
        end = end.strftime('%Y-%m-%d')

        data = yf.download(tickers=ticker, interval=interval, auto_adjust=True, start=start, end=end)

        data.index = pd.to_datetime(data.index)
        data = data.tz_localize(None)

    except:
        data = pd.DataFrame()

    return data


def data_etfs(tickers, interval='1d', years_data=7):

    dfs = []
    for ticker in tickers:

        print(f'Descargando data {ticker}')

        data = yfinance_data(ticker=ticker, interval=interval, years_data=years_data)

        if data.empty:
            print(f'Error con ticker {ticker}')
            continue

        data_filter = pd.DataFrame()
        data_filter[ticker] = data['Close']

        dfs.append(data_filter)

    data_all = pd.concat(dfs, axis=1)

    return data_all


if __name__ == '__main__':
    # CRYPTO
    # tickers = ['bitcoin', 'ethereum']
    # data = data_crypto(tickers=tickers)
    # data.to_pickle('data_crypto')

    # ETFS
    # tickers_etf = ['SPY', 'QQQ', 'DIA', 'XLF', 'XLE', 'EWZ']
    # data = data_etfs(tickers=tickers_etf, years_data=10)
    # data.to_pickle('data_etfs')
    data = yfinance_data(ticker='BTC-USD', years_data=1)
    # print(data)
    n=20
    data['wma'] = data['Close'].rolling(n).apply(lambda x: x[::-1].cumsum().sum() * 2 / n / (n + 1))
    print(data.tail(20))

