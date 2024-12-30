import websocket
import threading


def on_message(ws, message):
    """Fonction appelée lorsque le serveur envoie un message aux clients"""
    print(f"Message reçu : {message}")


def on_error(ws, error):
    """Fonction appelée lorsque le serveur renvoie une erreur"""
    print(f"Erreur : {error}")


def on_close(ws, close_status_code, close_msg):
    """Fonction appelée lorsque la connexion est fermée par le serveur avec le code de fermeture et un message si le serveur le fournit"""
    print(f"Connexion fermée avec code {close_status_code} et message {close_msg}")


def on_open(ws):
    """Fonction appelée lorsque la connexion est ouverte"""
    print("Connexion ouverte")

    def envoyer_messages():
        """Fonction pour permettre d'envoyer sur un thread des messages tout en écoutant sur un autre thread les réponses"""
        while True:
            message = input("Entrez un message à envoyer : ")
            ws.send(message)

    # thread pour permettre d'envoyer des messages tout en écoutant les réponses
    threading.Thread(target=envoyer_messages, daemon=True).start()


if __name__ == "__main__":
    ws = websocket.WebSocketApp(
        "ws://172.18.0.3:8765",
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )
    ws.on_open = on_open
    ws.run_forever()
