import persist as ps
import horo_format as hf

path1 = input("Fichier 1 : ")
path2 = input("Fichier 2 : ")

#['Jour','Mois','Annee','Date','Region','Secteur','Niveau','Compagnie','Description']

base = ps.combine_data_csv(path1,path2)
print(base)

H = hf.current_hour()
D = hf.current_date()

pathcsv = 'S:\mix_data_' + D + '_' + H + '_csv.csv'
base.to_csv(pathcsv, sep=';', index=False)

pathexcel = 'S:\mix_data_' + D + '_' + H + '_excel.xlsx'
ps.save_csv_to_excel(pathcsv,pathexcel)

# Récents
#S:\\rekrut_data_04-06-2021_11h32m24s_csv.csv
#S:\employ_data_04-06-2021_11h35m36s_csv.csv

# Anciens
#S:\\rekrut_data_05-26-2021_20h51m53s_csv.csv
#S:\employ_data_05-28-2021_05h13m49s_csv.csv

# Combos anciens nouveaux
#S:\mix_data_03-06-2021_23h29m15s_csv.csv
#S:\mix_data_04-06-2021_02h05m05s_csv.csv