import socket
from ssl import socket_error


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serveur = "192.168.41.225"  # Remplace par l'adresse IP de l'hôte du serveur
        self.port = 12345
        self.adresse = (self.serveur, self.port)
        self.position = self.connecter()

    def getPos(self):
        return self.position

    def connecter(self):
        try:
            print(f"Tentative de connexion au serveur à {self.adresse}")
            self.client.connect(self.adresse)
            print("Connexion réussie")
            return self.client.recv(1024).decode()
        except:
            pass

    #envoyer les données de l'autre joueur
    #sa position, son pseudo, et le pays choisi
    def sendPlayerData(self, pos, pseudo, country):
        try:
            #les données concernées
            data = f"{pos[0]},{pos[1]};{pseudo};{country}"
            self.client.send(str.encode(data))

            #le résultat
            result = self.client.recv(1024).decode()
            return result.split(";")
        except socket.error as e: #si il y a un souci
            print(e)

    #envoyer les données des batiments sur la map
    #nom, compétence associée, vie restante, statut
    def sendBuildingData(self, name, competence, life, isClaimed):
        try:
            data = f"{name},{competence}, {life}, {isClaimed}"
            self.client.send(str.encode(data))

            result = self.client.recv(1024).decode()
            return result.split(";")
        except socket_error as e:
            print(e)