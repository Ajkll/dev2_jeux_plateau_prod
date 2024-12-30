import os
import time


# on ne logs pas no message ici il s'affiche sinon on le serras !
def un_deux_trois(*messages, delay=2):
    """Affiche des messages (variatic on sait pas combien de message ici) avec un delay specifique"""
    for message in messages:
        print(f"Annonce : {message}")
        time.sleep(delay)


class Affichage:
    @staticmethod
    def afficher_message(message):
        """Affiche un message génerique ici"""
        un_deux_trois(message)

    @staticmethod
    def affichage_pion(pion):
        """Affiche la position du pion apres son deplacement grace a la methode lancer de de qui enclanche deplacement dans la class jeu"""
        un_deux_trois(f"{pion.nom} est maintenant sur la case {pion.position}.")

    @staticmethod
    def affichage_plateau(plateau):
        """Affiche le plateau de jeu"""
        un_deux_trois("\nVoici le plateau de jeu :", str(plateau))

    @staticmethod
    def afficher_infos_tour(joueur_actuel, joueurs, plateau):
        """Affiche toutes les infos utilile pour le joueur pour un tour"""
        os.system("cls" if os.name == "nt" else "clear")
        print(f"Tour de {joueur_actuel.pseudo}.")
        print("Positions actuelles des joueurs :")
        for joueur in joueurs:
            print(f"- {joueur.pseudo}: case {joueur.pion.position}")
        print("\nPlateau de jeu :")
        print(plateau)

    @staticmethod
    def annoncer_vainqueur(pion):
        """Affiche l'annonce de vainqueur"""
        un_deux_trois(f"Félicitations, {pion.nom}, vous gagnez la partie !")

    @staticmethod
    def affichage_effet_case(effet, pion):
        """Affiche l'effet de la case speciale"""
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
    def afficher_question(question):
        """Affiche la question et les options"""
        print(f"Question : {question['question']}")
        for option in question["options"]:
            print(option)

    @staticmethod
    def affichage_resultat_question(correct, pion):
        """Affiche le resultat du choix pris pour la question"""
        if correct:
            un_deux_trois(f"Bonne réponse ! {pion.nom}, vous avancez d'une case.")
        else:
            un_deux_trois(f"Mauvaise réponse ! {pion.nom}, vous reculez d'une case.")

    @staticmethod
    def demander_rejouer():
        """Demande au joueur si il veut rejouer"""
        un_deux_trois("Voulez-vous rejouer ? (y/n) : ")
