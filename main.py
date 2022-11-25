import pandas as pd
import time

import data_apis
import marko
import grafico


def run(descargar_data, tickers_crypto, tickers_etfs, max_crypto, min_crypto, max_etfs, min_etfs, q_crypto, q_etfs):

    start_time = time.time()

    if descargar_data:
        # CRYPTO
        data_crypto = data_apis.data_crypto(tickers=tickers_crypto)
        data_crypto.to_pickle('data_crypto')

        # ETFS
        data_etfs = data_apis.data_etfs(tickers=tickers_etfs, years_data=10)
        data_etfs.to_pickle('data_etfs')

    else:
        data_crypto = pd.read_pickle('data_crypto')
        data_etfs = pd.read_pickle('data_etfs')

    marko_crypto = marko.markowitz(data=data_crypto, anual=365, max=max_crypto, min=min_crypto, q=q_crypto)
    marko_crypto.to_excel('marko_cypto.xlsx')
    print(marko_crypto.head(20))
    grafico.plot(marko_crypto, name_archivo='plot_crypto.jpg')

    marko_etfs = marko.markowitz(data=data_etfs, anual=252, max=max_etfs, min=min_etfs, q=q_etfs)
    marko_etfs.to_excel('marko_etfs.xlsx')
    print(marko_etfs.head(20))
    grafico.plot(marko_etfs, name_archivo='plot_etfs.jpg')

    print(time.time() - start_time)


if __name__ == '__main__':
    tickers_crypto = ['bitcoin', 'ethereum']
    tickers_etfs = ['SPY', 'QQQ', 'DIA', 'XLF', 'XLE', 'EWZ']

    run(
        descargar_data=True,
        tickers_crypto=tickers_crypto,
        tickers_etfs=tickers_etfs,
        max_crypto=0.9, min_crypto=0.1, max_etfs=0.7, min_etfs=0.01, q_crypto=1500, q_etfs=10000)
