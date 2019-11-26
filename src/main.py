import pygame

# Initialize
pygame.init()
window = pygame.display.set_mode((800, 600))

is_game = True
while is_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_game = False

pygame.quit()