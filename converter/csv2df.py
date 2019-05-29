import pandas as pd


def csv2df(path_csv, sep=','):
        return pd.read_csv(path_csv, sep=sep, index_col='ID')
