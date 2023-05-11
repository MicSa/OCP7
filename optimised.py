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
    for i in range (1,num_shares + 1):
        share_name, share_cost, share_profit = shares[i - 1]
        for j  in range (max_cost + 1):
            if j < share_cost:
                dp[i][j] = dp[i - 1][j]
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i - 1][j - share_cost] + share_profit)
        
        best_profit = dp[-1][-1]
        best_combination = []
        
        i,j = num_shares, max_cost
        
        #boucle while pour trouver la meilleure combinaison
        while i > 0 and j > 0:
            if dp[i][j] != dp[i - 1][j]:
                share_name, share_cost, share_profit = shares[i - 1]
                if dp[i][j] != dp[i - 1][j]:
                    best_combination.append(share_name,share_cost,share_profit))
                    j-= share_cost
                i-=1
            
            return best_combination, best_profit
        
def main():
    shares = read_data("Actions1.csv")
    max_cost = 500
    best_combination, best_profit = knapsack(shares, max_cost)
    
    print(f"Best combination: {best_combination}")
    print(f"Best profit: {best_profit:.2f} euros")

if __name__ == "__main__":
    main()
            
        