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
        shares.append((row[0], int(row[1]), float(row[2].strip('%')) / 100))
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
                # Choix du profit maximum entre ne pas acheter l'action actuelle et l'acheter.
                dp[i][j] = max(dp[i - 1][j], dp[i - 1][j - share_cost] + share_cost * share_profit)

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
    C'est la fonction principale. Elle lit les données, appelle la fonction Knapsack et affiche les résultats.
    """
    #On commence à mesure le temps que ça prend
    start_time = time.time()
    shares = read_data("Actions1.csv")
    max_cost = 500
    best_combination, best_profit = knapsack(shares, max_cost)
    
    print(f"Best combination: {best_combination}")
    print(f"Best profit: {best_profit:.2f} euros")
    # On arrête la mesure du temps et on regarde la différence
    end_time = time.time()  # On arrête de mesurer le temps
    print(f"Execution time: {end_time - start_time:.2f} seconds")  # On imprime le temps d'exécution

if __name__ == "__main__":
    main()
