import random
import asyncio
from module_perso.jeu import Jeu
from module_perso.affichage import Affichage
from module_perso.logging_config import get_logger
from module_perso.joueur import Joueur
from module_perso.plateau import Plateau
from module_perso.db_extract import enregistrer_scores, recuperer_scores, top_3
from module_perso.changement_map import Changement_map
from module_perso.websocketo import WebSocketServer
from module_perso.decorateurs import log_result


logger = get_logger(__name__)


@log_result
async def traiter_case_speciale(
    effet, jeu, affichage, pion_actuel, joueurs, server, joueur_actuel
):
    """traiter l'effet de la case speciale en cascade limiter a une suite d'evenment en chaine de 5 max pour les joueur qui serais tomber sur une case speciale"""
    while effet and jeu.compteur_cascade < jeu.limite_cascade:
        if effet == "reculer":
            affichage.affichage_effet_case(effet, pion_actuel)
            effet = jeu.reculer_pion(pion_actuel, random.randint(1, 3))
        elif effet == "question":
            affichage.affichage_effet_case(effet, pion_actuel)
            question = jeu.poser_question()
            affichage.afficher_question(question)  # Utilise la méthode mise à jour
            reponse_client = await server.your_turn(
                joueur_actuel
            )  # asychronous pour permetre de repondre au questions
            if reponse_client.isdigit():
                reponse = int(reponse_client)
                correct = jeu.verifier_reponse(reponse, question)
                affichage.affichage_resultat_question(correct, pion_actuel)
                if correct:
                    effet = jeu.avancer_pion(pion_actuel, random.randint(1, 2))
                else:
                    effet = jeu.reculer_pion(pion_actuel, 1)
            else:
                affichage.afficher_message("Réponse invalide, aucun changement.")
                effet = None
        elif effet == "changement_map":
            Changement_map.appliquer_changement(jeu, joueurs)
            affichage.affichage_effet_case(effet, pion_actuel)
            affichage.affichage_plateau(jeu.plateau)
            effet = None


@log_result
def afficher_score_gagnant(affichage, joueurs):
    """Affiche le score de chaque joueur et le joueur gagnant actuellement."""
    affichage.afficher_message("Score :")
    for joueur in joueurs:
        affichage.afficher_message(str(joueur))

    meilleur = max(joueurs, key=lambda joueur: joueur.calculer_score_total())
    affichage.afficher_message(f"Joueur gagnant actuellement: {meilleur}")
    print(f"Top 3 : {top_3(recuperer_scores())}")


@log_result
async def demander_rejouer(affichage, joueurs, server):
    """Demande aux joueurs si ils veulent tous rejouer apres une partie (ils doissent choisir tous dire y pour rejouer)."""
    enregistrer_scores(joueurs)
    affichage.demander_rejouer()

    # cantainer pour le choix des joueurs
    decisions = {}

    for joueur in joueurs:
        while True:
            choix_rejouer = await server.your_turn(joueur)
            if choix_rejouer.lower() in {"y", "n"}:
                decisions[joueur.pseudo] = choix_rejouer.lower()
                break
            else:
                affichage.afficher_message(
                    f"Réponse invalide de {joueur.pseudo}, réessayez."
                )

    # si tous les joueurs ont répondu y
    if all(decision == "y" for decision in decisions.values()):
        affichage.afficher_message("Tous les joueurs ont accepté de rejouer.")
        for joueur in joueurs:
            joueur.pion.reset()  # Réinitialise les pions pour une nouvelle partie
        return True
    else:
        affichage.afficher_message(
            "Tous les joueurs n'ont pas accepté de rejouer. Fin du jeu."
        )
        affichage.afficher_message("Scores finaux :")
        joueurs_tries = Joueur.meilleurs_scores(joueurs)
        for joueur in joueurs_tries:
            affichage.afficher_message(str(joueur))
        affichage.afficher_message("Merci d'avoir joué !")
        return False


@log_result
async def jouer_tour(jeu, affichage, joueurs, server):
    """Joue un tour du jeu avec les joueurs et le serveur WebSocket."""
    try:
        joueur_actuel = joueurs[jeu.joueur_actuel]
        affichage.afficher_infos_tour(joueur_actuel, joueurs, jeu.plateau)

        # Utilisation de your_turn pour recevoir le message
        reponse_client = await server.your_turn(joueur_actuel)

        # Remplace le reponse_client direct par le message reçu
        if reponse_client in {"q", "esc"}:
            return "quitter"

        elif reponse_client == "n":
            jeu.tour_suivant()
            affichage.afficher_message(f"{joueur_actuel.pion.nom} a passé son tour.")
            return False

        elif reponse_client == "y":
            valeur_de = jeu.lancer_de()
            affichage.afficher_message(
                f"{joueur_actuel.pion.nom} a lancé le dé et a obtenu un {valeur_de}."
            )

            effet = jeu.avancer_pion(joueur_actuel.pion, valeur_de)
            affichage.affichage_pion(joueur_actuel.pion)

            if effet:
                await traiter_case_speciale(
                    effet,
                    jeu,
                    affichage,
                    joueur_actuel.pion,
                    joueurs,
                    server,
                    joueur_actuel,
                )

            if jeu.est_vainqueur(joueur_actuel.pion):
                affichage.annoncer_vainqueur(joueur_actuel.pion)
                joueur_actuel.ajouter_victoire()
                return "vainqueur"

        jeu.tour_suivant()
        return False
    except Exception as e:
        logger.exception(f"Une erreur s'est produite lors du tour du jeu : {e}")
        exit(
            -1
        )  # le programme dois s'arreter si cela arrive sans sauvegarder le score dans la db donc !


async def main():
    """Fonction principale du jeu de plateau avec WebSocket Server pour gerer en async les client / joueurs."""
    try:
        print(f"Top 3 : {top_3(recuperer_scores())}")
        logger.info("Lancement du jeu de plateau avec WebSocket Server.")
        affichage = Affichage()
    except Exception as e:
        logger.exception(
            f"Une erreur s'est produite lors du lancement des fonctionalité de routine  du jeu : {e}"
        )
        exit(
            -1
        )  # le programme dois s'arreter si cela arrive sans sauvegarder le score dans la db donc !
    # Démarrage du serveur WebSocket
    try:
        server = WebSocketServer()
        asyncio.create_task(server.run())
        print("Serveur WebSocket en cours d'exécution.")

        # Attente des connexions des joueurs
        joueurs = []
        while True:
            await asyncio.sleep(1)  # Temporisation pour limiter la boucle infinie
            if len(server.connected_players) >= 2 and server.ready:
                pseudos = server.pseudos  # Liste des pseudos des joueurs connectés
                joueurs = [Joueur(pseudo_proposer=pseudo) for pseudo in pseudos]
                break
    except Exception as e:
        logger.exception(
            f"Une erreur s'est produite lors de la connexion des joueurs : {e} et la gestion des routine du jeux entre main et le serveur / client side"
        )
        exit(
            -1
        )  # le programme dois s'arreter si cela arrive sans sauvegarder le score dans la db donc !
    # Paramètres du plateau
    taille_plateau = random.randint(10, 15)
    effets_possibles = ["reculer", "question", "changement_map"]

    while True:
        try:
            cases_speciales = Plateau.generer_cases_speciales(
                taille_plateau, effets_possibles
            )
            plateau = Plateau(taille=taille_plateau, cases_speciales=cases_speciales)
            jeu = Jeu([joueur.pseudo for joueur in joueurs], plateau=plateau)

            logger.info("Nouvelle partie initialisée.")
            affichage.afficher_message("Démarrage du jeu de plateau !")
            await server.broadcast(
                f"les joueurs sont : {[joueur.pseudo for joueur in joueurs]}"
            )
            affichage.affichage_plateau(jeu.plateau)

            vainqueur = False
            while not vainqueur:
                resultat = await jouer_tour(jeu, affichage, joueurs, server)
                if resultat == "quitter":
                    enregistrer_scores(joueurs)
                    exit()
                elif resultat == "vainqueur":
                    vainqueur = True

            afficher_score_gagnant(affichage, joueurs)

            if not await demander_rejouer(affichage, joueurs, server):
                exit()

        except Exception as e:
            logger.exception(
                f"Une erreur s'est produite lors de la boucle principale de la partie : {e}"
            )
            exit(
                -1
            )  # le programme dois s'arreter si cela arrive sans sauvegarder le score dans la db donc !


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.exception(
            f"Une erreur s'est produite coté serveur : {e}"
        )  # on tent de continuer si possible !
