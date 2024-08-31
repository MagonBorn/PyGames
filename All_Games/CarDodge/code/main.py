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

# Fonts
verdana_font = pygame.font.SysFont('Verdana', 60)
verdana_font_small = pygame.font.SysFont('Verdana', 20)

# Variables
enemy_speed = 8
running = True
game_over = verdana_font.render('Game Over', True, 'black')

# Audio
pygame.mixer.music.load('D:/Programming/Python/Games/All_Games/CarDodge/assets/background.wav')
pygame.mixer.music.play(-1)

# Frames
frames_per_second = pygame.time.Clock()
fps = 60

# ---------- Sprites/Surfaces ----------
#  Background
class Background():
    def __init__(self):
        self.bgimage = pygame.image.load('../assets/AnimatedStreet.png').convert_alpha()
        self.rectBGimg = self.bgimage.get_rect()

        self.bgY1 = 0
        self.bgX1 = 0
        self.bgY2 = -self.rectBGimg.height
        self.bgX2 = 0

        self.moving_speed = 5
    
    def update(self):
        self.bgY1 += self.moving_speed
        self.bgY2 += self.moving_speed
        if self.bgY1 >= self.rectBGimg.height:
            self.bgY1 = -self.rectBGimg.height
        if self.bgY2 >= self.rectBGimg.height:
            self.bgY2 = -self.rectBGimg.height

    def render(self):
      display_surface.blit(self.bgimage, (self.bgX1, self.bgY1))
      display_surface.blit(self.bgimage, (self.bgX2, self.bgY2))

# Player Class Sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('../assets/Player.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
        self.score = 0

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < WINDOW_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)
    
    def update_score(self):
        self.score += 1

# Enemy Class Sprite
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('../assets/Enemy.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, WINDOW_WIDTH-40), 0)

    def move(self):
        self.rect.move_ip(0, enemy_speed)
        if (self.rect.bottom > 600):
            self.rect.top = 0
            self.rect.center = (random.randint(30, 370), 0)
            P1.update_score()

# ---------- Custom User Events ----------
# Increase Speed
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 4000)

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

# Backgrounds
back_ground = Background()

# ---------- Game Loop ----------
while running:
    frames_per_second.tick(fps)
    display_surface.fill('#c3c3c3')
    back_ground.update()
    back_ground.render()

    # Render & display fonts
    scores = verdana_font_small.render(str(P1.score), True, 'black')
    display_surface.blit(scores, (10, 10))

    # Event Loop: Check if any events occuring this loop
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == INC_SPEED:
            enemy_speed += .5

    # Move and redraw all sprites
    for sprite in all_sprites:
        display_surface.blit(sprite.image, sprite.rect)
        sprite.move()
    
    # Collision detection and management
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.music.stop()
        # Play crash sound effect
        pygame.mixer.Sound.play(pygame.mixer.Sound('../assets/crash.wav'))
        # time.sleep(0.5)

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
