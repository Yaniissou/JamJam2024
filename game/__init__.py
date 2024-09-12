import pygame
import pytmx
import random

from game.objects.ClicGame import ClicGame
from game.objects.mapItem import MapItem
from objects import GameState
from objects import Competences
from objects.player import Player
from objects.button import Button
from objects.QTE import QTE
from objects.Pays import Pays
from objects.Structure import Structure
from game.objects.mapItem import MapItem

music_started = False
pygame.init()
window_width = 1024
window_height = 768
window = pygame.display.set_mode((window_width, window_height))
clock = pygame.time.Clock()
running = True
name = ""
gamestate = GameState.GameState.SELECTING_COUNTRY
time_diff = pygame.time.get_ticks()
minigame = False
started = False

titlefont = pygame.font.Font("./assets/fonts/RETROTECH.ttf", 72)
littleTitlefont = pygame.font.Font("./assets/fonts/RETROTECH.ttf", 52)
textFont = pygame.font.Font("./assets/fonts/RETROTECH.ttf", 48)
parentheseFont = pygame.font.Font("./assets/fonts/RETROTECH.ttf", 24)
statPoleFont = pygame.font.Font("./assets/fonts/RETROTECH.ttf", 12)

GRIS = (229, 231, 230)
ORANGE_PALE = (238, 230, 216)
MARRON_FONCE = (147,68,26)

ruleBtn = Button(260,680, pygame.image.load("assets/btn_regle_496.png"))
startButton = Button(window_width / 1.6, window_height / 1.50, pygame.image.load("./assets/btn_start.png"))
creditButton = Button(1000,680, pygame.image.load("./assets/credits.png"))
backButton = Button(300, 200, pygame.image.load("./assets/retour.png"))
replayBtn = Button(630,530, pygame.image.load("assets/btn_regle_496.png"))

backButton.image = pygame.transform.scale(backButton.image,(150,106))
nameButton = Button(window_width / 1.6, window_height / 1.25, pygame.image.load("./assets/btn_valider.png"))
countryBtnconfirm = Button(window_width / 1.1, window_height / 1.1, pygame.image.load("./assets/btn_valider.png"))
countryBtnconfirm.image = pygame.transform.scale(nameButton.image,(246,78))
startButton.image = pygame.transform.scale(startButton.image,(246,78))
creditButton.image = pygame.transform.scale(creditButton.image,(246,78))
ruleBtn.image = pygame.transform.scale(ruleBtn.image,(246,78))
nameButton.image = pygame.transform.scale(nameButton.image,(246,78))
replayBtn.image = pygame.transform.scale(ruleBtn.image,(246,78))

competences = {0 : 1.2,1 : 1.4,2 : 1,3 : 0.8,4 : 1,5 : 1}

france = Pays("France",competences,pygame.image.load("assets/france.png"),None,pygame.image.load("./assets/sprite_france/run_down_fr/sprite_0.png"))
allemagne = Pays("Allemagne",competences,pygame.image.load("assets/allemagne.png"),None,pygame.image.load("./assets/sprite_allemagne/run_down_all/sprite_0.png"))
angleterre = Pays("Angleterre",competences,pygame.image.load("assets/uk.png"),None,pygame.image.load("./assets/sprite_france/run_down_fr/sprite_0.png"))
chine = Pays("Chine",competences,pygame.image.load("assets/chine.png"),None,pygame.image.load("./assets/sprite_france/run_down_fr/sprite_0.png"))
eu = Pays("Etat-unis",competences,pygame.image.load("assets/etats_unis.png"),None,pygame.image.load("./assets/sprite_france/run_down_fr/sprite_0.png"))
russie = Pays("Russie",competences,pygame.image.load("assets/russie.png"),None,pygame.image.load("./assets/sprite_france/run_down_fr/sprite_0.png"))

pays = [france,allemagne,angleterre,chine,eu,russie]
selected_country = None
selected_country_nation = None
tmx_data = pytmx.util_pygame.load_pygame("assets/map/tileset/1.tmx")
take_speed = 5
col_active = False
count_struc_complete = 0
list_struc_complete = []

images_sprite_france = [ pygame.image.load("./assets/sprite_france/run_down_fr/sprite_0.png"),
                         pygame.image.load("./assets/sprite_france/run_down_fr/sprite_1.png"),
                         pygame.image.load("./assets/sprite_france/run_left_fr/sprite_0.png"),
                         pygame.image.load("./assets/sprite_france/run_left_fr/sprite_1.png"),
                         pygame.image.load("./assets/sprite_france/run_right_fr/sprite_0.png"),
                         pygame.image.load("./assets/sprite_france/run_right_fr/sprite_1.png"),
                         pygame.image.load("./assets/sprite_france/run_up_fr/sprite_0.png"),
                         pygame.image.load("./assets/sprite_france/run_up_fr/sprite_1.png")]


images_sprite_allemagne= [ pygame.image.load("./assets/sprite_allemagne/run_down_all/sprite_0.png"),
                         pygame.image.load("./assets/sprite_allemagne/run_down_all/sprite_1.png"),
                         pygame.image.load("./assets/sprite_allemagne/run_left_all/sprite_0.png"),
                         pygame.image.load("./assets/sprite_allemagne/run_left_all/sprite_1.png"),
                         pygame.image.load("./assets/sprite_allemagne/run_right_all/sprite_0.png"),
                         pygame.image.load("./assets/sprite_allemagne/run_right_all/sprite_1.png"),
                         pygame.image.load("./assets/sprite_allemagne/run_up_all/sprite_0.png"),
                         pygame.image.load("./assets/sprite_allemagne/run_up_all/sprite_1.png")]


player = Player(125, 680,competences,60,None,images_sprite_france,0)
imgPlayer = france.imgPlayer
imgPlayer = pygame.transform.scale(imgPlayer,(192,192))

hopital = Structure("hopital",Competences.Competences.SANTE,100,None,False,0,False)
ecole = Structure("ecole",Competences.Competences.EDUCATION,100,None,False,0,False)
banque = Structure("banque",Competences.Competences.FINANCE,100,None,False,0,False)
puit = Structure("puit",Competences.Competences.RESSOURCES,100,None,False,0,False)
stade = Structure("stade",Competences.Competences.SPORT,100,None,False,0,False)
musee = Structure("musee",Competences.Competences.CULTURE,100,None,False,0,False)

strucGroupe = [musee,hopital, ecole,stade,puit,banque]

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
    imgTitre = pygame.image.load("./assets/imgTitre.png")
    imgTitre = pygame.transform.scale(imgTitre,(500,93))

    window.blit(background, (0, 0))
    window.blit(imgTitre,(window_width/4,window_height/4))
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
                       "Idibei Hassan : Administrateur reseau|"
                       "Tom Jochum : Directeur artistique")

    devlines = devcontent.split('|')

    sourcecontent = ("Ecole : poppants|"
                     "Decor : schwarnhild|"
                     "Terrain de foot : davidevitali|")

    sourcelines = sourcecontent.split("|")


    window.blit(background, (0, 0))
    window.blit(titletext, titletext_rect)
    backButton.draw(window)
    y_offset = window_height /4
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
    window.blit(parentheseText,parentheseText_rect)
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
    strucGroupe = [musee.coll_zone,hopital.coll_zone, ecole.coll_zone,stade.coll_zone,puit.coll_zone,banque.coll_zone, batiments, palmier, bordure, mer]

    for k in range(length):
        x = random.randint(0, window_width - 32)  # Limite de la fenêtre
        y = random.randint(0, window_height - 32)
        item = MapItem(x, y, pygame.image.load("./assets/testPlayer.png"))
        for structure in strucGroupe:
            for tile in structure:
                while item.rect.colliderect(tile):
                    x = random.randint(0, window_width - 32)  # Limite de la fenêtre
                    y = random.randint(0, window_height - 32)
                    item = MapItem(x, y, pygame.image.load("./assets/testPlayer.png"))


        items.append(item)
    return items

def selectCountry():
    global selected_country
    global imgPlayer
    titletext = titlefont.render("Selectionnez un pays", False, (0, 0, 0))
    titletext_rect = titletext.get_rect()
    titletext_rect.center = (window_width / 2, window_height / 8)

    frBtn = Button(window_width /6, window_height / 3,france.img)
    france.btn = frBtn
    ukBtn = Button(window_width /2, window_height / 3,angleterre.img)
    angleterre.btn = ukBtn
    euBtn = Button(window_width /1.25, window_height / 3,eu.img)
    eu.btn = euBtn
    allemagneBtn = Button(window_width /6, window_height / 1.75,allemagne.img)
    allemagne.btn = allemagneBtn
    chineBtn = Button(window_width /2, window_height / 1.75,chine.img)
    chine.btn = chineBtn
    russieBtn = Button(window_width /1.25 , window_height / 1.75,russie.img)
    russie.btn = russieBtn

    window.fill(MARRON_FONCE)

    pygame.draw.rect(window,MARRON_FONCE,(window_width / 4, window_height / 1.1,256,32))
    for country in pays:
        if country.btn.isHovered():
            country.btn.image = pygame.transform.scale(country.btn.image,(235,160))
        if country.btn.isClicked():
            selected_country = country
            imgPlayer = selected_country.imgPlayer
            imgPlayer = pygame.transform.scale(imgPlayer,(192,192))
        country.btn.draw(window)
        if selected_country:
            countryBtnconfirm.draw(window)
            window.blit(imgPlayer,(window_width / 4, window_height / 1.6))
    window.blit(titletext, titletext_rect)

def circleZone():
    collision_tiles_musee = get_collision_tiles(tmx_data,"culture_cercle")
    collision_tiles_hopital = get_collision_tiles(tmx_data,"hopital_cercle")
    collision_tiles_ecole = get_collision_tiles(tmx_data,"ecole_cercle")
    collision_tiles_sport = get_collision_tiles(tmx_data,"stade_cercle")
    collision_tiles_puit = get_collision_tiles(tmx_data,"puit_cercle")
    collision_tiles_banque = get_collision_tiles(tmx_data,"banque_cercle")

    collision_tiles = collision_tiles_musee + collision_tiles_hopital + collision_tiles_ecole + collision_tiles_sport + collision_tiles_puit + collision_tiles_banque
    for tile in collision_tiles:
        s = pygame.Surface((32,32))
        s.set_alpha(70)
        s.fill((50, 158, 168))
        window.blit(s,(tile.x,tile.y))



def statPole(player1):
    global competences
    toolPole = pygame.Rect(330, 700, 300, 60)
    pygame.draw.rect(window,MARRON_FONCE,toolPole)
    pygame.draw.rect(window, (186, 88, 35), toolPole,5)
    count =0
    for cle in competences.keys():
        if count <=2:
            parentheseText = statPoleFont.render(f"{Competences.Competences(cle).name} : {competences[cle]}", False, (0, 0, 0))
            parentheseText_rect = parentheseText.get_rect()
            parentheseText_rect.center = (382 + count *90, 720)
            window.blit(parentheseText,parentheseText_rect)
        else:
            parentheseText = statPoleFont.render(f"{Competences.Competences(cle).name} : {competences[cle]}", False, (0, 0, 0))
            parentheseText_rect = parentheseText.get_rect()
            parentheseText_rect.center = (370 + (count-3) * 90, 740)
            window.blit(parentheseText, parentheseText_rect)
        count += 1

qte_ressource = QTE(7000,False)
addStar = False
def checkItemCollisions(player, items):
    global started
    global addStar
    timer_event = pygame.USEREVENT + 1

    for item in items:
        if player.rect.colliderect(item.rect):
            started = True
            items.remove(item)
            pygame.time.set_timer(timer_event,qte_ressource.duree)
        if started:
            qte_ressource.start(window_width, window_height, GRIS, window, textFont)
        if event.type == timer_event:
            qte_ressource.isFinish = True
            started = False
            addStar = True
            print(qte_ressource.wons)






def take():
    global take_speed
    global time_diff
    global strucGroupe
    timer_event = pygame.USEREVENT + 1
    charge_speed = 0
    musee.coll_zone = get_collision_tiles(tmx_data, "culture_zone")
    hopital.coll_zone = get_collision_tiles(tmx_data, "hopital_zone")
    ecole.coll_zone = get_collision_tiles(tmx_data, "ecole_zone")
    stade.coll_zone = get_collision_tiles(tmx_data, "stade_zone")
    puit.coll_zone = get_collision_tiles(tmx_data, "puit_zone")
    banque.coll_zone = get_collision_tiles(tmx_data, "banque_zone")

    strucGroupe = [musee,hopital, ecole,stade,puit,banque]
    pygame.draw.rect(window,GRIS,(150,300,100,20))
    pygame.draw.rect(window,GRIS,(210,10,100,20))
    pygame.draw.rect(window,GRIS,(450,10,100,20))
    pygame.draw.rect(window,GRIS,(550,230,100,20))
    pygame.draw.rect(window,GRIS,(850,50,100,20))
    pygame.draw.rect(window,GRIS,(700,600,100,20))

    pygame.draw.rect(window,(50, 158, 168),(150,300,musee.charge_state,20))
    pygame.draw.rect(window,(50, 158, 168),(210,10,ecole.charge_state,20))
    pygame.draw.rect(window,(50, 158, 168),(450,10,banque.charge_state,20))
    pygame.draw.rect(window,(50, 158, 168),(550,230,stade.charge_state,20))
    pygame.draw.rect(window,(50, 158, 168),(850,50,hopital.charge_state,20))
    pygame.draw.rect(window,(50, 158, 168),(700,600,puit.charge_state,20))
    anyCol = False
    for structure in strucGroupe:
        for tile in structure.coll_zone:
            charge_tap = player.competences[structure.competence.value] * player.etoile

            if player.rect.colliderect(tile) and not structure.isCLaim:
                anyCol = True
                if not structure.col_active:
                    structure.col_active = True
                else:
                    previous_charge = structure.charge_state
                    if structure.charge_state < structure.lifePole:
                        structure.charge_state += charge_tap
                        print(f"charge_state: {structure.charge_state}, lifePole: {structure.lifePole}")

                    if structure.charge_state >= structure.lifePole and structure.col_active:
                        structure.isCLaim = True
                        structure.col_active = False
                        diff = structure.lifePole - previous_charge
                        player.etoile -= diff
                        structure.charge_state = structure.lifePole
                        print("Structure revendiquée")
                    else:
                        if player.etoile > 0:
                            diff = structure.lifePole - structure.charge_state
                            player.etoile = 0
                        print(f"Étoiles restantes : {player.etoile}")
            elif not player.rect.colliderect(tile) and not structure.isCLaim:
                structure.col_active = False


    if not anyCol and structure.col_active:
        structure.col_active = False
        print(f"Collision terminée : {structure.col_active}")

items = generate_items(20)

def inList(list,elem):
    for l in list:
        if l == elem:
            return True
    return False
def inGame():
    global count_struc_complete
    global gamestate
    global list_struc_complete
    player.country = selected_country
    player.competences = player.country.competences
    if player.country == allemagne:
        player.images = images_sprite_allemagne

    titletext = titlefont.render(f"nb etoile :  {player.etoile}", False, (0, 0, 0))
    titletext_rect = titletext.get_rect()
    titletext_rect.center = (window_width / 2, window_height / 8)
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
    window.blit(titletext,titletext_rect)
    circleZone()
    take()
    statPole(player)

    for struc in strucGroupe:
        if struc.isCLaim and not inList(list_struc_complete,struc):
            count_struc_complete +=1
            list_struc_complete.append(struc)
            print(count_struc_complete)

    if count_struc_complete == 6:
        gamestate = GameState.GameState.WIN

    for item in items:
        item.draw(window)
    checkItemCollisions(player, items)

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

    player = Player(125, 680, competences, 60, None, images_sprite_france, 0)
    imgPlayer = france.imgPlayer
    imgPlayer = pygame.transform.scale(imgPlayer, (192, 192))

    hopital = Structure("hopital", Competences.Competences.SANTE, 100, None, False, 0, False)
    ecole = Structure("ecole", Competences.Competences.EDUCATION, 100, None, False, 0, False)
    banque = Structure("banque", Competences.Competences.FINANCE, 100, None, False, 0, False)
    puit = Structure("puit", Competences.Competences.RESSOURCES, 100, None, False, 0, False)
    stade = Structure("stade", Competences.Competences.SPORT, 100, None, False, 0, False)
    musee = Structure("musee", Competences.Competences.CULTURE, 100, None, False, 0, False)
    items = []
    items = generate_items(20)

def initWin():
    global gamestate
    global music_started
    s = pygame.Surface((window_width/2, window_height/2))
    s.set_alpha(70)
    s.fill(GRIS)
    titletext = littleTitlefont.render("Vous avez gagné", False, (0, 0, 0))
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

    window.blit(s, (window_width/4, window_height/4))
    window.blit(titletext,titletext_rect)
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


    if (gamestate == GameState.GameState.ENTRYPOINT or gamestate == GameState.GameState.CREDITS or gamestate == GameState.GameState.RULE) and not music_started:
        pygame.mixer.music.load("assets/sound/zic intro.mp3")
        pygame.mixer.music.play(-1)
        music_started = True
    #if gamestate == GameState.GameState.IN_GAME and not music_started:
     #   pygame.mixer.music.load("assets/sound/ingame song.mp3")
      #  pygame.mixer.music.play(-1)
       # music_started = True
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
        initWin()


    pygame.display.update()
    clock.tick(60)

