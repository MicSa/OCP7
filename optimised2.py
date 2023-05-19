# Modification pour prise en charge des centimes d'euros
""" l'algorithme du sac à dos est un exemple de problème de programmation dynamique qui ne peut pas être résolu 
avec des valeurs continues (c'est-à-dire des nombres à virgule flottante).
Pour résoudre ce problème, on va multiplier toutes les valeurs de coût par 100 pour convertir les centimes en euros.
Puis on va arrondir à l'entier le plus proche. 
Cette approche a l'avantage de préserver la précision tout en permettant à l'algorithme du sac à dos de fonctionner correctement.

Une fois les données transformées, on va utiliser la même fonction `knapsack` pour trouver la meilleure combinaison d'actions. """

import time
import csv

def read_data(file_path):
    """
    Cette fonction lit les données du fichier csv.
    :param file_path: Le chemin vers le fichier csv.
    :return: Une liste de tuples représentant les actions.
    Chaque tuple contient le nom de l'action, son coût et son profit.
    """
    with open(file_path, 'r') as file:
        data = list(csv.reader(file))
    shares = []
    for row in data[1:]:
        # Multiply the share cost by 100 to convert it to cents.
        shares.append((row[0], int(float(row[1]) * 100), float(row[2].strip('%')) / 100))
    return shares




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
    C'est la fonction principale. Elle lit les données, appelle la fonction Knapsack et imprime les résultats.
    """
    shares = read_data("dataset1_Python+P7.csv")
    max_cost = 500 * 100  # Conversion du max en centimes.
    best_combination, best_profit = knapsack(shares, max_cost)
    
    # En affichant la meilleure combinaison, on convertit en euros les coûts et les profits.
    best_combination = [(name, cost / 100, profit) for name, cost, profit in best_combination]
    print(f"Best combination: {best_combination}")
    print(f"Best profit: {best_profit / 100:.2f} euros")  # Cette ligne est dans la fonction main pour ne pas avoir best_profit undefined

if __name__ == "__main__":
    main()

