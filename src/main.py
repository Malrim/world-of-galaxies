import os
import sys
import random
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
clock = pygame.time.Clock()

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
player_laser_img = pygame.image.load(get_content("player_laser.png"))
enemy_img = pygame.image.load(get_content("enemy.png"))
enemy_laser_img = pygame.image.load(get_content("enemy_laser.png"))

#endregion

#region Classes

class ExtendedSprite(pygame.sprite.Sprite):

    def __init__(self, *groups):
        super().__init__(*groups)
        self.is_custom_draw = False

    def custom_draw(self):
        pass

class ExtendedGroup(pygame.sprite.Group):

    def draw(self, surface):
        sprites = self.sprites()
        surface_blit = surface.blit
        for spr in sprites:
            if spr.is_custom_draw == False:
                self.spritedict[spr] = surface_blit(spr.image, spr.rect)
            else:
                spr.custom_draw()
        self.lostsprites = []

class Component(ExtendedSprite):

    def __init__(self, pos_x, pos_y, img, *groups):
        super().__init__(*groups)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

class Background(Component):

    def __init__(self, scrolling_speed, pos_x, pos_y, img):
        super().__init__(pos_x, pos_y, img)
        self.is_custom_draw = True
        self.scrolling_speed = scrolling_speed

    def update(self):
        if self.rect.y < HEIGHT_WIN:
            self.rect.y += self.scrolling_speed
        else:
            self.rect.y = 0

    def custom_draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        window.blit(self.image, (self.rect.x, -self.image.get_rect().height + self.rect.y))

class Ship(Component):

    def __init__(self, health, speed, shoot_delay, pos_x, pos_y, img):
        super().__init__(pos_x, pos_y, img)
        self.health = health
        self.max_health = health
        self.speed = speed
        self.shoot_delay = shoot_delay
        self.last_shot = pygame.time.get_ticks()

class Player(Ship):

    def __init__(self, health, number_lasers, speed, shoot_delay, pos_x, pos_y, img):
        super().__init__(health, speed, shoot_delay, pos_x, pos_y, img)
        self.number_lasers = number_lasers
        self.max_number_lasers = number_lasers

    def update(self):
        keys = pygame.key.get_pressed()
        self.movement(keys)

    def movement(self, keys):
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        elif keys[pygame.K_w] or keys[pygame.K_UP]:
            self.rect.y -= self.speed

        if keys[pygame.K_SPACE]:
            self.shoot()

    def shoot(self):
        time_now = pygame.time.get_ticks()
        if time_now - self.last_shot > self.shoot_delay:
            self.last_shot = time_now
            x = (self.rect.x + self.image.get_width() // 2) - player_laser_img.get_width() // 2
            y = self.rect.y - player_laser_img.get_height()
            laser = Laser(8, -1, x, y, player_laser_img)
            components.add(laser)
            player_lasers.add(laser)

class Enemy(Ship):

    def __init__(self, health, speed, shoot_delay, pos_x, pos_y, img):
        super().__init__(health, speed, shoot_delay, pos_x, pos_y, img)

    def update(self):
        self.rect.y += self.speed

        self.shoot()

        # if the enemy is off-screen
        if self.rect.top > HEIGHT_WIN:
            self.kill()

    def shoot(self):
        if (player.rect.x + player_img.get_width() // 2) >= self.rect.x and player.rect.x <= (self.rect.x + self.image.get_width() // 2):
            time_now = pygame.time.get_ticks()
            if time_now - self.last_shot > self.shoot_delay:
                self.last_shot = time_now
                x = (self.rect.x + self.image.get_width() // 2) - enemy_laser_img.get_width() // 2
                y = self.rect.y + self.image.get_height()
                laser = Laser(8, 1, x, y, enemy_laser_img)
                components.add(laser)
                enemies_lasers.add(laser)

class Laser(Component):

    def __init__(self, speed, direction, pos_x, pos_y, img):
        super().__init__(pos_x, pos_y, img)
        self.speed = speed
        self.direction = direction

    def update(self):
        self.rect.y += (self.speed * self.direction)

        # if the laser is off-screen
        if self.rect.bottom < 0 or self.rect.top > HEIGHT_WIN:
            self.kill()

class EnemyGenerator:

    def __init__(self, gen_delay):
        self.gen_delay = gen_delay
        self.last_enemy = pygame.time.get_ticks()

    def generate_enemies(self):
        time_now = pygame.time.get_ticks()
        if time_now - self.last_enemy > self.gen_delay:
            self.last_enemy = time_now
            x = random.randrange(WIDTH_WIN - enemy_img.get_width())
            y = -(enemy_img.get_height() + 10)
            enemy = Enemy(100, 3, 500, x, y, enemy_img)
            components.add(enemy)
            enemies.add(enemy)

#endregion

# Lists of components
components = ExtendedGroup()
enemies = ExtendedGroup()
player_lasers = ExtendedGroup()
enemies_lasers = ExtendedGroup()

# Initialize components
background = Background(3, 0, 0, background_img)
player = Player(100, 50, 5, 250, (WIDTH_WIN // 2) - player_img.get_width() // 2, HEIGHT_WIN - 100, player_img)

components.add(background)
components.add(player)

enemy_generator = EnemyGenerator(1000)

# Game loop
def game():
    is_game = True
    while is_game:
        # events / inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_program()

        # generating enemies
        enemy_generator.generate_enemies()

        # updating components
        components.update()

        hits = pygame.sprite.groupcollide(enemies, player_lasers, True, True)

        # drawing components
        components.draw(window)

        pygame.display.update()
        clock.tick(120)

# endregion

# Main loop
#main_menu()
game()
quit_program()
