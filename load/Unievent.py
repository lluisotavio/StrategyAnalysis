
from structures import Well, Platform
from Params import ParseUnieventParams
from load import xml
import os
import pandas as pd


class Unievent:
    def __init__(self):
        pass

    @staticmethod
    def generate_wells(root):
        wells = []
        for event in root.findall(ParseUnieventParams.param_parse_drillings):
            well_aux = Well.Well()
            well_aux.name = event.attrib.get(ParseUnieventParams.param_parse_drilling_well_names)
            well_aux.dict_feats.update({'%s_I' % well_aux.name: [event.find(ParseUnieventParams.param_parse_geometry)
                                       .attrib[ParseUnieventParams.param_parse_i_pos]]})
            well_aux.dict_feats.update({'%s_J' % well_aux.name: [event.find(ParseUnieventParams.param_parse_geometry)
                                       .attrib[ParseUnieventParams.param_parse_j_pos]]})
            well_aux.dict_feats.update({'%s_K' % well_aux.name: [event.find(ParseUnieventParams.param_parse_geometry)
                                       .attrib[ParseUnieventParams.param_parse_k_pos]]})
            well_aux.dict_feats.update({'%s_DIRECTION' % well_aux.name: [event.find(ParseUnieventParams.
                                        param_parse_geometry).attrib[ParseUnieventParams.param_parse_direction]]})
            well_aux.dict_feats.update({'%s_TYPE' % well_aux.name: [root.find(ParseUnieventParams.
                                        param_parse_type % well_aux.name).attrib['type']]})
            wells.append(well_aux)
        return wells

    @staticmethod
    def generate_plat(root):
        plat = Platform.Platform()
        plat.dict_feats.update({'cpo': [float(root.find(ParseUnieventParams.param_parse_plat_qo)
                                              .attrib['value'])]})
        plat.dict_feats.update({'cpl': [float(root.find(ParseUnieventParams.param_parse_plat_ql)
                                              .attrib['value'])]})
        plat.dict_feats.update({'cpw': [float(root.find(ParseUnieventParams.param_parse_plat_qw)
                                              .attrib['value'])]})
        plat.dict_feats.update({'cpiw': [float(root.find(ParseUnieventParams.param_parse_plat_qi)
                                               .attrib['value'])]})
        return plat

    @staticmethod
    def generate_df(wells, plat, id):
        df_aux = pd.DataFrame()
        for well in wells:
            df_aux = pd.concat((df_aux, pd.DataFrame.from_dict(well.dict_feats)), axis=1)
        df_aux = pd.concat((df_aux, pd.DataFrame.from_dict(plat.dict_feats)), axis=1)
        df_aux.index = [id]
        return df_aux

    def run(self, unievent_path):
        try:
            root = xml.Loadxml(unievent_path).root
            id = os.path.splitext(os.path.basename(unievent_path))[0]
            wells = self.generate_wells(root=root)
            plat = self.generate_plat(root=root)
            df = self.generate_df(wells, plat, id)
        except:
            print('%s corrompido ou não existente' % unievent_path)
            df = pd.DataFrame()
        return df
