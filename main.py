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
pygame.display.set_caption("Space Invaders")
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
    bullets.add(new_bullet)
    
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
  
  def drop_bomb(self):
    new_bomb = Bomb(self.rect.centerx, self.rect.bottom)
    all_sprites.add(new_bomb)
    bombs.add(new_bomb)
  
  def speed_up(self, speed):
    self.speed += speed

class Bomb(pygame.sprite.Sprite):
  def __init__(self, x, y):
    super(Bomb, self).__init__()
    self.image = pygame.Surface((10, 20))
    self.image.fill(colours.RED)
    self.rect = self.image.get_rect(center=(x,y))
    self.speed = 10
  
  def update(self):
    self.rect.move_ip(0, self.speed)
    if self.rect.bottom > HEIGHT:
      self.kill()

# Sprites and Groups
all_sprites = pygame.sprite.Group()
aliens = pygame.sprite.Group()
bullets = pygame.sprite.Group()
bombs = pygame.sprite.Group()

player = Player()

all_sprites.add(player)

# GAME VARIABLES
frames = 0
timer = 0
player_lives = 10
player_score = 0

# TEXT
font_name = pygame.font.match_font('arial')

def draw_text(surf, text, size, x, y):
  font = pygame.font.Font(font_name, size)
  text_surf = font.render(text, True, colours.BLACK)
  text_rect = text_surf.get_rect()
  text_rect.center = (x,y)
  surf.blit(text_surf, text_rect)

# SCREENS
def draw_menu(screen):
  menu_surf = pygame.Surface((WIDTH -100, HEIGHT - 100))
  menu_surf.fill(colours.BLUE)
  menu_rect = menu_surf.get_rect(center=(WIDTH/2, HEIGHT/2))
  screen.blit(menu_surf, menu_rect)

# UTILITY FUNCTIONS
def set_aliens():
  for i in range(60, 301, 60):
    for j in range(20, WIDTH, 40):
      new_alien = Alien(j, i)
      all_sprites.add(new_alien)
      aliens.add(new_alien)

set_aliens()

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
  
  alien_kills = pygame.sprite.groupcollide(bullets, aliens, True, True)
  for kill in alien_kills:
    player_score += 100
  
  chosen_aliens = [alien for alien in aliens if alien.rect.centery < 360]
  if len(chosen_aliens) == 0:
    set_aliens()
    
  pygame.sprite.groupcollide(bullets, bombs, True, True)

  if pygame.sprite.spritecollide(player, bombs, True):
    player_lives -= 1

  frames += 1
  if frames % FPS == 0:
    if list(aliens) != []:
      chosen_alien = choice(list(aliens))
      if chosen_alien != None: chosen_alien.drop_bomb() 
    timer = frames // FPS

  # Draw / Render
  screen.fill(colours.WHITE)
  if player_lives <= 0:
    draw_menu(screen)
  else:
    all_sprites.draw(screen)
    for i, text in enumerate([f"Time: {timer}s", f"Score: {player_score}", f"Lives: {player_lives}"]):
      draw_text(screen, text, 18, 135 * (i+1), 20)

  # AFTER Drawing Everything, Flip the Display
  pygame.display.flip()

  # Keep Game Loop Running at Given FPS
  clock.tick(FPS)