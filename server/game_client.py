import sys
import os
import pygame
import pytmx
from network import Network  # Assurez-vous que 'network.py' est dans le dossier 'server'

# Ajouter dynamiquement le chemin du projet à sys.path pour inclure le module 'game'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Ensuite, après avoir ajouté le chemin, importe les éléments nécessaires de 'game'
from game import draw_map, get_collision_tiles, generate_items, circleZone, checkItemCollisions, take
from game.objects.player import Player  # Assurez-vous que 'player.py' est dans 'game/objects'

# Charger les données de la carte .tmx
tmx_file = os.path.join(os.path.dirname(__file__), '../game/assets/map/tileset/1.tmx')
tmx_data = pytmx.util_pygame.load_pygame(tmx_file)

# Définir la largeur et la hauteur de la fenêtre
largeur = 1024
hauteur = 768
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Client Multijoueur")

# Fonction pour lire une position à partir d'une chaîne de caractères
def lire_position(chaine):
    chaine = chaine.split(",")
    return int(chaine[0]), int(chaine[1])

# Fonction pour redessiner la fenêtre
def redessiner_fenetre(fenetre, joueur, joueur2):
    fenetre.fill((255, 255, 255))  # Couleur de fond
    joueur.dessiner(fenetre)
    joueur2.dessiner(fenetre)
    pygame.display.update()

# Fonction principale du client
def main():
    continuer = True
    reseau = Network()  # Connexion au réseau via Network
    position_depart = lire_position(reseau.getPos())
    print(f"Position de départ : {position_depart}")

    # Initialisation des joueurs avec les compétences
    joueur = Player(position_depart[0], position_depart[1], competences={0: 100, 1: 100, 2: 100, 3: 100, 4: 100, 5: 100})
    joueur2 = Player(0, 0, competences={0: 100, 1: 100, 2: 100, 3: 100, 4: 100, 5: 100})  # Le deuxième joueur (autre client)

    pseudo = "MonPseudo"  # Pseudo du joueur (à modifier si nécessaire)
    country = "France"    # Pays choisi par l'utilisateur

    horloge = pygame.time.Clock()

    # Générer les objets du jeu
    global items
    items = generate_items(5)

    while continuer:
        horloge.tick(60)

        # Envoi des données au serveur et réception des données du joueur 2
        try:
            data_joueur2 = reseau.send_data((joueur.rect.x, joueur.rect.y), pseudo, country)
            pos_joueur2 = lire_position(data_joueur2[0])
            pseudo_joueur2 = data_joueur2[1]
            country_joueur2 = data_joueur2[2]
        except:
            print("Erreur de réception des données")
            continue

        # Mise à jour des informations du joueur 2
        joueur2.rect.x = pos_joueur2[0]
        joueur2.rect.y = pos_joueur2[1]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continuer = False
                pygame.quit()

        # Gestion du déplacement du joueur et des interactions
        joueur.deplacer()

        # Mise à jour et affichage des éléments de jeu (carte, collisions, etc.)
        fenetre.fill((255, 255, 255))  # Efface l'écran
        draw_map(fenetre, tmx_data)  # Affichage de la carte
        circleZone()  # Affichage des zones de collision
        take()  # Gestion des interactions
        for item in items:
            item.draw(fenetre)  # Affichage des objets du jeu
        checkItemCollisions(joueur, items)  # Vérification des collisions avec les objets
        redessiner_fenetre(fenetre, joueur, joueur2)  # Affichage des joueurs

        pygame.display.update()

main()
