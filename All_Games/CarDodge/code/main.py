import pygame
import sys
import random
import time
from pygame.locals import *

# ---------- Initialise modules and engine ----------
pygame.init()

# ---------- Game set-up ----------

# Display
WINDOW_WIDTH, WINDOW_HEIGHT = 400, 600
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Car Game')

# Backgrounds
background = pygame.image.load('../assets/AnimatedStreet.png').convert_alpha()

# Fonts
verdana_font = pygame.font.SysFont('Verdana', 60)
verdana_font_small = pygame.font.SysFont('Verdana', 20)

# Variables
speed = 1
running = True
score = 0
game_over = verdana_font.render('Game Over', True, 'black')

# Frames
frames_per_second = pygame.time.Clock()
fps = 60

# ---------- Sprites/Surfaces ----------
# Player Class Sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('../assets/Player.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < WINDOW_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)

# Enemy Class Sprite
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('../assets/Enemy.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, WINDOW_WIDTH-40), 0)

    def move(self):
        self.rect.move_ip(0, speed)
        if (self.rect.bottom > 600):
            self.rect.top = 0
            self.rect.center = (random.randint(30, 370), 0)

# ---------- Custom User Events ----------
# Increase Speed
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 2000)

# ---------- Creation/Initialisation ----------
# Create Player and Enemy Objects
P1 = Player()
E1 = Enemy()

# Create Sprite Groups
# Enemies
enemies = pygame.sprite.Group()
enemies.add(E1)

# All Sprites
all_sprites = pygame.sprite.Group()
all_sprites.add(E1)
all_sprites.add(P1)

# ---------- Game Loop ----------
while running:
    display_surface.fill('white')
    display_surface.blit(background, (0, 0))

    # Render & display fonts
    scores = verdana_font_small.render(str(score), True, 'black')
    display_surface.blit(scores, (10, 10))

    # Event Loop: Check if any events occuring this loop
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == INC_SPEED:
            speed += 1

    # Move and redraw all sprites
    for sprite in all_sprites:
        display_surface.blit(sprite.image, sprite.rect)
        sprite.move()
    
    # Collision detection and management
    if pygame.sprite.spritecollideany(P1, enemies):
        # Play crash sound effect
        pygame.mixer.Sound.play(pygame.mixer.Sound('../assets/crash.wav'))
        time.sleep(0.5)

        # draw game over font and turn screen red
        display_surface.fill('red')
        display_surface.blit(game_over, (30, 250))
        pygame.display.update()

        # Remove all sprites from the screen
        for sprite in all_sprites:
            sprite.kill()

        # close the game after 2 seconds
        time.sleep(2)
        pygame.quit()
        sys.exit()

    pygame.display.update()
    frames_per_second.tick(fps)
