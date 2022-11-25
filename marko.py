import pandas as pd
import numpy as np
import tqdm


def retornos(data):

    retornos = pd.DataFrame(np.log((data/data.shift(1))))

    return retornos


def calc_proportions(tickers, max=0.4, min=0.05):

    finish = False
    while not finish:

        pond = np.array(np.random.random(len(tickers)))
        pond = pond / np.sum(pond)

        if not pond.max() > max and not pond.min() < min:
            return pond


def get_activos_pond_sorted(activos, pond):
    zipped = zip(activos, pond)
    zipped_list = list(zipped)
    zipped_list.sort(key=lambda tup: tup[1], reverse=True)
    zipped_list = list(zip(*zipped_list))

    activos = list(zipped_list[0])
    pond = list(zipped_list[1])

    return activos, pond


def markowitz(data, anual, max=False, min=False, q=1500):

    resultados = []

    # data = retornos(data)
    # data.dropna(inplace=True)
    data = pd.DataFrame(np.log((data/data.shift(1)))).dropna()

    tickers = list(data.columns)

    print(tickers)

    for i in tqdm.tqdm(range(q)):
        pond = calc_proportions(tickers=tickers, max=max, min=min)

        tickers_sort, pond_sort = get_activos_pond_sorted(activos=tickers, pond=pond)

        r = {}
        r['activos'] = tickers_sort
        r['pesos'] = np.round(pond_sort, 3)
        r['retorno'] = np.sum((data.mean() * pond * anual))
        r['volatilidad'] = np.sqrt(np.dot(pond, np.dot(data.cov() * anual, pond)))
        r['sharpe'] = r['retorno'] / r['volatilidad']
        resultados.append(r)

    porfolios = pd.DataFrame(resultados).sort_values("sharpe", ascending=False)
    # porfolios = porfolios.iloc[0:10000]

    return porfolios


if __name__ == '__main__':
    tickers = ['SPY', 'QQQ', 'DIA', 'XLF', 'XLE', 'EWZ']
    calc_proportions(tickers=tickers)

    pass


