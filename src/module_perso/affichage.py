import os
import time


def un_deux_trois(*messages, delay=2):
    for message in messages:
        print(f"Annonce : {message}")
        time.sleep(delay)


class Affichage:
    @staticmethod
    def afficher_message(message):
        un_deux_trois(message)

    @staticmethod
    def affichage_pion(pion):
        un_deux_trois(f"{pion.nom} est maintenant sur la case {pion.position}.")

    @staticmethod
    def affichage_plateau(plateau):
        un_deux_trois("\nVoici le plateau de jeu :", str(plateau))

    @staticmethod
    def afficher_infos_tour(joueur_actuel, joueurs, plateau):
        os.system("cls" if os.name == "nt" else "clear")
        print(f"Tour de {joueur_actuel.pseudo}.")
        print("Positions actuelles des joueurs :")
        for joueur in joueurs:
            print(f"- {joueur.pseudo}: case {joueur.pion.position}")
        print("\nPlateau de jeu :")
        print(plateau)

    @staticmethod
    def demander_action(pion):
        while True:
            choix = (
                input(f"{pion.nom}, voulez-vous lancer le dé ? (y/n/q) : ")
                .strip()
                .lower()
            )
            if choix in ("y", "n", "q", "esc"):
                return choix
            elif choix.isdigit():
                return int(choix)
            else:
                print(
                    "Entrée invalide. Veuillez répondre par 'y', 'n', un chiffre, ou 'q'/Esc."
                )

    @staticmethod
    def annoncer_vainqueur(pion):
        un_deux_trois(f"Félicitations, {pion.nom}, vous gagnez la partie !")

    @staticmethod
    def affichage_effet_case(effet, pion):
        if effet == "reculer":
            un_deux_trois(f"Attention ! {pion.nom}, vous devez reculer de 2 cases.")
        elif effet == "question":
            un_deux_trois(f"{pion.nom}, vous êtes sur une case Question !")
        elif effet == "changement_map":
            un_deux_trois(
                f"{pion.nom}, vous avez déclenché un changement de map !",
                "Le plateau est réinitialisé, vous êtes à la case départ.",
            )

    @staticmethod
    def poser_question(question):
        print(f"Question : {question['question']}")
        for option in question["options"]:
            print(option)

        while True:
            reponse = input("Votre réponse (entrez le numéro de l'option) : ").strip()
            if reponse.isdigit():
                return int(reponse)
            else:
                print(
                    "Choix de réponse invalide. Veuillez entrer un numéro de réponse."
                )

    @staticmethod
    def affichage_resultat_question(correct, pion):
        if correct:
            un_deux_trois(f"Bonne réponse ! {pion.nom}, vous avancez d'une case.")
        else:
            un_deux_trois(f"Mauvaise réponse ! {pion.nom}, vous reculez d'une case.")

    @staticmethod
    def demander_rejouer():
        while True:
            choix = input("Voulez-vous rejouer ? (y/n) : ").strip().lower()
            if choix in ("y", "n"):
                return choix
            else:
                print("Entrée invalide. Veuillez répondre par 'y' ou 'n'.")

    @staticmethod
    def demander_nb_joueurs():
        while True:
            choix = input("Combien de joueurs ? (2-4) : ").strip()
            if choix.isdigit() and 2 <= int(choix) <= 4:
                return int(choix)
            else:
                print("Entrée invalide. Veuillez entrer un nombre entre 2 et 4.")
