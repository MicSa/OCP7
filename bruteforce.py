#Programem Python
#Algorithme 
#Chaque action ne peut être achetée qu'une seule fois.
#Ne pas acheter une fraction d'action.
#Dépenser au maximum 500 euros par client.

#Importation des modules 
import itertools
import csv

#Définition des fonctions 

#Fonction pour lire un fichier de données csv
def read_data(file_path):
    with open(file_path, 'r') as file:
        data = list(csv.reader(file))
    shares = []
    for row in data[1:]:
        shares.append((row[0], int(row[1]), float(row[2].strip('%')) / 100))
    return shares
#Fonction algorithmique pour répondre au problème

#Fonction Main

