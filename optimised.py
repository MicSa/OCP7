#Version améliorée de bruteforce.py
#Utilisation de la librairie itertools pour générer les combinaisons
#Utilisation de la librairie time pour calculer le temps d'exécution

import csv

#Fonction de lecture des données
def read_data(file_path):
    with open(file_path, 'r') as file:
        data = list(csv.reader(file))
    shares = []
    for row in data[1:]:
        shares.append((row[0], int(row[1]), float(row[2].strip('%')) / 100))
    return shares

#Fonction de calcul de la meilleure combinaison
#Implémentation de l'algorithme de sac à dos (knapsack)
def knapsack(shares, max_cost):
    num_shares = len(shares)
    dp = [[0] * (max_cost + 1) for _ in range(num_shares + 1)]
    #Mise en place de la boucle 
    