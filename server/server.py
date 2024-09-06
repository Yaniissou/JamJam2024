import socket
from _thread import *

serveur = "0.0.0.0"  #  écoute sur toutes les interfaces
port = 1929

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Liaison du serveur au port
try:
    s.bind((serveur, port))
    print(f"Serveur lié au port {port}, écoute sur toutes les interfaces")
except socket.error as e:
    print(f"Erreur lors de la liaison au port : {e}")


s.listen(2)
print("En attente de connexions, serveur démarré")

# Fonction pour lire une position
def lire_position(chaine):
    chaine = chaine.split(",")
    return int(chaine[0]), int(chaine[1])

# Fonction pour créer une position à partir d'un tuple
def creer_position(tup):
    return str(tup[0]) + "," + str(tup[1])

# Liste des positions des joueurs
positions = [(0, 0), (100, 100)]

# Fonction pour gérer chaque client sur un nouveau thread
def client_thread(conn, joueur):
    conn.send(str.encode(creer_position(positions[joueur])))  # Envoie la position initiale au client
    reponse = ""
    while True:
        try:
            donnees = lire_position(conn.recv(2048).decode())  # Reçoit les données du client
            positions[joueur] = donnees  # Met à jour la position du joueur

            if not donnees:
                print("Déconnecté")
                break
            else:
                reponse = positions[1] if joueur == 0 else positions[0]  # Position de l'autre joueur
                print("Reçu : ", donnees)
                print("Envoi : ", reponse)

            conn.sendall(str.encode(creer_position(reponse)))  # Envoie la position de l'autre joueur
        except:
            break

    print("Connexion perdue")
    conn.close()

joueur_actuel = 0
while True:
    # Accepter une connexion
    conn, addr = s.accept()
    print("Connecté à :", addr)

    # Démarrer un nouveau thread pour gérer la connexion
    start_new_thread(client_thread, (conn, joueur_actuel))
    joueur_actuel += 1

    # Limiter à deux joueurs maximum
    if joueur_actuel > 1:
        joueur_actuel = 0
