import xml.etree.ElementTree as ET


class Loadxml:
    def __init__(self,path):
        tree = ET.parse(path)
        self.root = tree.getroot()
