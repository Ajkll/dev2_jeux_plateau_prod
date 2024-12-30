import asyncio
import websockets
from module_perso.logging_config import get_logger
from module_perso.decorateurs import log_result

logger = get_logger(__name__)


class WebSocketServer:
    def __init__(self):
        self.connected_players = []
        self.ready = False
        self.maxsize = 4  # taille max du loby
        self.minsize = 2
        self.pseudos = []
        self.queues = {}  # message destiner a l'app (main)
        self.current_turn = None

    async def broadcast(self, message):
        """Envoyer un message à tous les clients connectés"""
        for player in self.connected_players:
            try:
                await player["websocket"].send(message)
            except websockets.exceptions.ConnectionClosed:
                logger.error(
                    f"severe :{player.get('pseudo', 'erreur dans le broadcast avec le client')}"
                )

    @log_result
    async def your_turn(self, joueur_actuel):
        """Permet uniquement au joueur actuel d'envoyer des messages"""
        pseudo_actuel = joueur_actuel.pseudo

        # le joueur dont c'est le tour
        self.current_turn = pseudo_actuel

        # attendre un message dans la file d'attente des messagesdu joueur(si c'est sont tour evidement)
        queue = self.queues[pseudo_actuel]
        message = await queue.get()

        # reset du tour une fois le message recu et traiter
        self.current_turn = None
        return message

    async def update_ready_state(self):
        """Mise à jour de l'état ready"""
        if (
            all(p["ready"] for p in self.connected_players)
            and len(self.connected_players) >= self.minsize
        ):
            self.ready = True
            logger.info("tous les players sont ready")
        else:
            self.ready = False
            logger.info(
                "le lobby n'est pas pret ,nbr de joueurs minimum doit etre >= a minsize et tour le monde n'est pas ready"
            )

    async def handler(
        self, websocket, path=None
    ):  # path dois etre donné quoi qu'il arrive (condition de websocket) donc None valeurs par default car on en a pas besoin
        """Gestionnaire principal pour chaque client WebSocket"""
        player = {"websocket": websocket, "ready": False, "pseudo": None}
        self.connected_players.append(player)
        logger.info(f"joueurs connectées : {self.get_connected_players()}")

        if len(self.connected_players) > self.maxsize:
            await websocket.send("Nombre maximal de joueurs atteint.")
            self.connected_players.remove(player)
            logger.warning(
                f"Connection rejeter nombre maximal de joueurs atteint limitte = {self.maxsize}"
            )
            return

        try:
            await websocket.send("Bonjour,entrer votre pseudo favorit (pls):")
            async for message in websocket:
                logger.debug(
                    f"Message recue de {player.get('pseudo', 'inconnu')} : {message}"
                )

                if not player["pseudo"]:
                    player["pseudo"] = (
                        message.strip() or f"Joueur{len(self.connected_players)}"
                    )
                    self.pseudos.append(
                        player["pseudo"]
                    )  # liste des pseudos tenue a jour
                    self.queues[player["pseudo"]] = asyncio.Queue()
                    logger.info(f"pseudo joueur joueur ajouter: {player['pseudo']}")
                    await self.broadcast(
                        f"{player['pseudo']} a rejoint la partie de jeu"
                    )
                    continue

                if message == "ready":
                    player["ready"] = True
                    logger.info(f"{player['pseudo']} est ready")
                    await self.broadcast(
                        f"{player['pseudo']} est ready to go. liste des joueurs ready : {self.get_ready_state()}"
                    )
                    await self.update_ready_state()
                else:
                    if player["pseudo"] == self.current_turn:
                        await self.queues[player["pseudo"]].put(message)
                    else:
                        logger.info(
                            f"{player['pseudo']}tente d'ecrire alors que c'est pas son tour"
                        )
                        await websocket.send("Ce n'est pas votre tour attendez !")

        except websockets.exceptions.ConnectionClosed as e:
            logger.error(
                f"sever le joueur a eu un probleme pour nous joindre : {player.get('pseudo', 'inconnu')} détails : {e}"
            )
        except Exception as e:
            logger.error(
                f"sever exception inconnue {player.get('pseudo', 'inconnu')} détails : {e}"
            )
        finally:
            if player in self.connected_players:
                self.connected_players.remove(player)
                if player["pseudo"] in self.pseudos:
                    self.pseudos.remove(
                        player["pseudo"]
                    )  # Retirer le pseudo de la liste
                self.queues.pop(player["pseudo"], None)  # Supprimer la file du joueur
                logger.info(
                    f"Connexion terminer normalement pour le joueur : {player.get('pseudo', 'inconnu')} était encore connecter: {self.get_connected_players()}"
                )
                await self.update_ready_state()

    @log_result
    def get_ready_state(self):
        """retourne l'état des joueurs ready to go"""
        state = ", ".join(
            [
                f"{p['pseudo']} (Prêt : {'Oui' if p['ready'] else 'Non'})"
                for p in self.connected_players
            ]
        )
        return state

    @log_result
    def get_connected_players(self):
        """retourne une liste des pseudos des joueurs connecter"""
        return [p.get("pseudo", "inconnu") for p in self.connected_players]

    async def run(self):
        """Methode de lancement du serveur WebSocketo"""
        server = await websockets.serve(self.handler, "0.0.0.0", 8765)
        logger.info(
            "serveur WebSocketo ready et a l'ecoute (pour tout tentative de connection): ws://0.0.0.0:8765"
        )
        await server.wait_closed()
