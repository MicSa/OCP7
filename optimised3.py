# Backtesting sur le fichier de données de Sienna
""" l'algorithme du sac à dos est un exemple de problème de programmation dynamique qui ne peut pas être résolu 
avec des valeurs continues (c'est-à-dire des nombres à virgule flottante).
Pour résoudre ce problème, on va multiplier toutes les valeurs de coût par 100 pour convertir les centimes en euros.
Puis on va arrondir à l'entier le plus proche. 
Cette approche a l'avantage de préserver la précision tout en permettant à l'algorithme du sac à dos de fonctionner correctement.

Une fois les données transformées, on va utiliser la même fonction `knapsack` pour trouver la meilleure combinaison d'actions. """

import time
import csv

def read_sienna_data(file_path):
    """
    Cette fonction lit les données de trading de Sienna à partir du fichier csv.
    :param file_path: Le chemin vers le fichier csv.
    :return: Une liste de tuples représentant les transactions de Sienna.
    Chaque tuple contient le nom de l'action, son coût et son profit.
    """
    with open(file_path, 'r') as file:
        data = list(csv.reader(file))
    transactions = []
    for row in data[1:]:
        transactions.append((row[0], int(float(row[1]) * 100), float(row[2].strip('%')) / 100))
    return transactions

def calculate_profit(transactions):
    """
    Cette fonction calcule le profit total à partir d'une liste de transactions.
    :param transactions: Une liste de tuples représentant les transactions.
    Chaque tuple contient le nom de l'action, son coût et son profit.
    :return: Le profit total.
    """
    total_profit = 0
    for name, cost, profit in transactions:
        total_profit += cost * profit
    return total_profit




def knapsack(shares, max_cost):
    """
    Cette fonction met en œuvre l'algorithme du sac à dos pour trouver la meilleure combinaison d'actions.
    :param shares: Une liste de tuples représentant les actions.
    :param max_cost: Le coût maximum qui peut être dépensé pour les actions.
    :return: La meilleure combinaison d'actions et le profit maximum.
    """
    num_shares = len(shares)
    # Initialisation du tableau de programmation dynamique.
    dp = [[0] * (max_cost + 1) for _ in range(num_shares + 1)]

    # Remplissage du tableau de programmation dynamique.
    for i in range(1, num_shares + 1):
        share_name, share_cost, share_profit = shares[i - 1]
    for j in range(max_cost + 1):
        if j < share_cost:
            dp[i][j] = dp[i - 1][j]
        else:
            # Use int(share_cost) instead of share_cost.
            dp[i][j] = max(dp[i - 1][j], dp[i - 1][j - int(share_cost)] + share_cost * share_profit)


    # Le profit maximum se trouve dans le coin inférieur droit du tableau.
    best_profit = dp[-1][-1]
    best_combination = []

    # Recherche de la meilleure combinaison d'actions.
    i, j = num_shares, max_cost
    while i > 0 and j > 0:
        share_name, share_cost, share_profit = shares[i - 1]
        if dp[i][j] != dp[i - 1][j]:
            best_combination.append((share_name, share_cost, share_profit))
            j -= share_cost
        i -= 1


    return best_combination, best_profit

def main():
    """
    Il s'agit de la fonction principale. Elle lit les données, appelle la fonction Knapsack, 
    lit les transactions de Sienna, calcule les profits et imprime les résultats.
    """
    shares = read_sienna_data("dataset1_Python+P7.csv")
    max_cost = 500 * 100
    best_combination, _ = knapsack(shares, max_cost)
    sienna_transactions = read_sienna_data("solution2_Python+P7.txt")

    algorithm_profit = calculate_profit(best_combination)
    sienna_profit = calculate_profit(sienna_transactions)
    
    print(f"Profit de l'algorithme : {algorithm_profit / 100:.2f} euros")
    print(f"Profit de Sienna : {sienna_profit / 100:.2f} euros")

if __name__ == "__main__":
    main()

