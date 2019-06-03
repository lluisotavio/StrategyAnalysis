from strategies.distances import Wells
import InputParams
from converter import csv2df, Unievents2CSV
import time
from scipy.optimize import linear_sum_assignment

class PairedWells:
    def __init__(self,name_csv_input='', path_strategies_csv='', list_unievents=[], regen_csv=False):
        self.name_csv_input = name_csv_input
        self.path_strategies_csv = path_strategies_csv
        self.list_unievents = list_unievents
        self.regen_csv = regen_csv

    def run(self):
        wells = Wells.Wells( self.name_csv_input, self.path_strategies_csv, self.list_unievents, self.regen_csv)
        wells.run()
        array_unievent_df_well_position = wells.array_unievent_df_well_position
        array_unievent12_type_matrixdist =  wells.array_unievent12_type_matrixdist
        for unievent12_type_matrixdist in array_unievent12_type_matrixdist:

            row_ind, col_ind = linear_sum_assignment(unievent12_type_matrixdist[3])

            dist = unievent12_type_matrixdist[row_ind, col_ind].sum()
            self.matriz_somatorio_distancia[3][i, j] = "{:10.4f}".format(dist)
            self.matriz_somatorio_distancia[3][j, i] = "{:10.4f}".format(dist)

if __name__ == '__main__':
    paired = PairedWells(path_strategies_csv='./outputfolder/estrategias_UNISIM-II.csv', list_unievents=['01_0001', '01_0002', '01_0003', '01_0004', '01_0005', '01_0006', '01_0007'])
    paired.run()