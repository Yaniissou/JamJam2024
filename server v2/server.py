import socket
from _thread import *
import sys

#ip du serveur & son port
server = "192.168.56.1"
port = 5555

#type de connexion
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#bind le serveur à l'ip et au port donnés
try:
    s.bind((server, port))
#si ça marche pas on dit pourquoi
except socket.error as e:
    str(e)

#ouvrir le port aux connexions
#2 personnes pour le test
s.listen(2)
print("en attente de connexions!!")


def clientThread(connexion):

    reply = ""
    #tant qu'on est connecté
    while True:
        try:
            #+ la valeur est haute, + ça va mettre de temps
            data = connexion.recv(2048)
            reply = data.decode("utf-8")

            #si on reçoit rien c'est qu'il y a souci
            if not data:
                print("problème de connexion :(")
                break
            #sinon on affiche les stats
            else:
                print("réponse du client: ", reply)
                print("envoi: ", reply)
            connexion.sendall(str.encode(reply))
        #si il y a un problème quelconque on arrête tout
        except:
            break

while True:
    connexion, adresse = s.accept()
    print("connexion effectuée vers", adresse)

    #on démarre un thread une fois connecté
    #va exécuter la fonction en async
    start_new_thread(clientThread, (connexion,))
