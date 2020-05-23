# pylint: disable=no-member
# pylint: disable=too-many-function-args
# pylint: disable=no-name-in-module
# Skeleton for a new project
import pygame
from pygame.locals import (
  K_RIGHT,
  K_LEFT
)

import random
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
    
  def boundary_check(self):
    if self.rect.x < 0:
      self.rect.x = 0
    if self.rect.right > WIDTH:
      self.rect.right = WIDTH

# Sprites and Groups
all_sprites = pygame.sprite.Group()
player = Player()

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

  # Update
  all_sprites.update()
  
  # Draw / Render
  screen.fill(colours.WHITE)
  all_sprites.draw(screen)

  # AFTER Drawing Everything, Flip the Display
  pygame.display.flip()

  # Keep Game Loop Running at Given FPS
  clock.tick(FPS)