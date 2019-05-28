from converter import Unievents2CSV
from strategies.distances import Wells
import re
import pandas as pd

if __name__ in '__main__':
    strategies = Unievents2CSV.Unievents2CSV(name_csv='estrategias2')
    df = Wells.Wells(name_csv='estrategias2').df
    df_well_data = df.drop(columns=['cpo','cpl','cpw','cpiw'])
    df_clean = df_well_data.iloc[0,:].loc[df_well_data.iloc[0,:].notnull()]
    vars = list(df_clean.index)

    table_I = []
    table_J = []
    table_K = []
    table_DIRECTION = []
    table_TYPE = []
    for var in vars:
        test = re.search(r'(\w*)_(\w*)',var)
        property = test.group(2)
        well_name = test.group(1)
        value = df_clean[var]
        data_row = [well_name, value]
        if 'I' == property:
            table_I.append(data_row)
        elif 'J' == property:
            table_J.append(data_row)
        elif 'K' == property:
            table_K.append(data_row)
        elif 'DIRECTION' == property:
            table_DIRECTION.append(data_row)
        elif 'TYPE' == property:
            table_TYPE.append(data_row)

    df2 = pd.DataFrame()
    properties = ['I','J','K','DIRECTION','TYPE']
    tables = [table_I,table_J,table_K,table_DIRECTION,table_TYPE]

    for pro,table in zip(properties,tables):
        a = pd.DataFrame(table,columns=['WELL_NAME',pro]).set_index('WELL_NAME')
        df2 = pd.concat((df2,a),axis=1)