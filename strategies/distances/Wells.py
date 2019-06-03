import InputParams
import re
from converter import Unievents2CSV, Df2CSV
from converter import csv2df, Df2CSV
import pandas as pd
from sklearn.metrics.pairwise import pairwise_distances
import time
import numpy as np


class Wells:
    def __init__(self, name_csv_input='', path_strategies_csv='', list_unievents=[], regen_csv=False):
        start = time.time()
        if path_strategies_csv != '':
            df = csv2df.csv2df('%s' % path_strategies_csv)
            print('1 %s' % ((time.time() - start) * 1000))
        else:
            Unievents2CSV.Unievents2CSV(name_csv_input)
            start = time.time()
            df = csv2df.csv2df('%s%s.csv' % (InputParams.outputfolder, name_csv_input))
            print('2 %s' % ((time.time() - start) * 1000))
        if not list_unievents:
            list_unievents = list(df.index)
        self.array_unievent_df_well_position = self.gen_array_unievent_df_well_position(df, list_unievents)
        self.array_unievent12_type_matrixdist = []

    @staticmethod
    def gen_array_unievent_df_well_position(df, list_unievents):
        df_only_well_data = df.drop(columns=['cpo', 'cpl', 'cpw', 'cpiw'])
        array_unievent_df_well_position = []
        for unievent in list_unievents:
            df_only_well_data_clean = df_only_well_data.loc[unievent, :].loc[
                df_only_well_data.loc[unievent, :].notnull()]
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
            array_unievent_df_well_position.append([unievent, df_wells_position])
        return array_unievent_df_well_position

    def run(self, name_csv, type):
        final_list = []
        for i in range(len(self.array_unievent_df_well_position)):
            unievent1, df1 = [self.array_unievent_df_well_position[i][0]], self.array_unievent_df_well_position[i][1][
                self.array_unievent_df_well_position[i][1]['TYPE'] == type]
            df1_np = np.array(df1)
            wells_names_df1 = df1.index
            for j in range(i + 1, len(self.array_unievent_df_well_position)):
                unievent2, df2 = [self.array_unievent_df_well_position[j][0]], \
                                 self.array_unievent_df_well_position[j][1][
                                     self.array_unievent_df_well_position[j][1]['TYPE'] == type]
                df2_np = np.array(df2)
                wells_names_df2 = df2.index
                matrix_dist = self.gen_distance_matrix(df1, df2)
                self.array_unievent12_type_matrixdist.append([unievent1[0], unievent2[0], type,
                                                              pd.DataFrame(matrix_dist, index=wells_names_df1,
                                                                           columns=wells_names_df2)])
                for x in range((df1_np.shape[0])):
                    well1_prop = df1_np[x, :]
                    for y in range((df2_np.shape[0])):
                        well2_prop = df2_np[y, :]
                        name_well1 = [wells_names_df1[x]]
                        name_well2 = [wells_names_df2[y]]
                        final_list.append(unievent1 + name_well1 + list(well1_prop) + unievent2 + name_well2 + list(
                            well2_prop) + list([matrix_dist[x, y]]))
        columns = ['STRATEGY_1', 'WELL_1', 'I_1', 'J_1', 'K_1', 'DIRECTION_1', 'TYPE_1', 'STRATEGY_2', 'WELL_2', 'I_2',
                   'J_2', 'K_2', 'DIRECTION_2', 'TYPE_2', 'DIST']
        df = pd.DataFrame(np.array(final_list), columns=columns)
        Df2CSV.Df2CSV(name_csv, df)
        return df

    @staticmethod
    def gen_distance_matrix(unievent1_df_well_position, unievent2_df_well_position):
        ijk_e1 = unievent1_df_well_position[['I', 'J', 'K']].to_numpy()
        ijk_e2 = unievent2_df_well_position[['I', 'J', 'K']].to_numpy()
        matrix_dif = pairwise_distances(ijk_e1, ijk_e2)
        return matrix_dif

    def gen_df_well(self, df):
        pass
