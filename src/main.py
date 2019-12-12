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

components = []

def add_component(component):
    if components.count(component) == 0:
        components.append(component)

#region Load content

background_img = pygame.image.load(get_content("background.png"))
player_img = pygame.image.load(get_content("player.png"))
player_laser_img = pygame.image.load(get_content("player_laser.png"))

#endregion

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

class Background(Component):

    def __init__(self, scrolling_speed, pos_x, pos_y, img):
        super().__init__(pos_x, pos_y, img)
        self.scrolling_speed = scrolling_speed

    def update(self):
        if self.pos_y < HEIGHT_WIN:
            self.pos_y += self.scrolling_speed
        else:
            self.pos_y = 0

    def draw(self):
        window.blit(self.img, (self.pos_x, self.pos_y))
        window.blit(self.img, (self.pos_x, -self.img.get_rect().height + self.pos_y))

class Ship(Component):

    def __init__(self, health, number_lasers, speed, shoot_delay, pos_x, pos_y, img):
        super().__init__(pos_x, pos_y, img)
        self.health = health
        self.max_health = health
        self.number_lasers = number_lasers
        self.max_number_lasers = number_lasers
        self.speed = speed
        self.shoot_delay = shoot_delay
        self.last_shot = pygame.time.get_ticks()

class Player(Ship):

    def __init__(self, health, number_lasers, speed, shoot_delay, pos_x, pos_y, img):
        super().__init__(health, number_lasers, speed, shoot_delay, pos_x, pos_y, img)

    def update(self):
        keys = pygame.key.get_pressed()

        self.movement(keys)

    def movement(self, keys):
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.pos_x += self.speed
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.pos_x -= self.speed
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.pos_y += self.speed
        elif keys[pygame.K_w] or keys[pygame.K_UP]:
            self.pos_y -= self.speed

        if keys[pygame.K_SPACE]:
            self.shoot()

    def shoot(self):
        time_now = pygame.time.get_ticks()
        if time_now - self.last_shot > self.shoot_delay:
            self.last_shot = time_now
            x = (self.pos_x + self.img.get_width() // 2) - player_laser_img.get_width() // 2
            y = self.pos_y - player_laser_img.get_height()
            laser = Laser(1, -1, x, y, player_laser_img)
            add_component(laser)

class Laser(Component):

    def __init__(self, speed, direction, pos_x, pos_y, img):
        super().__init__(pos_x, pos_y, img)
        self.speed = speed
        self.direction = direction

    def update(self):
        self.pos_y += (self.speed * self.direction)

#endregion

# Initialize components
background = Background(0.5, 0, 0, background_img)
player = Player(100, 50, 0.5, 250, (WIDTH_WIN // 2) - player_img.get_width() // 2, HEIGHT_WIN - 100, player_img)

add_component(background)
add_component(player)

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
        for c in components:
            c.draw()

        pygame.display.update()

# endregion

# Main loop
#main_menu()
game()
quit_program()
