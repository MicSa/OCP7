from tqdm import tqdm
import csv
import time
import os

# Enregistre le temps au début de l'exécution du script
start_time = time.time()

MAX_INVEST = 500  # Montant maximum à investir

# Fonction pour lire les données du fichier csv
def lire_donnees_csv(filename):
    """Importe les données des actions à partir d'un fichier csv
    Filtre les données corrompues
    """
    with open(filename) as csvfile:
        # Utilise la bibliothèque csv pour lire le fichier
        shares_file = csv.reader(csvfile, delimiter=',')
        next(csvfile)  # Saute la première ligne (en-têtes de colonne)

        # Initialise une liste vide pour stocker les actions
        liste_actions = []

        # Parcourt chaque ligne du fichier csv
        for row in shares_file:
            # Ignore les lignes avec des valeurs négatives ou nulles
            if float(row[1]) <= 0 or float(row[2]) <= 0:
                pass
            else:
                # Crée un tuple pour chaque action et l'ajoute à la liste
                action = (
                    row[0],
                    int(float(row[1])*100),
                    float(float(row[1]) * float(row[2]) / 100)
                )
                liste_actions.append(action)

        return liste_actions  # Retourne la liste d'actions


def knapsack(liste_actions):
    """Initialise la matrice (ks) pour le problème du sac à dos 0-1
    Obtient la meilleure combinaison d'actions
    """
    # Convertit le montant maximal d'investissement en centimes pour éviter les problèmes de précision
    max_inv = int(MAX_INVEST * 100)
    total_actions = len(liste_actions)  # Nombre total d'actions disponibles
    cout = []   # Liste pour stocker le coût de chaque action
    profit = []  # Liste pour stocker le profit de chaque action

    # Parcourt chaque action et ajoute son coût et son profit aux listes respectives
    for action in liste_actions:
        cout.append(action[1])
        profit.append(action[2])

    # Initialise une matrice de zéros pour le problème du sac à dos
    ks = [[0 for x in range(max_inv + 1)] for x in range(total_actions + 1)]

    # Remplit la matrice à l'aide de l'algorithme du sac à dos
    for i in tqdm(range(1, total_actions + 1)):  # tqdm est utilisé pour afficher une barre de progression
        for w in range(1, max_inv + 1):
            if cout[i-1] <= w:
                ks[i][w] = max(profit[i-1] + ks[i-1][w-cout[i-1]], ks[i-1][w])
            else:
                ks[i][w] = ks[i-1][w]

    # Trouve la combinaison d'actions optimale
    meilleur_combinaison = []

    # Parcourt la matrice à partir de la fin pour déterminer les actions à inclure dans la combinaison optimale
    while max_inv >= 0 and total_actions >= 0:
        if ks[total_actions][max_inv] == \
                ks[total_actions-1][max_inv - cout[total_actions-1]] + profit[total_actions-1]:

            meilleur_combinaison.append(liste_actions[total_actions-1])
            max_inv -= cout[total_actions-1]

        total_actions -= 1

    while max_inv >= 0 and total_actions >= 0:
        if ks[total_actions][max_inv] == \
            ks[total_actions-1][max_inv - cout[total_actions-1]] + profit[total_actions-1]:
            # Si l'action est incluse dans la solution optimale, l'ajouter à la liste
            meilleur_combinaison.append(liste_actions[total_actions-1])
            # Soustraire le coût de l'action du montant total
            max_inv -= cout[total_actions-1]
        # Passe à l'action précédente
        total_actions -= 1
    # Retourne la meilleure combinaison d'actions et le profit total
    return meilleur_combinaison, ks[-1][-1] / 100



def afficher_resultats(meilleur_combinaison, meilleur_profit):
    """Affiche les résultats de la meilleure combinaison
    """
    print(f"\nInvestissement le plus rentable ({len(meilleur_combinaison)} actions) :\n")

    cout = []   # Liste pour stocker le coût de chaque action dans la meilleure combinaison
    profit = []  # Liste pour stocker le profit de chaque action dans la meilleure combinaison

    # Parcourt chaque action dans la meilleure combinaison et affiche ses détails
    for item in meilleur_combinaison:
        print(f"{item[0]} | {item[1] / 100} € | +{item[2]} €")
        # Ajoute le coût et le profit de l'action aux listes respectives
        cout.append(item[1] / 100)
        profit.append(item[2])

    # Affiche le coût total, le profit total et le temps d'exécution
    print("\nCoût total : ", sum(cout), "€")
    print("Profit après 2 ans : +", meilleur_profit, "€")
    print("\nTemps écoulé : ", time.time() - start_time, "secondes\n")


def main():
    """Choisissez le fichier csv à analyser et vérifiez si le fichier existe"""
    print("\nVeuillez choisir un dataset à analyser :")
    print("1: dataset1")
    print("2: dataset2")
    # Demande à l'utilisateur de choisir un dataset
    user_input = input("Votre choix (1 ou 2): ")

    # Sélectionne le fichier csv en fonction du choix de l'utilisateur
    if user_input == '1':
        filename = "dataset1.csv"
    elif user_input == '2':
        filename = "dataset2.csv"
    else:
        print("Choix non valide. Veuillez entrer 1 ou 2.")
        return

    # Vérifie si le fichier existe
    if not os.path.exists(filename):
        print(f"\nLe fichier '{filename}' n'existe pas. Veuillez réessayer.\n")
        time.sleep(1)  # Attends une seconde avant de quitter
        return

    # Lit les données du fichier csv
    shares_list = lire_donnees_csv(filename)

    # Affiche le nombre d'actions et le montant à investir
    print(f"\nTraitement de '{filename}' ({len(shares_list)} actions valides) pour {MAX_INVEST}€ :")
    # Résoud le problème du sac à dos
    resultats = knapsack(shares_list)
    # Affiche les résultats
    afficher_resultats(*resultats)


if __name__ == "__main__":
    main()  # Appelle la fonction principale lorsque le script est exécuté

                    