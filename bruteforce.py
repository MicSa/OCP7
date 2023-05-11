import itertools
import csv

def read_data(file_path):
    """
    Cette fonction lit le fichier CSV à partir du chemin donné et 
    renvoie une liste de tuples contenant le nom, le coût et le profit de chaque action.

    :param file_path: str, chemin du fichier CSV à lire.
    :return: list, liste de tuples contenant le nom, le coût et le profit de chaque action.
    """
    with open(file_path, 'r') as file:
        data = list(csv.reader(file)) # lecture du fichier CSV

    shares = [] # initialiser une liste vide pour stocker les actions

    # itérer sur chaque ligne dans les données (en excluant la première ligne)
    for row in data[1:]:
        # ajouter un tuple contenant le nom, le coût et le profit de l'action à la liste des actions
        shares.append((row[0], int(row[1]), float(row[2].strip('%')) / 100))

    return shares

def brute_force(shares, max_cost):
    """
    Cette fonction utilise une approche de force brute pour trouver la meilleure combinaison d'actions 
    qui maximise le profit tout en respectant le coût maximal.

    :param shares: list, liste de tuples contenant le nom, le coût et le profit de chaque action.
    :param max_cost: int, coût maximal autorisé.
    :return: tuple, meilleure combinaison d'actions et profit correspondant.
    """
    best_profit = 0 # initialiser le meilleur profit à 0
    best_combination = [] # initialiser la meilleure combinaison à une liste vide

    # itérer sur chaque nombre possible d'actions à acheter
    for i in range(1, len(shares) + 1):
        # itérer sur chaque combinaison possible d'actions
        for combination in itertools.combinations(shares, i):
            cost = sum([share[1] for share in combination]) # calculer le coût de la combinaison
            profit = sum([share[1] * share[2] for share in combination]) # calculer le profit de la combinaison

            # si le coût de la combinaison est inférieur ou égal au coût maximal et que le profit est supérieur au meilleur profit
            if cost <= max_cost and profit > best_profit:
                best_profit = profit # mettre à jour le meilleur profit
                best_combination = combination # mettre à jour la meilleure combinaison

    return best_combination, best_profit

def main():
    """
    Cette fonction est le point d'entrée du programme. Elle lit les données, trouve la meilleure combinaison d'actions 
    et affiche les résultats.
    """
    shares = read_data("Actions1.csv") # lire les données
    max_cost = 500 # définir le coût maximal
    best_combination, best_profit = brute_force(shares, max_cost) # trouver la meilleure combinaison d'actions

    # imprimer la meilleure combinaison et le meilleur profit
    print(f"Best combination: {best_combination}")
    print(f"Best profit: {best_profit:.2f} euros")

if __name__ == "__main__":
    # exécuter la fonction principale si le script est exécuté en tant que programme principal
    main()
