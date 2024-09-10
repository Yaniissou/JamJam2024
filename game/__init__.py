import pygame
import pytmx
from objects import GameState
from objects.player import Player
from objects.button import Button
from objects.Pays import Pays
pygame.init()
window_width = 1024
window_height = 768
window = pygame.display.set_mode((window_width, window_height))
clock = pygame.time.Clock()
running = True
name = ""
gamestate = GameState.GameState.ENTRYPOINT
player = Player(125, 680)
player.image = pygame.transform.scale(player.image, (32, 32))
titlefont = pygame.font.Font("./assets/fonts/RETROTECH.ttf", 72)
textFont = pygame.font.Font("./assets/fonts/RETROTECH.ttf", 48)
parentheseFont = pygame.font.Font("./assets/fonts/RETROTECH.ttf", 24)
GRIS = (229, 231, 230)
ORANGE_PALE = (238, 230, 216)
MARRON_FONCE = (147,68,26)
ruleBtn = Button(260,680, pygame.image.load("assets/btn_regle_496.png"))
startButton = Button(window_width / 1.6, window_height / 1.50, pygame.image.load("./assets/btn_start.png"))
creditButton = Button(window_width / 1.6, window_height/1.1, pygame.image.load("./assets/btn_start.png"))
nameButton =  Button(window_width / 1.6, window_height / 1.25, pygame.image.load("./assets/btn_valider.png"))
countryBtnconfirm = Button(window_width / 1.1, window_height / 1.1, pygame.image.load("./assets/btn_valider.png"))
countryBtnconfirm.image = pygame.transform.scale(nameButton.image,(246,78))
startButton.image = pygame.transform.scale(startButton.image,(246,78))
creditButton.image = pygame.transform.scale(creditButton.image,(246,78))
ruleBtn.image = pygame.transform.scale(ruleBtn.image,(246,78))
nameButton.image = pygame.transform.scale(nameButton.image,(246,78))
competences = {"education" : 100,"sante":100,"finance":100,"ressource":100,"culture":100,"sport":100}
france = Pays("France",competences,pygame.image.load("assets/france.png"))
allemagne = Pays("Allemagne",competences,pygame.image.load("assets/allemagne.png"))
angleterre = Pays("Angleterre",competences,pygame.image.load("assets/uk.png"))
chine = Pays("Chine",competences,pygame.image.load("assets/chine.png"))
eu = Pays("Etat-unis",competences,pygame.image.load("assets/etats_unis.png"))
russie = Pays("Russie",competences,pygame.image.load("assets/russie.png"))
selected_country = None
tmx_data = pytmx.util_pygame.load_pygame("assets/map/tileset/1.tmx")

def draw_map(screen, tmx_data):
    tile_width = tmx_data.tilewidth
    tile_height = tmx_data.tileheight

    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    screen.blit(tile, (x * tile_width, y * tile_height))

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

    titletext = titlefont.render("Concorde", False, (0, 0, 0))
    titletext_rect = titletext.get_rect()
    titletext_rect.center = (window_width/2, window_height/4)

    window.blit(background, (0, 0))
    window.blit(titletext, titletext_rect)
    startButton.draw(window)
    creditButton.draw(window)
    ruleBtn.draw(window)

def initRule():
    background = pygame.image.load("./assets/menu-background.png")
    titletext = titlefont.render("Regles", False, (0, 0, 0))
    titletext_rect = titletext.get_rect()
    titletext_rect.center = (window_width / 2, window_height / 8 - 50)

    regleText =  ("Alors que les differentes nations |du monde sont en pleine expansion,| plusieurs territoires |sont encore a departager !| A vous de montrer que votre pays |est le plus a meme| a obtenir ces terres. |explorer la map| et augmentez vos competences | afin de prendre possesion |des differente structure du territoire | pour gagner la partie :)")
    lines = regleText.split('|')
    y_offset = window_height / 6

    window.blit(background, (0, 0))
    window.blit(titletext,titletext_rect)
    for line in lines:
        content = textFont.render(line, False, (0, 0, 0))
        window.blit(content, (window_width / 2 - content.get_width() / 2, y_offset))
        y_offset += content.get_height() + 10
def initCredits():
    background = pygame.image.load("./assets/menu-background.png")

    titletext = titlefont.render("Credits", False, (0, 0, 0))
    titletext_rect = titletext.get_rect()
    titletext_rect.center = (window_width / 2, window_height / 6)

    credits_content = ("Yanis Harkati : Developpeur|"
                       "Ilan Darmon : Developpeur|"
                       "Rachel Peretti : Developpeuse|"
                       "Idibei Hassan : Administrateur reseau|"
                       "Tom Jochum : Directeur artistique")

    lines = credits_content.split('|')

    window.blit(background, (0, 0))
    window.blit(titletext, titletext_rect)

    y_offset = window_height / 2
    for line in lines:
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
    window.fill(ORANGE_PALE)
    pygame.draw.rect(window, (GRIS), (window_width / 4, window_height / 2, 512, 64))
    window.blit(titletext, titletext_rect)
    window.blit(pseudoUser, pseudoUser_rect)
    window.blit(parentheseText,parentheseText_rect)
    nameButton.draw(window)

def selectCountry():
    global selected_country
    imgPlayer = pygame.image.load("assets/testPlayer.png")
    imgPlayer = pygame.transform.scale(imgPlayer,(256,256))
    frBtn = Button(window_width /6, window_height / 3,france.img)
    ukBtn = Button(window_width /2, window_height / 3,angleterre.img)
    euBtn = Button(window_width /1.25, window_height / 3,eu.img)
    allemagneBtn = Button(window_width /6, window_height / 1.75,allemagne.img)
    chineBtn = Button(window_width /2, window_height / 1.75,chine.img)
    russieBtn = Button(window_width /1.25 , window_height / 1.75,russie.img)
    btnPays = [frBtn,ukBtn,euBtn,allemagneBtn,chineBtn,russieBtn]
    titletext = titlefont.render("Selectionner un pays", False, (0, 0, 0))
    titletext_rect = titletext.get_rect()
    titletext_rect.center = (window_width / 2, window_height / 8)
    window.fill(ORANGE_PALE)

    pygame.draw.rect(window,MARRON_FONCE,(window_width / 4, window_height / 1.1,256,32))
    for btn in btnPays:
        if btn.isHovered():
            btn.image = pygame.transform.scale(btn.image,(235,160))
        if btn.isClicked():
            selected_country = btn
        btn.draw(window)
        if selected_country:
            countryBtnconfirm.draw(window)
            window.blit(imgPlayer,(window_width / 4, window_height / 1.6))
    window.blit(titletext, titletext_rect)

def inGame():
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

#vérifier que deux sprites s'overlap
#fonction test jsp si elle marche
def collisionCheck(self, sprite1, sprite2):
    return pygame.sprite.collide_rect(sprite1, sprite2)

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

    if gamestate == GameState.GameState.ENTRYPOINT:
        initMenu()
        if startButton.isClicked():
            gamestate = GameState.GameState.CHOOSE_PSEUDO
        elif creditButton.isClicked():
            gamestate = GameState.GameState.CREDITS
        elif ruleBtn.isClicked():
            gamestate = GameState.GameState.RULE
    elif gamestate == GameState.GameState.CREDITS:
        initCredits()
    elif gamestate == GameState.GameState.RULE:
        initRule()
    elif gamestate == GameState.GameState.CHOOSE_PSEUDO:
        choosePseudo(name)
        if nameButton.isClicked() and name != "":
            gamestate = GameState.GameState.SELECTING_COUNTRY

    elif gamestate == GameState.GameState.SELECTING_COUNTRY:
        selectCountry()
        if countryBtnconfirm.isClicked():
            gamestate = GameState.GameState.IN_GAME
    elif gamestate == GameState.GameState.IN_GAME:
        inGame()


    pygame.display.update()
    clock.tick(60)

