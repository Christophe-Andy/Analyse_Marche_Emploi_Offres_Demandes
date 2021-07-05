import pandas as pd
import horo_format as hf
from PIL._imaging import display


def save_csv_to_excel(path_csv,path_excel):
    base = pd.read_csv(path_csv, sep=";")
    if any(base):
        base.to_excel(path_excel, index=False, header=True)
    else :
        print("Erreur lors de l'enregistrement sous format EXCEL !")

def import_csv_to_dataframe(path_csv):
    base = pd.read_csv(path_csv, sep=";")
    return base

def combine_data_csv(path_csv1,path_csv2):
    base1 = import_csv_to_dataframe(path_csv1)
    base2 = import_csv_to_dataframe(path_csv2)

    base = pd.merge(base1, base2, how='outer',left_index=False,right_index=False)

    return base