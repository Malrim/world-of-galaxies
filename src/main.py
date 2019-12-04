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

def main_menu():
    is_menu = True
    while is_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_program()

# endregion

# region Game

#region Load content

background_img = pygame.image.load(get_content("background.png"))
player_img = pygame.image.load(get_content("player.png"))

#endregion

bg_y = 0
def scrolling_background_draw(img, scrolling_speed):
    global bg_y
    window.blit(img, (0, bg_y))
    window.blit(img, (0, -img.get_rect().height + bg_y))
    if bg_y < HEIGHT_WIN:
        bg_y += scrolling_speed
    else:
        bg_y = 0

#region Classes

class Component:

    def __init__(self, pos_x, pos_y, img):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.img = img

    def update(self):
        pass

    def draw(self):
        window.blit(self.img, (self.pos_x, self.pos_y))

class Ship(Component):

    def __init__(self, health, number_lasers, speed, pos_x, pos_y, img):
        super().__init__(pos_x, pos_y, img)
        self.health = health
        self.max_health = health
        self.number_lasers = number_lasers
        self.max_number_lasers = number_lasers
        self.speed = speed

class Player(Ship):

    def __init__(self, health, number_lasers, speed, pos_x, pos_y, img):
        super().__init__(health, number_lasers, speed, pos_x, pos_y, img)

    def update(self):
        self.movement()  # player movement (inputs)

    def movement(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.pos_x += self.speed
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.pos_x -= self.speed
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.pos_y += self.speed
        elif keys[pygame.K_w] or keys[pygame.K_UP]:
            self.pos_y -= self.speed

class Laser:

    def __init__(self, start_x, start_y, speed, img):
        self.x = start_x
        self.y = start_y
        self.speed = speed
        self.img = img

        window.blit(self.img, start_x, start_y)

#endregion

components = []

# Initialize
player = Player(100, 50, 0.5, (WIDTH_WIN // 2) - player_img.get_width() // 2, HEIGHT_WIN - 100, player_img)
components.append(player)

# Game loop
def game():
    is_game = True
    while is_game:
        # events / inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_program()

        # updating components
        for c in components:
            c.update()

        # drawing components
        scrolling_background_draw(background_img, 0.5)
        for c in components:
            c.draw()

        pygame.display.update()

# endregion

# Main loop
#main_menu()
game()
quit_program()
