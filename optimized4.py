from tqdm import tqdm
import csv
import time
import os

start_time = time.time()

MAX_INVEST = 500  # Montant maximum à investir

def lire_donnees_csv(filename):
    """Importe les données des actions à partir d'un fichier csv
    Filtre les données corrompues

    @return: données des actions (liste)
    """
    with open(filename) as csvfile:
        shares_file = csv.reader(csvfile, delimiter=',')
        next(csvfile)       # saute la première ligne

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
    """Initialise la matrice (ks) pour le problème du sac à dos 0-1
     Obtient la meilleure combinaison d'actions

     @param liste_actions: données des actions (liste)
     @return: meilleure combinaison possible (liste)
    """
    max_inv = int(MAX_INVEST * 100)     # capacité
    total_actions = len(liste_actions)
    cout = []       # poids
    profit = []     # valeurs

    for action in liste_actions:
        cout.append(action[1])
        profit.append(action[2])

    # Trouve le profit optimal
    ks = [[0 for x in range(max_inv + 1)] for x in range(total_actions + 1)]

    for i in tqdm(range(1, total_actions + 1)):
        for w in range(1, max_inv + 1):
            if cout[i-1] <= w:
                ks[i][w] = max(profit[i-1] + ks[i-1][w-cout[i-1]], ks[i-1][w])
            else:
                ks[i][w] = ks[i-1][w]

    # Récupère la combinaison d'actions à partir du profit optimal
    meilleur_combinaison = []

    while max_inv >= 0 and total_actions >= 0:
        if ks[total_actions][max_inv] == \
                ks[total_actions-1][max_inv - cout[total_actions-1]] + profit[total_actions-1]:

            meilleur_combinaison.append(liste_actions[total_actions-1])
            max_inv -= cout[total_actions-1]

        total_actions -= 1

    return meilleur_combinaison, ks[-1][-1] / 100


def afficher_resultats(meilleur_combinaison, meilleur_profit):
    """Affiche les résultats de la meilleure combinaison

    @param meilleur_combinaison: combinaison d'actions la plus rentable (liste)
    @param meilleur_profit: Le profit total pour cette combinaison d'actions
    """
    print(f"\nInvestissement le plus rentable ({len(meilleur_combinaison)} actions) :\n")

    cout = []
    profit = []

    for item in meilleur_combinaison:
        print(f"{item[0]} | {item[1] / 100} € | +{item[2]} €")
        cout.append(item[1] / 100)
        profit.append(item[2])

    print("\nCoût total : ", sum(cout), "€")
    print("Profit après 2 ans : +", meilleur_profit, "€")
    print("\nTemps écoulé : ", time.time() - start_time, "secondes\n")

def main():
    """Choisissez le fichier csv à analyser et vérifiez si le fichier existe"""
    print("\nVeuillez choisir un dataset à analyser :")
    print("1: dataset1")
    print("2: dataset2")
    user_input = input("Votre choix (1 ou 2): ")

    if user_input == '1':
        filename = "dataset1.csv"
    elif user_input == '2':
        filename = "dataset2.csv"
    else:
        print("Choix non valide. Veuillez entrer 1 ou 2.")
        return

    if not os.path.exists(filename):
        print(f"\nLe fichier '{filename}' n'existe pas. Veuillez réessayer.\n")
        time.sleep(1)
        return

    shares_list = lire_donnees_csv(filename)

    print(f"\nTraitement de '{filename}' ({len(shares_list)} actions valides) pour {MAX_INVEST}€ :")
    resultats = knapsack(shares_list)
    afficher_resultats(*resultats)


if __name__ == "__main__":
    main()

