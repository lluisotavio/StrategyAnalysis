import InputParams
from converter import Unievents2CSV
from converter import CSV2Df

class Wells:
    def __init__(self, name_csv='', path_strategy_csv='', list_unievents=[], regen_csv=False):


        Unievents2CSV.Unievents2CSV(name_csv)
        csv2df = CSV2Df.CSV2Df()
        path_strategy_csv = '%s%s.csv' % (InputParams.outputfolder,name_csv)
        df = csv2df.gen(path_strategy_csv)

        self.df = df