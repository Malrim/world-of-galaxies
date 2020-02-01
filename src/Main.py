import pygame, sys, os
from UIClasses import *
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

# region common content

ui_font = pygame.font.Font(get_content("fonts/kenney_future.ttf"), 25)
title_font = pygame.font.Font(get_content("fonts/kenney_future.ttf"), 50)


# endregion

# region Main menu

def quit_game():
    pygame.quit()
    sys.exit()


def main_menu():
    # load content for main menu
    background_img = pygame.image.load(get_content("menu/bg_menu.png"))
    bg_panel_img = pygame.image.load(get_content("menu/bg_panel_01.png"))
    button_blue_img = pygame.image.load(get_content("menu/button_blue.png"))
    button_yellow_img = pygame.image.load(get_content("menu/button_yellow.png"))

    # create UI
    size_text = title_font.size("World of Galaxies")
    title_text = UIText("World of Galaxies", title_font, (WIDTH_WIN / 2) - (size_text[0] / 2), 40)
    panel_x = (WIDTH_WIN / 2) - (bg_panel_img.get_width() / 2)
    panel_y = (HEIGHT_WIN / 2) - (bg_panel_img.get_width() / 2) - 50
    btn_play = UIButton("Play", ui_font, button_blue_img, button_yellow_img, panel_x + 20, panel_y + 20, game)
    btn_top_score = UIButton("Top Score", ui_font, button_blue_img, button_yellow_img,
                             panel_x + 20,
                             btn_play.pos_y + button_blue_img.get_height() + 10
                             )
    btn_quit = UIButton("Quit", ui_font, button_blue_img, button_yellow_img,
                        panel_x + 20,
                        btn_top_score.pos_y + button_blue_img.get_height() + 10,
                        quit_game
                        )

    while True:
        # events / inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        WINDOW.blit(background_img, (0, 0))

        # updating UI
        btn_play.update()
        btn_top_score.update()
        btn_quit.update()

        # drawing UI
        title_text.draw(WINDOW)
        WINDOW.blit(bg_panel_img, (panel_x, panel_y))
        btn_play.draw(WINDOW)
        btn_top_score.draw(WINDOW)
        btn_quit.draw(WINDOW)

        pygame.display.update()

# endregion

# region Game

def update_and_draw_ui(score_text, panel_score_x, bg_panel_score_img, player_hud, player):
    player_score = str(player.get_score())
    player_health = player.get_health()

    size_text = ui_font.size(player_score)
    score_text.pos_x = panel_score_x + (bg_panel_score_img.get_width() / 2) - (size_text[0] / 2)
    score_text.update_text(player_score)
    score_text.draw(WINDOW)

    player_hud.update_lives(player_health)
    player_hud.draw(WINDOW)

def game_over_menu():
    # load content for game over menu
    bg_panel_img = pygame.image.load(get_content("menu/bg_panel_02.png"))
    button_blue_img = pygame.image.load(get_content("menu/button_blue.png"))
    button_yellow_img = pygame.image.load(get_content("menu/button_yellow.png"))

    # create UI
    size_text = title_font.size("Game Over")
    game_over_text = UIText("Game Over", title_font, (WIDTH_WIN / 2) - (size_text[0] / 2), (HEIGHT_WIN / 2) - 150)
    panel_x = (WIDTH_WIN / 2) - (bg_panel_img.get_width() / 2)
    panel_y = (HEIGHT_WIN / 2) - (bg_panel_img.get_height() / 2)
    btn_again = UIButton("Again", ui_font, button_blue_img, button_yellow_img, panel_x + 20, panel_y + 20, game)
    btn_menu = UIButton("Menu", ui_font, button_blue_img, button_yellow_img,
                        panel_x + 20,
                        btn_again.pos_y + button_blue_img.get_height() + 10,
                        main_menu
                        )

    while True:
        # events / inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # updating UI
        btn_again.update()
        btn_menu.update()

        # drawing UI
        game_over_text.draw(WINDOW)
        WINDOW.blit(bg_panel_img, (panel_x, panel_y))
        btn_again.draw(WINDOW)
        btn_menu.draw(WINDOW)

        pygame.display.update()

def game():
    # sprite groups
    components = pygame.sprite.Group()  # all components in game
    enemies = pygame.sprite.Group()  # all enemies in game
    player_lasers = pygame.sprite.Group()  # all player lasers in game
    enemies_lasers = pygame.sprite.Group()  # all enemies lasers in game

    # load content for game
    background_img = pygame.image.load(get_content("background.png"))
    bg_panel_score_img = pygame.image.load(get_content("bg_panel_score.png"))
    bg_panel_lifes_img = pygame.image.load(get_content("bg_panel_lifes.png"))
    player_img = pygame.image.load(get_content("player.png"))
    player_laser_img = pygame.image.load(get_content("player_laser.png"))
    player_life_img = pygame.image.load(get_content("player_life.png"))
    enemy_img = pygame.image.load(get_content("enemy.png"))
    enemy_laser_img = pygame.image.load(get_content("enemy_laser.png"))

    # create basic game objects
    background = Background(BG_SCROLLING_SPEED, 0, 0, background_img)
    player_x = (WIDTH_WIN // 2) - player_img.get_width() // 2
    player_y = HEIGHT_WIN - 100
    player = Player(PLAYER_HEALTH, PLAYER_SPEED, PLAYER_SHOOT_DELAY, player_x, player_y, player_img, player_laser_img)
    components.add(player)

    # create UI for game
    panel_score_x = 8
    panel_score_y = HEIGHT_WIN - bg_panel_score_img.get_height() - 8
    size_text = ui_font.size("Score:")
    score_title = UIText("Score:", ui_font,
                         panel_score_x + (bg_panel_score_img.get_width() / 2) - (size_text[0] / 2),
                         panel_score_y + 15
                         )
    size_text = ui_font.size(str(player.get_score()))
    score_text = UIText(str(player.get_score()), ui_font,
                        panel_score_x + (bg_panel_score_img.get_width() / 2) - (size_text[0] / 2),
                        panel_score_y + 45
                        )
    panel_lifes_x = WIDTH_WIN - bg_panel_lifes_img.get_width() - 8
    panel_lifes_y = HEIGHT_WIN - bg_panel_lifes_img.get_height() - 8
    size_text = ui_font.size("Lifes:")
    lifes_title = UIText("Lifes:", ui_font,
                         panel_lifes_x + (bg_panel_lifes_img.get_width() / 2) - (size_text[0] / 2),
                         panel_lifes_y + 15
                         )
    player_hud = PlayerHUD(player.get_health(), player_life_img, panel_lifes_x + 35, panel_lifes_y + 45)

    generator = EnemiesAndAsteroidsGenerator(ENEMIES_AND_ASTEROIDS_GEN)

    # game loop
    while True:
        # events / inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                main_menu()

        background.scrolling(HEIGHT_WIN)  # background updating
        generator.generate(enemy_img, enemy_laser_img, WIDTH_WIN, components, enemies)  # generating enemies

        # updating game components
        for component in components:
            if isinstance(component, Player):
                component.update(components, player_lasers, enemies, enemies_lasers)
            elif isinstance(component, Enemy):
                component.update(HEIGHT_WIN, components, enemies_lasers)
            elif isinstance(component, Laser):
                component.update(HEIGHT_WIN)
            else:
                component.update()

        # drawing components and UI
        background.draw(WINDOW)
        components.draw(WINDOW)
        WINDOW.blit(bg_panel_score_img, (panel_score_x, panel_score_y))
        WINDOW.blit(bg_panel_lifes_img, (panel_lifes_x, panel_lifes_y))
        score_title.draw(WINDOW)
        lifes_title.draw(WINDOW)
        update_and_draw_ui(score_text, panel_score_x, bg_panel_score_img, player_hud, player)

        # check game over
        if player.get_health() <= 0:
            game_over_menu()

        FPS_CLOCK.tick(FPS)
        pygame.display.update()

# endregion

# Main loop
main_menu()
pygame.quit()
sys.exit()
