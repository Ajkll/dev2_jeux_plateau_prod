import random
from module_perso.jeu import Jeu
from module_perso.affichage import Affichage
from module_perso.logging_config import get_logger
from module_perso.joueur import Joueur
from module_perso.plateau import Plateau
from module_perso.db_extract import enregistrer_scores, recuperer_scores, top_3
from module_perso.changement_map import Changement_map

logger = get_logger(__name__)


def traiter_case_speciale(effet, jeu, affichage, pion_actuel, joueurs):
    while effet and jeu.compteur_cascade < jeu.limite_cascade:
        if effet == "reculer":
            affichage.affichage_effet_case(effet, pion_actuel)
            effet = jeu.reculer_pion(pion_actuel, 2)
        elif effet == "question":
            affichage.affichage_effet_case(effet, pion_actuel)
            question = jeu.poser_question()
            reponse = affichage.poser_question(question)
            correct = jeu.verifier_reponse(reponse, question)
            affichage.affichage_resultat_question(correct, pion_actuel)
            if correct:
                effet = jeu.avancer_pion(pion_actuel, 1)
            else:
                effet = jeu.reculer_pion(pion_actuel, 1)
        elif effet == "changement_map":
            Changement_map.appliquer_changement(jeu, joueurs)
            affichage.affichage_effet_case(effet, pion_actuel)
            affichage.affichage_plateau(jeu.plateau)
            effet = None  # Pas de cascade après changement de map(normalement impossible mais par sécurité)


def afficher_score_gagnant(affichage, joueurs):
    affichage.afficher_message("Score :")
    for joueur in joueurs:
        affichage.afficher_message(str(joueur))

    # trouver et afficher le meilleur joueur de la partie et afficher le top 3
    meilleur = max(joueurs, key=lambda joueur: joueur.calculer_score_total())
    affichage.afficher_message(f"Joueur gagnant actuellement: {meilleur}")
    print(f"Top 3 : {top_3(recuperer_scores())}")


def demander_rejouer(affichage, joueurs):
    enregistrer_scores(joueurs)
    choix_rejouer = affichage.demander_rejouer()
    if choix_rejouer == "n":
        affichage.afficher_message("Scores finaux :")
        joueurs_tries = Joueur.meilleurs_scores(joueurs)
        for joueur in joueurs_tries:
            affichage.afficher_message(str(joueur))
        affichage.afficher_message("Merci d'avoir joué !")
        return False
    else:
        for joueur in joueurs:
            joueur.pion.reset()
        return True


def jouer_tour(jeu, affichage, joueurs):
    joueur_actuel = joueurs[jeu.joueur_actuel]
    pion_actuel = joueur_actuel.pion

    affichage.afficher_infos_tour(joueur_actuel, joueurs, jeu.plateau)
    choix_action = affichage.demander_action(pion_actuel)

    if choix_action in {"q", "esc"}:
        return "quitter"

    elif choix_action == "n":
        jeu.tour_suivant()
        affichage.afficher_message(f"{pion_actuel.nom} a passé son tour.")
        return False

    elif choix_action == "y":
        valeur_de = jeu.lancer_de()
        affichage.afficher_message(
            f"{pion_actuel.nom} a lancé le dé et a obtenu un {valeur_de}."
        )

        effet = jeu.avancer_pion(pion_actuel, valeur_de)
        affichage.affichage_pion(pion_actuel)

        if effet:
            traiter_case_speciale(effet, jeu, affichage, pion_actuel, joueurs)

        if jeu.est_vainqueur(pion_actuel):
            affichage.annoncer_vainqueur(pion_actuel)
            joueur_actuel.ajouter_victoire()
            return "vainqueur"

    jeu.tour_suivant()
    return False


def main():
    print(f"Top 3 : {top_3(recuperer_scores())}")
    logger.info("Lancement du jeu de plateau.")
    affichage = Affichage()

    query_nb_joueurs = affichage.demander_nb_joueurs()
    nb_joueurs = query_nb_joueurs  # Nombre de joueurs.
    joueurs = [Joueur() for _ in range(nb_joueurs)]

    # Paramètres du plateau
    taille_plateau = random.randint(10, 15)
    effets_possibles = ["reculer", "question", "changement_map"]

    while True:  # Boucle de jeu principale.
        # Initialisation du plateau et du jeu
        cases_speciales = Plateau.generer_cases_speciales(
            taille_plateau, effets_possibles
        )
        plateau = Plateau(taille=taille_plateau, cases_speciales=cases_speciales)
        jeu = Jeu([joueur.pseudo for joueur in joueurs], plateau=plateau)
        logger.info("Nouvelle partie initialisée.")
        affichage.afficher_message("Démarrage du jeu de plateau !")
        affichage.affichage_plateau(jeu.plateau)

        vainqueur = False
        while not vainqueur:
            resultat = jouer_tour(jeu, affichage, joueurs)
            if resultat == "quitter":
                enregistrer_scores(joueurs)
                exit()
            elif resultat == "vainqueur":
                vainqueur = True

        # Afficher les scores après chaque partie.
        afficher_score_gagnant(affichage, joueurs)

        # Demander si on rejoue.
        if not demander_rejouer(affichage, joueurs):
            exit()


if __name__ == "__main__":
    main()
