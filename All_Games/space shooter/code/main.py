import pygame
from os.path import join
import random

# Gener setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Space Shooter')
running = True
clock = pygame.time.Clock()

# Plain Surface
surf = pygame.Surface((100, 200))
surf.fill('orange')

# Imports
# Player
player_surface = pygame.image.load(join('../images', 'player.png')).convert_alpha()
player_rect = player_surface.get_frect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT - 60))
player_x_direction = 1
player_y_direction = 1

# Meteor
meteor_surface = pygame.image.load(join('../images', 'meteor.png')).convert_alpha()
meteor_rect = meteor_surface.get_frect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))

# Laser
laser_surface = pygame.image.load(join('../images', 'laser.png')).convert_alpha()
laser_rect = laser_surface.get_frect(bottomleft = (20, WINDOW_HEIGHT - 20))

# Stars
star_surface = pygame.image.load(join('../images', 'star.png')).convert_alpha()
star_positions = [(random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)) for i in range(20)]

while running:
    # Event loop
    clock.tick()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw the game
    display_surface.fill('darkgray')
    for pos in star_positions:
        display_surface.blit(star_surface, pos)

    display_surface.blit(meteor_surface, meteor_rect)
    display_surface.blit(laser_surface, laser_rect)
    display_surface.blit(player_surface, player_rect)

    player_rect.x += player_x_direction * 0.4
    player_rect.y += player_y_direction * 0.4
    if player_rect.right > WINDOW_WIDTH or player_rect.left < 0:
        player_x_direction *= -1
    if player_rect.top < 0 or player_rect.bottom > WINDOW_HEIGHT:
        player_y_direction *= -1

    pygame.display.update()

pygame.quit()