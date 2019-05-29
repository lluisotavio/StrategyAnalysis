import InputParams
import re
from converter import Unievents2CSV, Df2CSV
from converter import csv2df
import pandas as pd
from sklearn.metrics.pairwise import pairwise_distances
import time


class Wells:
    def __init__(self, name_csv_input='', path_strategy_csv='', list_unievents=[], regen_csv=False):
        Unievents2CSV.Unievents2CSV(name_csv_input)
        df = csv2df.csv2df('%s%s.csv' % (InputParams.outputfolder,name_csv_input))
        if list_unievents == []:
            list_unievents = list(df.index)
        start = time.time()
        self.array_unievent_df_well_position = self.gen_array_unievent_df_well_position(df, list_unievents)
        end = time.time()
        print((end-start)*1000,'criacao novo df')

    def gen_array_unievent_df_well_position(self, df, list_unievents):
        df_only_well_data = df.drop(columns=['cpo', 'cpl', 'cpw', 'cpiw'])
        array_unievent_df_well_position = []
        for unievent in list_unievents:
            df_only_well_data_clean = df_only_well_data.loc[unievent, :].loc[df_only_well_data.loc[unievent, :].notnull()]
            vars = list(df_only_well_data_clean.index)

            table_I = []
            table_J = []
            table_K = []
            table_DIRECTION = []
            table_TYPE = []
            for var in vars:
                test = re.search(r'(\w*)_(\w*)', var)
                property = test.group(2)
                well_name = test.group(1)
                value = df_only_well_data_clean[var]
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

            df_wells_position = pd.DataFrame()
            properties = ['I', 'J', 'K', 'DIRECTION', 'TYPE']
            tables = [table_I, table_J, table_K, table_DIRECTION, table_TYPE]


            for property, table in zip(properties, tables):
                a = pd.DataFrame(table, columns=['WELL_NAME', property]).set_index('WELL_NAME')
                df_wells_position = pd.concat((df_wells_position, a), axis=1)
            array_unievent_df_well_position.append([unievent,df_wells_position])
        return array_unievent_df_well_position

    def run(self,name_csv):
        array1 = []
        df1 = pd.DataFrame()
        df2 = pd.DataFrame()
        columns = ['UNIEVENT1', 'UNIEVENT2', 'DISTANCE']
        for k in range(len(self.array_unievent_df_well_position)-1):
            name_unievent1 = self.array_unievent_df_well_position[k][0]
            name_unievent2 = self.array_unievent_df_well_position[k+1][0]
            matrix = self.gen_distance_matrix(self.array_unievent_df_well_position[k][1],self.array_unievent_df_well_position[k+1][1])
            print(matrix)
            [n_rows, n_cols] = (len(self.array_unievent_df_well_position[k][0]),len(self.array_unievent_df_well_position[k+1][0]))
            # ########problema eficiencia
            # start = time.time()
            # ijk = []
            # for i in range(n_rows):
            #     df1 = pd.concat((df1, self.array_unievent_df_well_position[k][1].loc[[matrix.index[i]]]), axis=0)
            #     for j in range(n_cols):
            #         distance_wells_unievent1_unievent2 = matrix.iloc[i, j]
            #         array1.append([name_unievent1, name_unievent2, distance_wells_unievent1_unievent2])
            #         ijk.append([i,j,k])
            #         df2 = pd.concat((df2,self.array_unievent_df_well_position[k+1][1].loc[[matrix.columns[j]]]),axis=0)
            #
            # end = time.time()
            # print('tempo gasto iteracao n, com n variando de 1 até numero de estrategias a comparar df estrategia 1 X estrategia 2',(end-start)*1000,'ms')
        df1 = df1.reset_index()
        df2 = df2.reset_index()
        df1.columns = df1.columns + '_UNIEVENT1'
        df2.columns = df2.columns + '_UNIEVENT2'
        df = pd.concat((pd.DataFrame(array1,columns=columns), df1, df2), axis=1)
        Df2CSV.Df2CSV(name_csv, df)
        return(df)

    def gen_distance_matrix(self,unievent1_df_well_position, unievent2_df_well_position):
        ijk_e1 = unievent1_df_well_position[['I', 'J', 'K']].to_numpy()
        ijk_e2 = unievent2_df_well_position[['I', 'J', 'K']].to_numpy()
        matrix_dif = pairwise_distances(ijk_e1, ijk_e2)
        matrix_dif_df = pd.DataFrame(matrix_dif, index=unievent1_df_well_position.index, columns=unievent2_df_well_position.index)
        return matrix_dif_df

    def gen_df_well(self,df):
        pass