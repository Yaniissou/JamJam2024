import socket

# Classe pour gérer la connexion réseau
class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serveur = "localhost"
        self.port = 1920
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
        except:
            pass

    # Fonction pour envoyer et recevoir des données
    def send_data(self, pos, pseudo, country):
        try:
            # On envoie la position, le pseudo et le pays sous forme de chaîne
            data = f"{pos[0]},{pos[1]};{pseudo};{country}"
            self.client.send(str.encode(data))

            # On reçoit la réponse du serveur (position, pseudo, pays de l'autre joueur)
            retour = self.client.recv(2048).decode()
            return retour.split(";")  # On sépare les données
        except socket.error as e:
            print(e)
