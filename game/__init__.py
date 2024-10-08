import pygame
import pytmx
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game.objects.ClicGame import ClicGame
from game.objects.mapItem import MapItem
from game.objects import GameState
from game.objects import Competences
from game.objects.player import Player
from game.objects.button import Button
from game.objects.QTE import QTE
from game.objects.Pays import Pays
from game.objects.Structure import Structure
import random

from game.objects.mapItem import MapItem
from server.network import Network

music_started = False
pygame.init()
window_width = 1024
window_height = 768
window = pygame.display.set_mode((window_width, window_height))
clock = pygame.time.Clock()
running = True
name = ""
gamestate = GameState.GameState.ENTRYPOINT
time_diff = pygame.time.get_ticks()
minigame = False
started = False

titlefont = pygame.font.Font("./assets/fonts/RETROTECH.ttf", 72)
littleTitlefont = pygame.font.Font("./assets/fonts/RETROTECH.ttf", 52)
textFont = pygame.font.Font("./assets/fonts/RETROTECH.ttf", 48)
parentheseFont = pygame.font.Font("./assets/fonts/RETROTECH.ttf", 24)
statPoleFont = pygame.font.Font("./assets/fonts/RETROTECH.ttf", 12)
starFont = pygame.font.Font("./assets/fonts/RETROTECH.ttf", 12)

GRIS = (229, 231, 230)
ORANGE_PALE = (238, 230, 216)
MARRON_FONCE = (147, 68, 26)

ruleBtn = Button(260, 680, pygame.image.load("assets/btn_regle_496.png"))
startButton = Button(window_width / 1.6, window_height / 1.50, pygame.image.load("./assets/btn_start.png"))
creditButton = Button(1000, 680, pygame.image.load("./assets/credits.png"))
backButton = Button(300, 200, pygame.image.load("./assets/retour.png"))
replayBtn = Button(630, 530, pygame.image.load("assets/btn_rejouer496.png"))

backButton.image = pygame.transform.scale(backButton.image, (150, 106))
nameButton = Button(window_width / 1.6, window_height / 1.25, pygame.image.load("./assets/btn_valider.png"))
countryBtnconfirm = Button(window_width / 1.1, window_height / 1.1, pygame.image.load("./assets/btn_valider.png"))
countryBtnconfirm.image = pygame.transform.scale(nameButton.image, (246, 78))
startButton.image = pygame.transform.scale(startButton.image, (246, 78))
creditButton.image = pygame.transform.scale(creditButton.image, (246, 78))
ruleBtn.image = pygame.transform.scale(ruleBtn.image, (246, 78))
nameButton.image = pygame.transform.scale(nameButton.image, (246, 78))
replayBtn.image = pygame.transform.scale(replayBtn.image, (246, 78))

competences_france = {0: 0.8, 1: 1.4, 2: 1, 3: 1.2, 4: 1, 5: 1}
competences_allemagne = {0: 1.3, 1: 1, 2: 1, 3: 1, 4: 0.8, 5: 1}
competences_chine = {0: 1.5, 1: 0.8, 2: 1.4, 3: 1.2, 4: 1.2, 5: 1.2}

france = Pays("France", competences_france, pygame.image.load("assets/france.png"), None,
              pygame.image.load("./assets/sprite_france/run_down_fr/sprite_0.png"))
allemagne = Pays("Allemagne", competences_allemagne, pygame.image.load("assets/allemagne.png"), None,
                 pygame.image.load("./assets/sprite_allemagne/run_down_all/sprite_0.png"))
angleterre = Pays("Angleterre", competences_france, pygame.image.load("assets/uk.png"), None,
                  pygame.image.load("./assets/sprite_france/run_down_fr/sprite_0.png"))
chine = Pays("Chine", competences_chine, pygame.image.load("assets/chine.png"), None,
             pygame.image.load("./assets/sprite_chine/run_down_chine/sprite_0.png"))
eu = Pays("Etat-unis", competences_france, pygame.image.load("assets/etats_unis.png"), None,
          pygame.image.load("./assets/sprite_france/run_down_fr/sprite_0.png"))
russie = Pays("Russie", competences_france, pygame.image.load("assets/russie.png"), None,
              pygame.image.load("./assets/sprite_russie/run_down_ru/sprite_0.png"))

pays = [france, allemagne, angleterre, chine, eu, russie]
selected_country = None
selected_country_nation = None
tmx_data = pytmx.util_pygame.load_pygame("assets/map/tileset/1.tmx")
take_speed = 5
col_active = False
count_struc_complete = 0
list_struc_complete = []

list_qte_obj = ["./assets/qte-object/bookv2.png",
                "./assets/qte-object/fuel_tank.png",
                "./assets/qte-object/raquette.png",
                "./assets/qte-object/statue9.png"]
images_sprite_france = [pygame.image.load("./assets/sprite_france/run_down_fr/sprite_0.png"),
                        pygame.image.load("./assets/sprite_france/run_down_fr/sprite_1.png"),
                        pygame.image.load("./assets/sprite_france/run_left_fr/sprite_0.png"),
                        pygame.image.load("./assets/sprite_france/run_left_fr/sprite_1.png"),
                        pygame.image.load("./assets/sprite_france/run_right_fr/sprite_0.png"),
                        pygame.image.load("./assets/sprite_france/run_right_fr/sprite_1.png"),
                        pygame.image.load("./assets/sprite_france/run_up_fr/sprite_0.png"),
                        pygame.image.load("./assets/sprite_france/run_up_fr/sprite_1.png")]

images_sprite_allemagne = [pygame.image.load("./assets/sprite_allemagne/run_down_all/sprite_0.png"),
                           pygame.image.load("./assets/sprite_allemagne/run_down_all/sprite_1.png"),
                           pygame.image.load("./assets/sprite_allemagne/run_left_all/sprite_0.png"),
                           pygame.image.load("./assets/sprite_allemagne/run_left_all/sprite_1.png"),
                           pygame.image.load("./assets/sprite_allemagne/run_right_all/sprite_0.png"),
                           pygame.image.load("./assets/sprite_allemagne/run_right_all/sprite_1.png"),
                           pygame.image.load("./assets/sprite_allemagne/run_up_all/sprite_0.png"),
                           pygame.image.load("./assets/sprite_allemagne/run_up_all/sprite_1.png")]

images_sprite_chine = [pygame.image.load("./assets/sprite_chine/run_down_chine/sprite_0.png"),
                       pygame.image.load("./assets/sprite_chine/run_down_chine/sprite_1.png"),
                       pygame.image.load("./assets/sprite_chine/run_left_chine/sprite_0.png"),
                       pygame.image.load("./assets/sprite_chine/run_left_chine/sprite_1.png"),
                       pygame.image.load("./assets/sprite_chine/run_right_chine/sprite_0.png"),
                       pygame.image.load("./assets/sprite_chine/run_right_chine/sprite_1.png"),
                       pygame.image.load("./assets/sprite_chine/run_up_chine/sprite_0.png"),
                       pygame.image.load("./assets/sprite_chine/run_up_chine/sprite_1.png")]

images_sprite_russie = [pygame.image.load("./assets/sprite_russie/run_down_ru/sprite_0.png"),
                        pygame.image.load("./assets/sprite_russie/run_down_ru/sprite_1.png"),
                        pygame.image.load("./assets/sprite_russie/run_left_ru/sprite_0.png"),
                        pygame.image.load("./assets/sprite_russie/run_left_ru/sprite_1.png"),
                        pygame.image.load("./assets/sprite_russie/run_right_ru/sprite_0.png"),
                        pygame.image.load("./assets/sprite_russie/run_right_ru/sprite_1.png"),
                        pygame.image.load("./assets/sprite_russie/run_up_ru/sprite_0.png"),
                        pygame.image.load("./assets/sprite_russie/run_up_ru/sprite_1.png")]

images_qte_ressource = [pygame.image.load("./assets/image_qte_ressource/image_QTE_essence.png"),
                        pygame.image.load("./assets/image_qte_ressource/image_QTE_essence-f2.png")]
image_qte_musee = [pygame.image.load("./assets/musee_qte.png")]
image_qte_banque = [pygame.image.load("./assets/banque_qte.png")]
ecole_qte = [pygame.image.load("./assets/ecole_qte.png")]
stade_qte = [pygame.image.load("./assets/terrain_foot_qte.png")]
player = Player(125, 680, competences_france, 60, None, images_sprite_france, 0)

imgPlayer = france.imgPlayer
imgPlayer = pygame.transform.scale(imgPlayer, (192, 192))

player2 = Player(125, 680, competences_allemagne, 60, None, images_sprite_allemagne, 0)
imgPlayer2 = allemagne.imgPlayer
imgPlayer = pygame.transform.scale(imgPlayer, (192, 192))

hopital = Structure("hopital", Competences.Competences.SANTE, 100, 100, None, False, 0, 0, False, False)
ecole = Structure("ecole", Competences.Competences.EDUCATION, 100, 100, None, False, 0, 0, False, False)
banque = Structure("banque", Competences.Competences.FINANCE, 100, 100, None, False, 0, 0, False, False)
puit = Structure("puit", Competences.Competences.RESSOURCES, 100, 100, None, False, 0, 0, False, False)
stade = Structure("stade", Competences.Competences.SPORT, 100, 100, None, False, 0, 0, False, False)
musee = Structure("musee", Competences.Competences.CULTURE, 100, 100, None, False, 0, 0, False, False)

strucGroupe = [musee, hopital, ecole, stade, puit, banque]
layer_mer2 = {"mer 2": False}


# prendre une chaine de caractères et en déduire une position
def lire_position(chaine):
    chaine = chaine.split(",")
    return int(chaine[0]), int(chaine[1])


# prendre une chaine et en déduire les infos d'un batiment
def lire_batiment(chaine):
    chaine = chaine.split(",")
    return ()


# update la fenêtre pour les joueurs
def redraw(window, player, player2):
    # on réaffiche les sprites
    window.blit(player.image, player.rect)
    window.blit(player2.image, player2.rect)
    # et on update le tout
    pygame.display.update()


addStar = False
checked = False
not_sel_qte = False
qte_ressource = QTE(7000, False, images_qte_ressource)
qte_culture = QTE(7000, False, image_qte_musee)
qte_banque = QTE(7000, False, image_qte_banque)
qte_ecole = QTE(7000, False, ecole_qte)
qte_stade = QTE(7000, False, stade_qte)

qtes = [qte_culture, qte_stade, qte_ecole, qte_banque, qte_ressource]


def draw_map(screen, tmx_data):
    global layer_mer2
    tile_width = tmx_data.tilewidth
    tile_height = tmx_data.tileheight

    for layer in tmx_data.visible_layers:
        bad_layer = False
        if layer.name == "mer 2" and not layer_mer2["mer 2"]:
            bad_layer = True
        if not bad_layer:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        screen.blit(tile, (x * tile_width, y * tile_height))
    if layer_mer2["mer 2"]:
        layer_mer2["mer 2"] = False
    else:
        layer_mer2["mer 2"] = True


def get_collision_tiles(tmx_data, layer_name):
    collision_tiles = []
    layer = tmx_data.get_layer_by_name(layer_name)
    if isinstance(layer, pytmx.TiledTileLayer):
        for x, y, gid in layer:
            if gid != 0:
                collision_tiles.append(pygame.Rect(x * tmx_data.tilewidth,
                                                   y * tmx_data.tileheight,
                                                   tmx_data.tilewidth,
                                                   tmx_data.tileheight))
    return collision_tiles


def initMenu():
    background = pygame.image.load("./assets/menu-background.png")
    imgTitre = pygame.image.load("./assets/imgTitre.png")
    imgTitre = pygame.transform.scale(imgTitre, (500, 93))

    window.blit(background, (0, 0))
    window.blit(imgTitre, (window_width / 4, window_height / 4))
    startButton.draw(window)
    creditButton.draw(window)
    ruleBtn.draw(window)


def initRule():
    background = pygame.image.load("./assets/menu-background.png")
    titletext = titlefont.render("Regles", False, (0, 0, 0))
    titletext_rect = titletext.get_rect()
    titletext_rect.center = (window_width / 2, window_height / 8 - 50)

    regleText = (
        "Alors que les differentes nations |du monde sont en pleine expansion,| plusieurs territoires |sont encore a departager !| A vous de montrer que votre pays |est le plus a meme| a obtenir ces terres. |explorer la map| et augmentez vos competences | afin de prendre possesion |des differente structure du territoire | pour gagner la partie :)")
    lines = regleText.split('|')
    y_offset = window_height / 6

    window.blit(background, (0, 0))
    window.blit(titletext, titletext_rect)
    backButton.draw(window)

    for line in lines:
        content = textFont.render(line, False, (0, 0, 0))
        window.blit(content, (window_width / 2 - content.get_width() / 2, y_offset))
        y_offset += content.get_height() + 10


def initCredits():
    background = pygame.image.load("./assets/menu-background.png")

    titletext = titlefont.render("Credits", False, (0, 0, 0))
    titletext_rect = titletext.get_rect()
    titletext_rect.center = (window_width / 2, window_height / 6)

    sourcetitle = titlefont.render("Sources", False, (0, 0, 0))
    sourcetitle_rect = sourcetitle.get_rect()
    sourcetitle_rect.center = (window_width, window_height)

    devcontent = ("Yanis Harkati : Developpeur|"
                  "Ilan Darmon : Developpeur|"
                  "Rachel Peretti : Developpeuse|"
                  "Idibei Hamid : Administrateur reseau|"
                  "Tom Jochum : Directeur artistique")

    devlines = devcontent.split('|')

    sourcecontent = ("Ecole : poppants|"
                     "Decor : schwarnhild|"
                     "Terrain de foot : davidevitali|")

    sourcelines = sourcecontent.split("|")

    window.blit(background, (0, 0))
    window.blit(titletext, titletext_rect)
    backButton.draw(window)
    y_offset = window_height / 4
    for line in devlines:
        content = textFont.render(line, False, (0, 0, 0))
        window.blit(content, (window_width / 2 - content.get_width() / 2, y_offset))
        y_offset += content.get_height() + 10

    for line in sourcelines:
        content = textFont.render(line, False, (0, 0, 0))
        window.blit(content, (window_width / 2 - content.get_width() / 2, y_offset))
        y_offset += content.get_height() + 10


def choosePseudo(name):
    titletext = titlefont.render("Choisir un pseudo", False, (0, 0, 0))
    titletext_rect = titletext.get_rect()
    titletext_rect.center = (window_width / 2, window_height / 4)
    pseudoUser = textFont.render(name, False, (0, 0, 0))
    pseudoUser_rect = pseudoUser.get_rect()
    pseudoUser_rect.center = (window_width / 2, 420)
    parentheseText = parentheseFont.render("(18 char max)", False, (0, 0, 0))
    parentheseText_rect = parentheseText.get_rect()
    parentheseText_rect.center = (window_width / 2, 365)
    window.fill(MARRON_FONCE)
    pygame.draw.rect(window, (GRIS), (window_width / 4, window_height / 2, 512, 64))
    window.blit(titletext, titletext_rect)
    window.blit(pseudoUser, pseudoUser_rect)
    window.blit(parentheseText, parentheseText_rect)
    nameButton.draw(window)


def generate_items(length):
    items = []

    musee.coll_zone = get_collision_tiles(tmx_data, "culture_zone")
    hopital.coll_zone = get_collision_tiles(tmx_data, "hopital_zone")
    ecole.coll_zone = get_collision_tiles(tmx_data, "ecole_zone")
    stade.coll_zone = get_collision_tiles(tmx_data, "stade_zone")
    puit.coll_zone = get_collision_tiles(tmx_data, "puit_zone")
    banque.coll_zone = get_collision_tiles(tmx_data, "banque_zone")
    batiments = get_collision_tiles(tmx_data, "batiments")
    palmier = get_collision_tiles(tmx_data, "palmier")
    bordure = get_collision_tiles(tmx_data, "bordure")
    mer = get_collision_tiles(tmx_data, "mer")
    strucGroupe = [musee.coll_zone, hopital.coll_zone, ecole.coll_zone, stade.coll_zone, puit.coll_zone,
                   banque.coll_zone, batiments, palmier, bordure, mer]

    for k in range(length):
        x = random.randint(0, window_width - 32)  # Limite de la fenêtre
        y = random.randint(0, window_height - 32)
        index = random.randint(0, 3)
        item = MapItem(x, y, pygame.image.load(list_qte_obj[index]))
        for structure in strucGroupe:
            for tile in structure:
                while item.rect.colliderect(tile):
                    x = random.randint(0, window_width - 32)  # Limite de la fenêtre
                    y = random.randint(0, window_height - 32)
                    index = random.randint(0, 3)
                    item = MapItem(x, y, pygame.image.load(list_qte_obj[index]))

        items.append(item)
    return items


def selectCountry():
    global selected_country
    global imgPlayer
    titletext = titlefont.render("Selectionnez un pays", False, (0, 0, 0))
    titletext_rect = titletext.get_rect()
    titletext_rect.center = (window_width / 2, window_height / 8)

    frBtn = Button(window_width / 6, window_height / 3, france.img)
    france.btn = frBtn
    ukBtn = Button(window_width / 2, window_height / 3, angleterre.img)
    angleterre.btn = ukBtn
    euBtn = Button(window_width / 1.25, window_height / 3, eu.img)
    eu.btn = euBtn
    allemagneBtn = Button(window_width / 6, window_height / 1.75, allemagne.img)
    allemagne.btn = allemagneBtn
    chineBtn = Button(window_width / 2, window_height / 1.75, chine.img)
    chine.btn = chineBtn
    russieBtn = Button(window_width / 1.25, window_height / 1.75, russie.img)
    russie.btn = russieBtn

    window.fill(MARRON_FONCE)

    pygame.draw.rect(window, MARRON_FONCE, (window_width / 4, window_height / 1.1, 256, 32))
    for country in pays:
        if country.btn.isHovered():
            country.btn.image = pygame.transform.scale(country.btn.image, (235, 160))
        if country.btn.isClicked():
            selected_country = country
            imgPlayer = selected_country.imgPlayer
            imgPlayer = pygame.transform.scale(imgPlayer, (192, 192))
        country.btn.draw(window)
        if selected_country:
            countryBtnconfirm.draw(window)
            window.blit(imgPlayer, (window_width / 4, window_height / 1.6))
    window.blit(titletext, titletext_rect)


def circleZone():
    collision_tiles_musee = get_collision_tiles(tmx_data, "culture_cercle")
    collision_tiles_hopital = get_collision_tiles(tmx_data, "hopital_cercle")
    collision_tiles_ecole = get_collision_tiles(tmx_data, "ecole_cercle")
    collision_tiles_sport = get_collision_tiles(tmx_data, "stade_cercle")
    collision_tiles_puit = get_collision_tiles(tmx_data, "puit_cercle")
    collision_tiles_banque = get_collision_tiles(tmx_data, "banque_cercle")

    collision_tiles = collision_tiles_musee + collision_tiles_hopital + collision_tiles_ecole + collision_tiles_sport + collision_tiles_puit + collision_tiles_banque
    for tile in collision_tiles:
        s = pygame.Surface((32, 32))
        s.set_alpha(70)
        s.fill((50, 158, 168))
        window.blit(s, (tile.x, tile.y))


def statPole(player1):
    global selected_country
    toolPole = pygame.Rect(330, 700, 400, 60)
    pygame.draw.rect(window, MARRON_FONCE, toolPole)
    pygame.draw.rect(window, (186, 88, 35), toolPole, 5)
    count = 0
    parentheseText = statPoleFont.render(f" Etoile : {player1.etoile} *", False, ORANGE_PALE)
    parentheseText_rect = parentheseText.get_rect()
    parentheseText_rect.center = (650, 720)
    window.blit(parentheseText, parentheseText_rect)
    for cle in selected_country.competences.keys():
        if count <= 2:
            parentheseText = statPoleFont.render(
                f"{Competences.Competences(cle).name} : {selected_country.competences[cle]}", False, (0, 0, 0))
            parentheseText_rect = parentheseText.get_rect()
            parentheseText_rect.center = (382 + count * 90, 720)
            window.blit(parentheseText, parentheseText_rect)
        else:
            parentheseText = statPoleFont.render(
                f"{Competences.Competences(cle).name} : {selected_country.competences[cle]}", False, (0, 0, 0))
            parentheseText_rect = parentheseText.get_rect()
            parentheseText_rect.center = (370 + (count - 3) * 90, 740)
            window.blit(parentheseText, parentheseText_rect)
        count += 1


qte = qte_ressource


def checkItemCollisions(player, items):
    global started
    global checked
    global not_sel_qte
    global qte
    timer_event = pygame.USEREVENT + 1

    if not not_sel_qte:
        for i in range(len(qtes) - 1):
            x = random.randint(0, len(qtes) - 1)
            qte = qtes[x]
            not_sel_qte = True

    for item in items:
        if player.rect.colliderect(item.rect):
            started = True
            items.remove(item)
            pygame.time.set_timer(timer_event, qte_ressource.duree)
        if started:
            qte.start(window_width, window_height, GRIS, window, textFont, player)
        if event.type == timer_event:
            qte.isFinish = True
            not_sel_qte = False
            started = False
            pygame.time.set_timer(timer_event, 0)


def take():
    global take_speed
    global time_diff
    global strucGroupe
    musee.coll_zone = get_collision_tiles(tmx_data, "culture_zone")
    hopital.coll_zone = get_collision_tiles(tmx_data, "hopital_zone")
    ecole.coll_zone = get_collision_tiles(tmx_data, "ecole_zone")
    stade.coll_zone = get_collision_tiles(tmx_data, "stade_zone")
    puit.coll_zone = get_collision_tiles(tmx_data, "puit_zone")
    banque.coll_zone = get_collision_tiles(tmx_data, "banque_zone")
    strucGroupe = [musee, hopital, ecole, stade, puit, banque]
    # joueur 1
    pygame.draw.rect(window, GRIS, (150, 300, 100, 20))
    pygame.draw.rect(window, GRIS, (210, 10, 100, 20))
    pygame.draw.rect(window, GRIS, (450, 10, 100, 20))
    pygame.draw.rect(window, GRIS, (550, 230, 100, 20))
    pygame.draw.rect(window, GRIS, (850, 50, 100, 20))
    pygame.draw.rect(window, GRIS, (700, 600, 100, 20))

    pygame.draw.rect(window, (50, 158, 168), (150, 300, musee.charge_state_1, 20))
    pygame.draw.rect(window, (50, 158, 168), (210, 10, ecole.charge_state_1, 20))
    pygame.draw.rect(window, (50, 158, 168), (450, 10, banque.charge_state_1, 20))
    pygame.draw.rect(window, (50, 158, 168), (550, 230, stade.charge_state_1, 20))
    pygame.draw.rect(window, (50, 158, 168), (850, 50, hopital.charge_state_1, 20))
    pygame.draw.rect(window, (50, 158, 168), (700, 600, puit.charge_state_1, 20))

    # joueur 2

    pygame.draw.rect(window, GRIS, (150, 270, 100, 20))
    pygame.draw.rect(window, GRIS, (210, 40, 100, 20))
    pygame.draw.rect(window, GRIS, (450, 40, 100, 20))
    pygame.draw.rect(window, GRIS, (550, 200, 100, 20))
    pygame.draw.rect(window, GRIS, (850, 20, 100, 20))
    pygame.draw.rect(window, GRIS, (700, 570, 100, 20))

    pygame.draw.rect(window, (168, 32, 5), (150, 270, musee.charge_state_2, 20))
    pygame.draw.rect(window, (168, 32, 5), (210, 40, ecole.charge_state_2, 20))
    pygame.draw.rect(window, (168, 32, 5), (450, 40, banque.charge_state_2, 20))
    pygame.draw.rect(window, (168, 32, 5), (550, 200, stade.charge_state_2, 20))
    pygame.draw.rect(window, (168, 32, 5), (850, 20, hopital.charge_state_2, 20))
    pygame.draw.rect(window, (168, 32, 5), (700, 570, puit.charge_state_2, 20))
    anyCol = False
    anyCol_2 = False
    for structure in strucGroupe:
        for tile in structure.coll_zone:
            charge_tap = player.competences[structure.competence.value] * player.etoile

            if player.rect.colliderect(tile) and not structure.isCLaim:
                anyCol = True
                if not structure.col_active_1:
                    structure.col_active_1 = True
                else:
                    previous_charge = structure.charge_state_1
                    if structure.charge_state_1 < structure.lifePole:
                        structure.charge_state_1 += charge_tap
                        print(f"charge_state: {structure.charge_state_1}, lifePole: {structure.lifePole}")

                    if structure.charge_state_1 >= structure.lifePole and structure.col_active_1:
                        structure.isCLaim = True
                        structure.col_active_1 = False
                        diff = structure.lifePole - previous_charge
                        player.etoile -= diff
                        structure.charge_state_1 = structure.lifePole
                        print("Structure revendiquée")
                    else:
                        if player.etoile > 0:
                            player.etoile = 0
                        print(f"Étoiles restantes : {player.etoile}")
            elif not player.rect.colliderect(tile) and not structure.isCLaim:
                structure.col_active_1 = False

    if not anyCol and structure.col_active_1:
        structure.col_active = False
        print(f"Collision terminée : {structure.col_active_1}")
        ########################################################################
    #################################################################################
    for structure in strucGroupe:
        for tile in structure.coll_zone:
            charge_tap_2 = player2.competences[structure.competence.value] * player2.etoile

            if player2.rect.colliderect(tile) and not structure.isCLaim:
                anyCol_2 = True
                if not structure.col_active_2:
                    structure.col_active_2 = True
                else:
                    previous_charge = structure.charge_state_2
                    if structure.charge_state_2 < structure.lifePole_2:
                        structure.charge_state_2 += charge_tap_2
                        print(f"charge_state: {structure.charge_state_2}, lifePole: {structure.lifePole_2}")

                    if structure.charge_state_2 >= structure.lifePole_2 and structure.col_active_2:
                        structure.isCLaim = True
                        structure.col_active_2 = False
                        diff = structure.lifePole_2 - previous_charge
                        player2.etoile -= diff
                        structure.charge_state_2 = structure.lifePole_2
                        print("Structure revendiquée")
                    else:
                        if player2.etoile > 0:
                            player2.etoile = 0
                        print(f"Étoiles restantes : {player2.etoile}")
            elif not player2.rect.colliderect(tile) and not structure.isCLaim:
                structure.col_active_2 = False

        if not anyCol_2 and structure.col_active_2:
            structure.col_active_2 = False
            print(f"Collision terminée : {structure.col_active_2}")


items = generate_items(20)


def inList(list, elem):
    for l in list:
        if l == elem:
            return True
    return False


# initialiser
networkStatus = False
network = None


def inGame():
    global count_struc_complete
    global gamestate
    global list_struc_complete
    global networkStatus
    global network

    # si la connection n'est pas ouverte
    if not networkStatus:
        network = Network()  # on l'ouvre
        # et récupérer les positions des joueurs
        position_depart = lire_position(network.getPos())
        # debug
        print(f"Position de départ : {position_depart}")
        networkStatus = True  # pour éviter de l'ouvrir 20 fois en boucle ^^

    global checked
    player.country = selected_country
    player.competences = player.country.competences
    if player.country == allemagne:
        player.images = images_sprite_allemagne
    elif player.country == chine:
        player.images = images_sprite_chine
    elif player.country == russie:
        player.images == images_sprite_russie
    draw_map(window, tmx_data)
    collision_tilesBatiment = get_collision_tiles(tmx_data, "batiments")
    collision_tilesPalmier = get_collision_tiles(tmx_data, "palmier")
    collision_tilesBordure = get_collision_tiles(tmx_data, "bordure")
    collision_tilesMer = get_collision_tiles(tmx_data, "mer")

    collision_tiles = collision_tilesBatiment + collision_tilesPalmier + collision_tilesBordure + collision_tilesMer
    previous_position = player.rect.copy()
    player.deplacer()
    for tile in collision_tiles:
        if player.rect.colliderect(tile):
            player.rect = previous_position
    window.blit(player.image, player.rect)
    circleZone()
    take()
    statPole(player)

    for item in items:
        item.draw(window)
    checkItemCollisions(player, items)

    try:
        data_player2 = network.sendPlayerData((player.rect.x, player.rect.y), 'pseudo', 'France')
        pos_player2 = lire_position(data_player2[0])
        pseudo_player2 = data_player2[1]
        country_player2 = data_player2[2]
    except:
        print("erreur!!")
        pass

    # update la pos du joueur 2
    player2.rect.x = pos_player2[0]
    player2.rect.y = pos_player2[1]

    # si on est en jeu on affiche les sprites des joueurs
    # pour pas que ça s'affiche sur l'écran principal/dès qu'il y a connexion
    if gamestate == gamestate.IN_GAME:
        # update les sprites des joueurs
        redraw(window, player, player2)

    for struc in strucGroupe:
        if struc.isCLaim and not inList(list_struc_complete, struc):
            count_struc_complete += 1
            list_struc_complete.append(struc)
            print(count_struc_complete)

    if count_struc_complete == 6:
        gamestate = GameState.GameState.WIN


def resetGame():
    global music_started
    global minigame
    global selected_country
    global selected_country_nation
    global col_active
    global count_struc_complete
    global list_struc_complete
    global player
    global imgPlayer
    global hopital
    global banque
    global ecole
    global puit
    global stade
    global musee
    global items
    music_started = False
    minigame = False
    selected_country = None
    selected_country_nation = None
    col_active = False
    count_struc_complete = 0
    list_struc_complete = []

    player = Player(125, 680, competences_france, 60, None, images_sprite_france, 0)
    imgPlayer = france.imgPlayer
    imgPlayer = pygame.transform.scale(imgPlayer, (192, 192))

    hopital = Structure("hopital", Competences.Competences.SANTE, 100, 100, None, False, 0, 0, False, False)
    ecole = Structure("ecole", Competences.Competences.EDUCATION, 100, 100, None, False, 0, 0, False, False)
    banque = Structure("banque", Competences.Competences.FINANCE, 100, 100, None, False, 0, 0, False, False)
    puit = Structure("puit", Competences.Competences.RESSOURCES, 100, 100, None, False, 0, 0, False, False)
    stade = Structure("stade", Competences.Competences.SPORT, 100, 100, None, False, 0, 0, False, False)
    musee = Structure("musee", Competences.Competences.CULTURE, 100, 100, None, False, 0, 0, False, False)
    items = []
    items = generate_items(20)


def initWin():
    global gamestate
    global music_started
    s = pygame.Surface((window_width / 2, window_height / 2))
    s.set_alpha(70)
    s.fill(GRIS)
    titletext = littleTitlefont.render("Vous gagnez la partie", False, (0, 0, 0))
    titletext_rect = titletext.get_rect()
    titletext_rect.center = (window_width / 2, window_height / 3)
    if replayBtn.isClicked():
        gamestate = GameState.GameState.SELECTING_COUNTRY
        resetGame()
        pygame.mixer.music.stop()
        if not music_started:
            pygame.mixer.music.load("assets/sound/zic intro.mp3")
            pygame.mixer.music.play(-1)
            music_started = True

    window.blit(s, (window_width / 4, window_height / 4))
    window.blit(titletext, titletext_rect)
    replayBtn.draw(window)


def initLoss():
    global gamestate
    global music_started
    s = pygame.Surface((window_width / 2, window_height / 2))
    s.set_alpha(70)
    s.fill(GRIS)
    titletext = littleTitlefont.render("Vous perdez la partie", False, (0, 0, 0))
    titletext_rect = titletext.get_rect()
    titletext_rect.center = (window_width / 2, window_height / 3)
    if replayBtn.isClicked():
        gamestate = GameState.GameState.SELECTING_COUNTRY
        resetGame()
        pygame.mixer.music.stop()
        if not music_started:
            pygame.mixer.music.load("assets/sound/zic intro.mp3")
            pygame.mixer.music.play(-1)
            music_started = True
    window.blit(s, (window_width / 4, window_height / 4))
    window.blit(titletext, titletext_rect)
    replayBtn.draw(window)


def initDraw():
    global gamestate
    global music_started
    s = pygame.Surface((window_width / 2, window_height / 2))
    s.set_alpha(70)
    s.fill(GRIS)
    titletext = littleTitlefont.render("Personne ne gagne", False, (0, 0, 0))
    titletext_rect = titletext.get_rect()
    titletext_rect.center = (window_width / 2, window_height / 3)
    if replayBtn.isClicked():
        gamestate = GameState.GameState.SELECTING_COUNTRY
        resetGame()
        pygame.mixer.music.stop()
        if not music_started:
            pygame.mixer.music.load("assets/sound/zic intro.mp3")
            pygame.mixer.music.play(-1)
            music_started = True

    window.blit(s, (window_width / 4, window_height / 4))
    window.blit(titletext, titletext_rect)
    replayBtn.draw(window)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if gamestate == GameState.GameState.CHOOSE_PSEUDO:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) <= 18 and event.unicode.isprintable():
                    name += event.unicode

    if (
            gamestate == GameState.GameState.ENTRYPOINT or gamestate == GameState.GameState.CREDITS or gamestate == GameState.GameState.RULE) and not music_started:
        pygame.mixer.music.load("assets/sound/zic intro.mp3")
        pygame.mixer.music.play(-1)
        music_started = True
    if gamestate == GameState.GameState.IN_GAME and not music_started:
        pygame.mixer.music.load("assets/sound/ingame song.mp3")
        pygame.mixer.music.play(-1)
        music_started = True
    if gamestate == GameState.GameState.ENTRYPOINT:
        initMenu()
        if startButton.isClicked():
            gamestate = GameState.GameState.CHOOSE_PSEUDO
            pygame.mixer.Sound("assets/sound/bnt sound.mp3").play()

        elif creditButton.isClicked():
            gamestate = GameState.GameState.CREDITS
            pygame.mixer.Sound("assets/sound/bnt sound.mp3").play()
        elif ruleBtn.isClicked():
            gamestate = GameState.GameState.RULE
            pygame.mixer.Sound("assets/sound/bnt sound.mp3").play()
    elif gamestate == GameState.GameState.CREDITS:
        initCredits()
        if backButton.isClicked() and gamestate == GameState.GameState.CREDITS:
            gamestate = GameState.GameState.ENTRYPOINT

    elif gamestate == GameState.GameState.RULE:
        initRule()
        if backButton.isClicked():
            gamestate = GameState.GameState.ENTRYPOINT

    elif gamestate == GameState.GameState.CHOOSE_PSEUDO:

        choosePseudo(name)
        if nameButton.isClicked() and name != "":
            gamestate = GameState.GameState.SELECTING_COUNTRY

    elif gamestate == GameState.GameState.SELECTING_COUNTRY:
        selectCountry()
        if countryBtnconfirm.isClicked():
            gamestate = GameState.GameState.IN_GAME
            pygame.mixer.music.stop()
            music_started = False
    elif gamestate == GameState.GameState.IN_GAME:
        inGame()
    elif gamestate == GameState.GameState.WIN:
        if player.countClaim >= 6:
            initWin()
        elif player.countClaim < 6:
            initWin()
        else:
            initWin()

    pygame.display.update()
    clock.tick(60)
