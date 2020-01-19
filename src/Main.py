import pygame, sys, os
from GameClasses import *
from os.path import dirname

ROOT_PATH = dirname(dirname(__file__))  # create root path
def get_content(name_content):
    return os.path.join(os.path.join(ROOT_PATH, "content"), name_content)

WIDTH_WIN = 800
HEIGHT_WIN = 600

pygame.init()
WINDOW = pygame.display.set_mode((WIDTH_WIN, HEIGHT_WIN))
pygame.display.set_caption("World of Galaxies")
icon_img = pygame.image.load(get_content("icon.png"))
pygame.display.set_icon(icon_img)
FPS = 120
FPS_CLOCK = pygame.time.Clock()

# region Main menu

def main_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                game()

# endregion

#region Game

def game():
    # sprite groups
    components = pygame.sprite.Group()  # all components in game
    enemies = pygame.sprite.Group()  # all enemies in game
    player_lasers = pygame.sprite.Group()  # all player lasers in game
    enemies_lasers = pygame.sprite.Group()  # all enemies lasers in game

    # load content for game
    background_img = pygame.image.load(get_content("background.png"))
    player_img = pygame.image.load(get_content("player.png"))
    player_laser_img = pygame.image.load(get_content("player_laser.png"))
    enemy_img = pygame.image.load(get_content("enemy.png"))
    enemy_laser_img = pygame.image.load(get_content("enemy_laser.png"))

    # create basic game objects
    background = Background(3, 0, 0, background_img)
    player_x = (WIDTH_WIN // 2) - player_img.get_width() // 2
    player_y = HEIGHT_WIN - 100
    player = Player(100, 50, 5, 250, player_x, player_y, player_img, player_laser_img)

    components.add(player)

    generator = EnemiesAndAsteroidsGenerator(1000)
    # game loop
    is_game = True
    while is_game:
        # events / inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                is_game = False

        background.scrolling(HEIGHT_WIN)                                                # background updating
        generator.generate(enemy_img, enemy_laser_img, WIDTH_WIN, components, enemies)  # generating enemies

        # updating components
        for component in components:
            if isinstance(component, Player):
                component.update(components, player_lasers, enemies, enemies_lasers)
            elif isinstance(component, Enemy):
                component.update(HEIGHT_WIN, components, enemies_lasers)
            elif isinstance(component, Laser):
                component.update(HEIGHT_WIN)
            else:
                component.update()

        hits = pygame.sprite.groupcollide(enemies, player_lasers, True, True)

        background.draw(WINDOW)     # background drawing
        components.draw(WINDOW)     # drawing components

        FPS_CLOCK.tick(FPS)
        pygame.display.update()

    WINDOW.fill((0, 0, 0))
    pygame.display.update()

# endregion

# Main loop
main_menu()
pygame.quit()
sys.exit()
