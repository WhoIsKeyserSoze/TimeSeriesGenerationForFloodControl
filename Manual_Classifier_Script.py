# L for linear 
# R for reccurent patern
# F for flood
# N no pattern

import pandas
import matplotlib.pyplot as plt
import os

classified_data_path = "D:\Desktop\Prog\L3\BE\ClassifiedData"
unclassified_data_path = "D:\Desktop\Prog\L3\BE\SomeData"

# Parcourir la liste des fichier
for file in os.listdir(unclassified_data_path):
    if file.endswith(".csv"):

        # Afficher le graph
        df = pandas.read_csv(unclassified_data_path + '\\' + file)
        fig, ax = plt.subplots()

        df.plot(kind='line', x='date', y='height', ax=ax)
        fig.tight_layout()
        plt.show()

        #Affiche les infos nom / sensor name / date

        # recup l'input
        res = input()

        if(res == 'l'):
            res = 'L'
        if(res == 'n'):
            res = 'N'
        if(res == 'r'):
            res = 'R'
        if(res == 'f'):
            res = 'F'

        # rewrite le fichier dans /classifiedData
        filename = file[:-4] +'_'+ res
        df.to_csv(classified_data_path+ '\\' +filename+ '.csv', index=False)
