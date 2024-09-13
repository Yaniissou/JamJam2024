import socket
from _thread import start_new_thread
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

#from game.objects.Structure import Structure

#adresse + port pour se connecter au serveur
serveur = "0.0.0.0"  # écoute sur toutes les interfaces réseau
port = 5555

#créer le socket
#une connection INET et de type STREAMing
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#on donne l'adresse au serveur
try:
    s.bind((serveur, port))
except socket.error as e:
    print("erreur: " + str(e))

s.listen(2)
print("serveur démarré — attend les connexions")

# stocker les données des joueurs
players_data = [{"pos": (100, 100), "pseudo": "Joueur1", "country": "France"},
                {"pos": (100, 100), "pseudo": "Joueur2", "country": "Allemagne"}]

#test pour envoyer des objets: utiliser Pickle
#baseStructure = Structure("nom", None, 0, None, False, 0, False)
#buildings_data = pickle.dumps(baseStructure)

#lire une position
def lire_position(chaine):
    chaine = chaine.split(",")
    return int(chaine[0]), int(chaine[1])

#convertir une position en chaine
def positionToStr(tup):
    return f"{tup[0]},{tup[1]}"

#créer un nouveau thread avec les données qu'on veut envoyer
def client_thread(conn, joueur):
    #la position initiale
    conn.send(str.encode(positionToStr(players_data[joueur]["pos"])))

    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                print("déconnecté")
                break

            #on récupère les données
            data_parts = data.split(";")
            position = lire_position(data_parts[0])
            pseudo = data_parts[1]
            country = data_parts[2]

            #on les met à jour avec les vraies données
            players_data[joueur]["pos"] = position
            players_data[joueur]["pseudo"] = pseudo
            players_data[joueur]["country"] = country

            # Envoi des informations de l'autre joueur
            other_player = 1 if joueur == 0 else 0
            response = f"{positionToStr(players_data[other_player]['pos'])};{players_data[other_player]['pseudo']};{players_data[other_player]['country']}"
            conn.sendall(str.encode(response))
        except:
            break

    print("connexion perdue :/")
    conn.close()

#
joueur_actuel = 0
while True:
    conn, addr = s.accept()
    print("actuellement connecté à :", addr)

    #pour chaque joueur, un thread
    start_new_thread(client_thread, (conn, joueur_actuel))
    joueur_actuel += 1

    if joueur_actuel > 1:
        joueur_actuel = 0