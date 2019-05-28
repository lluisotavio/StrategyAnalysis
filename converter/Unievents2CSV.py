from load import Unievent
import pandas as pd
from converter import Df2CSV
import InputParams
import os
import glob


class Unievents2CSV:
    def __init__(self, name_csv):
        self.df = pd.DataFrame()
        if InputParams.unievents == ['*']:
            list_unievents = glob.glob('%s*.unievent' % InputParams.folder_unievents)
        else:
            list_unievents = ['%s%s.unievent' % (InputParams.folder_unievents, unievent_id)
                              for unievent_id in InputParams.unievents]

        df_unievents = pd.DataFrame()
        loadunievent = Unievent.Unievent()
        for unievent in list_unievents:
            df_unievent = loadunievent.run(unievent)
            df_unievents = pd.concat((df_unievents, df_unievent), axis=0, sort=False)
        df_unievents.index.name = 'ID'
        Df2CSV.Df2CSV(name_csv, df_unievents)

