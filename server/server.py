import socket
from _thread import *

# Paramètres du serveur
serveur = "0.0.0.0"  # écoute sur toutes les interfaces réseau
port = 1920

# Création du socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Liaison du serveur au port
try:
    s.bind((serveur, port))
except socket.error as e:
    print(f"Erreur de liaison : {str(e)}")

s.listen(2)
print("En attente de connexions, serveur démarré")

# Liste pour stocker les données des joueurs (position, pseudo, pays)
players_data = [{"pos": (100, 100), "pseudo": "", "country": None}, {"pos": (300, 300), "pseudo": "", "country": None}]


# Fonction pour lire une position
def lire_position(chaine):
    chaine = chaine.split(",")
    return int(chaine[0]), int(chaine[1])


# Fonction pour formater une position en chaîne
def creer_position(tup):
    return str(tup[0]) + "," + str(tup[1])


# Fonction qui gère chaque client sur un nouveau thread
def client_thread(conn, joueur):
    conn.send(str.encode(creer_position(players_data[joueur]["pos"])))  # Envoi de la position initiale
    while True:
        try:
            data = conn.recv(2048).decode()
            if not data:
                print("Déconnecté")
                break

            # Récupération des données (position, pseudo, pays)
            data_parts = data.split(";")
            position = lire_position(data_parts[0])
            pseudo = data_parts[1]
            country = data_parts[2]

            # Mise à jour des données du joueur
            players_data[joueur]["pos"] = position
            players_data[joueur]["pseudo"] = pseudo
            players_data[joueur]["country"] = country

            # Envoi des informations de l'autre joueur
            other_player = 1 if joueur == 0 else 0
            response = f"{creer_position(players_data[other_player]['pos'])};{players_data[other_player]['pseudo']};{players_data[other_player]['country']}"
            conn.sendall(str.encode(response))
        except:
            break

    print("Connexion perdue")
    conn.close()


# Gestion des connexions des joueurs
joueur_actuel = 0
while True:
    conn, addr = s.accept()
    print("Connecté à :", addr)

    # Création d'un nouveau thread pour chaque joueur
    start_new_thread(client_thread, (conn, joueur_actuel))
    joueur_actuel += 1

    if joueur_actuel > 1:
        joueur_actuel = 0
