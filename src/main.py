import os
import sys
import pygame
from os.path import dirname

# region Initialize PyGame

pygame.init()

# endregion

# region Functions for paths to folders

ROOT_PATH = dirname(dirname(__file__))  # create root path

def get_path(name_folder):
    return os.path.join(ROOT_PATH, name_folder)

def get_content(name_content):
    return os.path.join(get_path("content"), name_content)

# endregion

# region Initialize window

WIDTH_WIN = 800
HEIGHT_WIN = 600

window = pygame.display.set_mode((WIDTH_WIN, HEIGHT_WIN))
pygame.display.set_caption("World of Galaxies")
icon_img = pygame.image.load(get_content("icon.png"))
pygame.display.set_icon(icon_img)

# endregion

# region System functions

def quit_program():
    pygame.quit()
    sys.exit()

# endregion

# region Main menu

def menu_loop():
    is_menu = True
    while is_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_program()

# endregion

# region Game

# Content
background_img = pygame.image.load(get_content("background.png"))
player_img = pygame.image.load(get_content("player.png"))

# Functions

bg_y = 0
def scrolling_background_draw(img, scrolling_speed):
    global bg_y
    window.blit(img, (0, bg_y))
    window.blit(img, (0, -img.get_rect().height + bg_y))
    if bg_y < HEIGHT_WIN:
        bg_y += scrolling_speed
    else:
        bg_y = 0

# Classes

class Player:

    def __init__(self, health, number_laser, start_x, start_y, img):
        self.health = health
        self.number_laser = number_laser
        self.x = start_x
        self.y = start_y
        self.img = img

    def movement(self, keys, speed):
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x += speed
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x -= speed
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.y += speed
        elif keys[pygame.K_w] or keys[pygame.K_UP]:
            self.y -= speed

    def draw(self):
        window.blit(self.img, (self.x, self.y))

# Initialize
player = Player(100, 50, (WIDTH_WIN // 2) - player_img.get_width() // 2, HEIGHT_WIN - 100, player_img)

# Game loop
def game_loop():
    x = 0
    is_game = True
    while is_game:
        # events / inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_program()
        keys = pygame.key.get_pressed()

        player.movement(keys, 0.5)

        # drawing
        scrolling_background_draw(background_img, 0.5)
        player.draw()

        pygame.display.update()

# endregion

# Main loop
#menu_loop()
game_loop()
quit_program()
