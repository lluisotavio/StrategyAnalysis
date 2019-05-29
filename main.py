from converter import Unievents2CSV
from strategies.distances import Wells
import time
import glob


if __name__ in '__main__':
    #strategies = Unievents2CSV.Unievents2CSV(name_csv='estrategias_UNISIM-I')
    wells_dif = Wells.Wells('estrategias_UNISIM-II',list_unievents=[])
    df = wells_dif.run('distancia_pocos')