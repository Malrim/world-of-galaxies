import pygame
from pathlib import Path

# Initialize
pygame.init()

#region Paths to folders

ROOT_PATH = Path(__file__).resolve().parent.parent  # Create root path

def get_path(name_folder):
    return ROOT_PATH.joinpath(name_folder)

def get_content(name_content):
    return str(get_path("content").joinpath(name_content))

#endregion

#region Initialize window

window = pygame.display.set_mode((800, 600))
pygame.display.set_caption("World of Galaxies")
icon_img = pygame.image.load(get_content("icon.png"))
pygame.display.set_icon(icon_img)

#endregion

# Main loop
is_game = True
while is_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_game = False

pygame.quit()