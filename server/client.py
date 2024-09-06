import pygame
from network import Network

# Définir la largeur et la hauteur de la fenêtre
largeur = 500
hauteur = 500
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Client")

# Classe Joueur
class Joueur:
    def __init__(self, x, y, largeur, hauteur, couleur):
        # Position et dimensions du joueur
        self.x = x
        self.y = y
        self.largeur = largeur
        self.hauteur = hauteur
        self.couleur = couleur
        self.rect = (x, y, largeur, hauteur)
        # Vitesse de déplacement du joueur
        self.vitesse = 7

    # Fonction pour dessiner le joueur sur la fenêtre
    def dessiner(self, fenetre):
        pygame.draw.rect(fenetre, self.couleur, self.rect)

    # Fonction pour déplacer le joueur selon les touches appuyées
    def bouger(self):
        touches = pygame.key.get_pressed()

        if touches[pygame.K_LEFT]:
            self.x -= self.vitesse
        if touches[pygame.K_RIGHT]:
            self.x += self.vitesse
        if touches[pygame.K_UP]:
            self.y -= self.vitesse
        if touches[pygame.K_DOWN]:
            self.y += self.vitesse
        self.mettre_a_jour()

    # Fonction pour mettre à jour les coordonnées du joueur
    def mettre_a_jour(self):
        self.rect = (self.x, self.y, self.largeur, self.hauteur)

# pour lire une position à partir d'une chaine de caractère
def lire_position(chaine):
    chaine = chaine.split(",")
    return int(chaine[0]), int(chaine[1])

# convertir une position en chaîne de caractères
def creer_position(tup):
    return str(tup[0]) + "," + str(tup[1])

# Fonction pour redessiner la fenêtre de jeu
def redessiner_fenetre(fenetre, joueur, joueur2):
    fenetre.fill((255, 255, 255))  # Remplir la fenêtre avec une couleur blanche
    joueur.dessiner(fenetre)
    joueur2.dessiner(fenetre)
    pygame.display.update()  # Mettre à jour l'affichage


# Fonction principale du client
def main():
    continuer = True
    reseau = Network()
    position_depart = lire_position(reseau.getPos())
    print(f"Position de départ : {position_depart}")

    joueur = Joueur(position_depart[0], position_depart[1], 100, 100, (0, 255, 0))
    joueur2 = Joueur(0, 0, 100, 100, (0, 255, 0))
    horloge = pygame.time.Clock()


    while continuer:
        horloge.tick(60)

        try:
            pos_joueur2 = lire_position(reseau.send(creer_position((joueur.x, joueur.y))))
        except:
            print("Échec de réception des positions")
            continue

        joueur2.x = pos_joueur2[0]
        joueur2.y = pos_joueur2[1]
        joueur2.mettre_a_jour()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continuer = False
                pygame.quit()

        joueur.bouger()
        redessiner_fenetre(fenetre, joueur, joueur2)

main()
