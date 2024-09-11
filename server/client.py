import pygame
import os
from network import Network
import pytmx

# Définir la largeur et la hauteur de la fenêtre
largeur = 1024
hauteur = 768
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Client Multijoueur")
pygame.font.init()

# Charger la carte une seule fois pour réduire le nombre de chargements
tmx_data = pytmx.util_pygame.load_pygame("../game/assets/map/export_map/1.tmx")

# Charger les polices
titlefont = pygame.font.Font("../game/assets/fonts/RETROTECH.ttf", 72)
textFont = pygame.font.Font("../game/assets/fonts/RETROTECH.ttf", 48)
parentheseFont = pygame.font.Font("../game/assets/fonts/RETROTECH.ttf", 24)

# Couleurs
GRIS = (229, 231, 230)
ORANGE_PALE = (238, 230, 216)
MARRON_FONCE = (147, 68, 26)

# États de jeu
class GameState:
    ENTRYPOINT = 0
    CHOOSE_PSEUDO = 1
    SELECTING_COUNTRY = 2
    IN_GAME = 6

gamestate = GameState.ENTRYPOINT
name = ""  # Pseudo du joueur
selected_country = None  # Pays choisi

# Classe Joueur
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        chemin_image = os.path.join(os.path.dirname(__file__), '../game/assets/testPlayer.png')
        self.image = pygame.image.load(chemin_image)
        self.image = pygame.transform.scale(self.image, (32, 32))  # Redimensionner l'image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vitesse = 3

    def dessiner(self, fenetre):
        fenetre.blit(self.image, self.rect)

    def deplacer(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.vitesse
        if keys[pygame.K_RIGHT] and self.rect.x < 1000:
            self.rect.x += self.vitesse
        if keys[pygame.K_UP] and self.rect.y > 0:
            self.rect.y -= self.vitesse
        if keys[pygame.K_DOWN] and self.rect.y < 744:
            self.rect.y += self.vitesse


# Fonction pour lire une position à partir d'une chaîne de caractères
def lire_position(chaine):
    chaine = chaine.split(",")
    return int(chaine[0]), int(chaine[1])


# Fonction pour dessiner la carte une seule fois
def draw_map_once(screen, tmx_data):
    tile_width = tmx_data.tilewidth
    tile_height = tmx_data.tileheight
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    screen.blit(tile, (x * tile_width, y * tile_height))
    pygame.display.update()


# Fonction pour redessiner uniquement les joueurs
def redessiner_fenetre(fenetre, joueur, joueur2):
    joueur.dessiner(fenetre)
    joueur2.dessiner(fenetre)
    pygame.display.update()


# Affichage du menu principal
def initMenu():
    background = pygame.image.load("../game/assets/menu-background.png")
    titletext = titlefont.render("Concorde", False, (0, 0, 0))
    titletext_rect = titletext.get_rect()
    titletext_rect.center = (largeur / 2, hauteur / 4)

    debut_image = pygame.image.load("../game/assets/btn_start.png")
    debut_image = pygame.transform.scale(debut_image, (246, 78))
    debutButton = pygame.Rect(largeur / 2 - 123, hauteur / 2, 246, 78)

    fenetre.blit(background, (0, 0))
    fenetre.blit(titletext, titletext_rect)
    fenetre.blit(debut_image, debutButton.topleft)

    pygame.display.update()

    return debutButton


# Affichage de la sélection du pseudo
def choosePseudo(name):
    titletext = titlefont.render("Choisir un pseudo", False, (0, 0, 0))
    titletext_rect = titletext.get_rect()
    titletext_rect.center = (largeur / 2, hauteur / 4)

    pseudoUser = textFont.render(name, False, (0, 0, 0))
    pseudoUser_rect = pseudoUser.get_rect()
    pseudoUser_rect.center = (largeur / 2, 420)

    parentheseText = parentheseFont.render("(18 char max)", False, (0, 0, 0))
    parentheseText_rect = parentheseText.get_rect()
    parentheseText_rect.center = (largeur / 2, 365)

    fenetre.fill(ORANGE_PALE)
    pygame.draw.rect(fenetre, (GRIS), (largeur / 4, hauteur / 2, 512, 64))
    fenetre.blit(titletext, titletext_rect)
    fenetre.blit(pseudoUser, pseudoUser_rect)
    fenetre.blit(parentheseText, parentheseText_rect)

    valider_image = pygame.image.load("../game/assets/btn_valider.png")
    valider_image = pygame.transform.scale(valider_image, (246, 78))
    validerButton = pygame.Rect(largeur / 2 - 123, hauteur / 1.25, 246, 78)

    fenetre.blit(valider_image, validerButton.topleft)
    pygame.display.update()

    return validerButton


# Affichage de la sélection du pays
def selectCountry():
    global selected_country
    imgPlayer = pygame.image.load("../game/assets/testPlayer.png")
    imgPlayer = pygame.transform.scale(imgPlayer, (256, 256))

    # Drapeaux des pays
    france_img = pygame.image.load("../game/assets/france.png")
    allemagne_img = pygame.image.load("../game/assets/allemagne.png")
    uk_img = pygame.image.load("../game/assets/uk.png")
    eu_img = pygame.image.load("../game/assets/etats_unis.png")
    chine_img = pygame.image.load("../game/assets/chine.png")
    russie_img = pygame.image.load("../game/assets/russie.png")

    pays_images = [(france_img, (largeur / 6, hauteur / 3)), (uk_img, (largeur / 2, hauteur / 3)),
                   (eu_img, (largeur / 1.25, hauteur / 3)), (allemagne_img, (largeur / 6, hauteur / 1.75)),
                   (chine_img, (largeur / 2, hauteur / 1.75)), (russie_img, (largeur / 1.25, hauteur / 1.75))]

    titletext = titlefont.render("Selectionner un pays", False, (0, 0, 0))
    titletext_rect = titletext.get_rect()
    titletext_rect.center = (largeur / 2, hauteur / 8)

    fenetre.fill(ORANGE_PALE)
    pygame.draw.rect(fenetre, MARRON_FONCE, (largeur / 4, hauteur / 1.1, 256, 32))
    fenetre.blit(titletext, titletext_rect)

    for img, pos in pays_images:
        fenetre.blit(img, pos)

    pygame.display.update()

    return pays_images  # On renvoie les images pour qu'elles soient détectées lors de clic


# Fonction principale du client
# Fonction principale du client
def main():
    global gamestate, name, selected_country
    continuer = True
    reseau = Network()

    joueur = Player(125, 680)  # Position par défaut
    joueur2 = Player(0, 0)

    horloge = pygame.time.Clock()

    # Dessiner la carte une fois au début
    draw_map_once(fenetre, tmx_data)

    while continuer:
        horloge.tick(60)  # Augmentation des FPS à 60 pour une meilleure fluidité

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continuer = False
                pygame.quit()

            # Gestion du pseudo
            if gamestate == GameState.CHOOSE_PSEUDO:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    elif len(name) <= 18 and event.unicode.isprintable():
                        name += event.unicode
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    validerButton = choosePseudo(name)
                    if validerButton.collidepoint(event.pos):
                        gamestate = GameState.SELECTING_COUNTRY

        # Affichage et gestion du menu principal
        if gamestate == GameState.ENTRYPOINT:
            debutButton = initMenu()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if debutButton.collidepoint(event.pos):
                    gamestate = GameState.CHOOSE_PSEUDO

        # Affichage et gestion de la sélection du pays
        elif gamestate == GameState.SELECTING_COUNTRY:
            pays_images = selectCountry()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Ici vous placez le nouveau code pour détecter les clics sur les pays
                for i, (img, pos) in enumerate(pays_images):
                    rect = img.get_rect(topleft=pos)
                    if rect.collidepoint(event.pos):
                        selected_country = i  # Sélectionner le pays
                        gamestate = GameState.IN_GAME

        # Jeu principal
        elif gamestate == GameState.IN_GAME:
            try:
                # Envoi des données du joueur (position, pseudo, pays) au serveur
                data_joueur2 = reseau.send_data((joueur.rect.x, joueur.rect.y), name, selected_country)
                pos_joueur2 = lire_position(data_joueur2[0])
                joueur2.rect.x = pos_joueur2[0]
                joueur2.rect.y = pos_joueur2[1]
            except:
                print("Erreur de réception des données")
                continue

            # Gestion du déplacement du joueur
            joueur.deplacer()

            # Redessiner uniquement les joueurs
            redessiner_fenetre(fenetre, joueur, joueur2)


main()




