import matplotlib.pyplot as plt
import pandas as pd


def plot_graph(name_archivo):
    data = pd.read_excel(name_archivo)
    print(data.columns)
    new_df = data.loc[:, ['retorno', 'volatilidad']]
    new_df.set_index('volatilidad', inplace=True)
    plt.style.use('dark_background')
    plt.plot(new_df)
    plt.xlabel('volatilidad')
    plt.ylabel('retorno')
    plt.show()


def plot(data, name_archivo):

    new_df = data.loc[:, ['retorno', 'volatilidad']]
    new_df.set_index('volatilidad', inplace=True)
    print(new_df)
    plt.style.use('dark_background')
    plt.plot(new_df)
    plt.xlabel('volatilidad')
    plt.ylabel('retorno')
    plt.savefig(name_archivo)
    # plt.show()



if __name__ == '__main__':
    plot_graph('marko_etfs_300.xlsx')
