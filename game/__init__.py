import pygame
from objects import GameState
from objects.player import Player
from objects.button import Button

pygame.init()
window_width = 1024
window_height = 768
window = pygame.display.set_mode((window_width, window_height))
clock = pygame.time.Clock()
running = True
name = ""
gamestate = GameState.GameState.ENTRYPOINT
player = Player(1200, 1200)
player.image = pygame.transform.scale(player.image, (100, 100))
titlefont = pygame.font.Font("./assets/fonts/RETROTECH.ttf", 72)
textFont = pygame.font.Font("./assets/fonts/RETROTECH.ttf", 48)
parentheseFont = pygame.font.Font("./assets/fonts/RETROTECH.ttf", 24)
KAKI = (89, 102, 67)
startButton = Button(window_width / 2, window_height / 1.25, pygame.image.load("./assets/startbutton.jpg"))

def initMenu():
    background = pygame.image.load("./assets/menu-background.png")

    titletext = titlefont.render("Concorde", False, (0, 0, 0))
    titletext_rect = titletext.get_rect()
    titletext_rect.center = (window_width/2, window_height/4)

    window.blit(background, (0, 0))
    window.blit(titletext, titletext_rect)
    startButton.draw(window)

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
    window.fill(KAKI)
    pygame.draw.rect(window, (255, 255, 255), (window_width / 4, window_height / 2, 512, 64))
    window.blit(titletext, titletext_rect)
    window.blit(pseudoUser, pseudoUser_rect)
    window.blit(parentheseText,parentheseText_rect)

while running:
    if gamestate == GameState.GameState.ENTRYPOINT:
        initMenu()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if gamestate == GameState.GameState.CHOOSE_PSEUDO:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name)<= 18:
                    name += event.unicode

    gamestate = GameState.GameState.CHOOSE_PSEUDO
    if startButton.isClicked():
        gamestate = GameState.GameState.CHOOSE_PSEUDO

    player.deplacer()

    if gamestate == GameState.GameState.CHOOSE_PSEUDO:
        choosePseudo(name)

    pygame.display.update()
    clock.tick(60)
