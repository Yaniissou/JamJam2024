import socket

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serveur = "192.168.122.1"  # Remplace par l'adresse IP de l'hôte du serveur
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
            return self.client.recv(2048).decode()
        except:
            pass

    def send_data(self, pos, pseudo, country):
        try:
            data = f"{pos[0]},{pos[1]};{pseudo};{country}"
            self.client.send(str.encode(data))

            retour = self.client.recv(2048).decode()
            return retour.split(";")
        except socket.error as e:
            print(e)
