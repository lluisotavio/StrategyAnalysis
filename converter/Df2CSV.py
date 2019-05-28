import pandas as pd
import InputParams


class Df2CSV:
    def __init__(self, name_csv, df):
        self.name_csv = name_csv
        self.out_put_file = '%s%s.csv' % (InputParams.outputfolder, self.name_csv)
        df.to_csv(self.out_put_file)
