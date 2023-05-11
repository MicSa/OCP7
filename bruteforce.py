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
def brute_force(shares,max_cost):
    best_profit=0
    best_combination=[]
    
    for i in range (1,len(shares)+1):
        for combination in itertools.combinations(shares,i):
            cost=0
            profit=0
            for share in combination:
                cost+=share[1]
                profit+=share[2]
            if cost<=max_cost and profit>best_profit:
                best_profit=profit
                best_combination=combination
    return best_combination,best_profit

#Fonction Main
def main ():
    shares=read_data('data.csv')
    best_combination,best_profit=brute_force(shares,500)
    print("Meilleur combinaison d'actions : ",best_combination)
    print("Meilleur profit : ",best_profit)

