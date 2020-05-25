# pylint: disable=no-member
# pylint: disable=too-many-function-args
# pylint: disable=no-name-in-module
# Skeleton for a new project
import pygame
from pygame.locals import (
  K_RIGHT,
  K_LEFT,
  K_SPACE
)

from random import choice
from os import path
import colours

# INITIALISE PYGAME AND CREATE WINDOW
WIDTH = 540
HEIGHT = 720
FPS = 60

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

# LOAD ALL SPRITE IMAGES
img_dir = path.join(path.dirname(__file__), 'img')

# SETUP SPRITES

# Sprite Classes
class Player(pygame.sprite.Sprite):
  def __init__(self):
    super(Player, self).__init__()
    self.image = pygame.Surface((50, 50))
    self.image.fill(colours.RED)
    self.rect = self.image.get_rect(center=(WIDTH / 2, HEIGHT - 55))
    self.speed = 5
  
  def update(self):
    key_state = pygame.key.get_pressed()
    if key_state[K_LEFT]:
      self.rect.move_ip(-self.speed, 0)
    if key_state[K_RIGHT]:
      self.rect.move_ip(self.speed, 0)

    self.boundary_check()
  
  def fire_bullet(self):
    new_bullet = Bullet(self.rect.centerx, self.rect.y)
    all_sprites.add(new_bullet)
    
  def boundary_check(self):
    if self.rect.x < 0:
      self.rect.x = 0
    if self.rect.right > WIDTH:
      self.rect.right = WIDTH

class Bullet(pygame.sprite.Sprite):
  def __init__(self, x, y):
    super(Bullet, self).__init__()
    self.image = pygame.Surface((5, 30))
    self.image.fill(colours.BLACK)
    self.rect = self.image.get_rect(center=(x,y))
    self.speed = 10
  
  def update(self):
    self.rect.move_ip(0, -self.speed)
    if self.rect.bottom < 0:
      self.kill()

class Alien(pygame.sprite.Sprite):
  def __init__(self, x, y):
    super(Alien, self).__init__()
    self.image = pygame.Surface((20, 20))
    self.image.fill(choice(colours.ALL_COLOURS)[1])
    self.rect = self.image.get_rect(center=(x,y))
    self.speed = 2

  def update(self):
    self.rect.move_ip(self.speed, 0)
    if self.rect.left < 0 or self.rect.right > WIDTH:
      self.rect.move_ip(0, 30)
      self.speed = -self.speed

# Sprites and Groups
all_sprites = pygame.sprite.Group()
aliens = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()

for i in range(60, 301, 60):
  for j in range(20, WIDTH, 40):
    new_alien = Alien(j, i)
    all_sprites.add(new_alien)
    aliens.add(new_alien)

all_sprites.add(player)

# GAME VARIABLES

# TEXT

# UTILITY FUNCTIONS

# GAME LOOP
running = True

while running:
  # Process Input (events)
  for event in pygame.event.get():
    if event.type == pygame.QUIT: # check for closing the window
      running = False
    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
      player.fire_bullet()

  # Update
  all_sprites.update()
  
  # Draw / Render
  screen.fill(colours.WHITE)
  all_sprites.draw(screen)

  # AFTER Drawing Everything, Flip the Display
  pygame.display.flip()

  # Keep Game Loop Running at Given FPS
  clock.tick(FPS)