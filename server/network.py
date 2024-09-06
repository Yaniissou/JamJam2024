import socket

# Classe pour gérer la connexion réseau
class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serveur = "localhost"  # adresse IP
        self.port = 5555
        self.adresse = (self.serveur, self.port)
        self.position = self.connecter()

    # Fonction pour obtenir la position initiale
    def getPos(self):
        return self.position

    # Fonction pour se connecter au serveur
    def connecter(self):
        try:
            print(f"Tentative de connexion au serveur à {self.adresse}")
            self.client.connect(self.adresse)
            print("Connexion réussie")
            return self.client.recv(2048).decode()
        except Exception as e:
            print(f"Erreur de connexion : {e}")
            return None

    # Fonction pour envoyer et recevoir des données
    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(f"Erreur d'envoi/réception : {e}")
