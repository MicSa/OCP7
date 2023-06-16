from tqdm import tqdm
import csv
import time
import os
from colorama import Fore, Style

# Enregistre le temps au début de l'exécution du script
start_time = time.time()

MAX_INVEST = 500  # Montant maximum à investir

# Fonction pour lire les données du fichier csv
def lire_donnees_csv(filename):
    """Importe les données des actions à partir d'un fichier csv
    Filtre les données corrompues
    """
    with open(filename) as csvfile:
        shares_file = csv.reader(csvfile, delimiter=',')
        next(csvfile)

        liste_actions = []

        for row in shares_file:
            if float(row[1]) <= 0 or float(row[2]) <= 0:
                pass
            else:
                action = (
                    row[0],
                    int(float(row[1])*100),
                    float(float(row[1]) * float(row[2]) / 100)
                )
                liste_actions.append(action)

        return liste_actions


def knapsack(liste_actions):
    max_inv = int(MAX_INVEST * 100)
    total_actions = len(liste_actions)
    cout = []
    profit = []

    for action in liste_actions:
        cout.append(action[1])
        profit.append(action[2])

    ks = [[0 for x in range(max_inv + 1)] for x in range(total_actions + 1)]

    for i in tqdm(range(1, total_actions + 1)):
        for w in range(1, max_inv + 1):
            if cout[i-1] <= w:
                ks[i][w] = max(profit[i-1] + ks[i-1][w-cout[i-1]], ks[i-1][w])
            else:
                ks[i][w] = ks[i-1][w]

    meilleur_combinaison = []

    while max_inv >= 0 and total_actions >= 0:
        if ks[total_actions][max_inv] == \
                ks[total_actions-1][max_inv - cout[total_actions-1]] + profit[total_actions-1]:
            meilleur_combinaison.append(liste_actions[total_actions-1])
            max_inv -= cout[total_actions-1]

        total_actions -= 1

    while max_inv >= 0 and total_actions >= 0:
        if ks[total_actions][max_inv] == \
            ks[total_actions-1][max_inv - cout[total_actions-1]] + profit[total_actions-1]:
            meilleur_combinaison.append(liste_actions[total_actions-1])
            max_inv -= cout[total_actions-1]
        total_actions -= 1

    return meilleur_combinaison, ks[-1][-1]


def afficher_resultats(meilleur_combinaison, meilleur_profit):
    print(Fore.GREEN + f"\nInvestissement le plus rentable ({len(meilleur_combinaison)} actions) :\n" + Style.RESET_ALL)

    cout = []
    profit = []

    # Parcourt chaque action dans la meilleure combinaison et affiche ses détails
    for item in meilleur_combinaison:
        print(Fore.CYAN + f"{item[0]} | {item[1] / 100} € | +{item[2]} €" + Style.RESET_ALL)
        # Ajoute le coût et le profit de l'action aux listes respectives
        cout.append(item[1] / 100)
        profit.append(item[2])

    # Affiche le coût total, le profit total et le temps d'exécution
    print(Fore.GREEN + "\nCoût total : " + Style.RESET_ALL, sum(cout), "€")
    print(Fore.GREEN + "Profit après 2 ans : +" + Style.RESET_ALL, meilleur_profit, "€")
    print(Fore.GREEN + "\nTemps écoulé : " + Style.RESET_ALL, time.time() - start_time, "secondes\n")

def main():
    print("\nVeuillez choisir un dataset à analyser :")
    print("1: dataset1")
    print("2: dataset2")
    user_input = input("Votre choix (1 ou 2): ")

    if user_input == '1':
        filename = "dataset1.csv"
    elif user_input == '2':
        filename = "dataset2.csv"
    else:
        print(Fore.RED + "Choix non valide. Veuillez entrer 1 ou 2." + Style.RESET_ALL)
        return

    if not os.path.exists(filename):
        print(Fore.RED + f"\nLe fichier '{filename}' n'existe pas. Veuillez réessayer.\n" + Style.RESET_ALL)
        time.sleep(1)
        return

    shares_list = lire_donnees_csv(filename)

    print(Fore.GREEN + f"\nTraitement de '{filename}' ({len(shares_list)} actions valides) pour {MAX_INVEST}€ :" + Style.RESET_ALL)
    resultats = knapsack(shares_list)
    afficher_resultats(*resultats)


if __name__ == "__main__":
    main()