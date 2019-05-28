import pandas as pd


class CSV2Df:
    def __init__(self):
        pass

    def gen(self,path_csv,sep=','):
        return pd.read_csv(path_csv,sep=sep,index_col='ID')