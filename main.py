# pylint: disable=no-member
# pylint: disable=too-many-function-args
# pylint: disable=no-name-in-module
# Skeleton for a new project
import pygame
from time import sleep
from pygame.locals import (
  K_RIGHT,
  K_LEFT,
  K_UP,
  K_SPACE
)

from random import choice
from os import path
import colours
import game_settings

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
    self.speed = 12
  
  def update(self):
    self.rect.move_ip(0, -self.speed)
    if self.rect.bottom < 0:
      self.kill()

class Alien(pygame.sprite.Sprite):
  def __init__(self, x=0, y=0, width=20, height=20, speed=1, v_shift=30, lives=1):
    super(Alien, self).__init__()
    self.image = pygame.Surface((width, height))
    self.image.fill(choice(colours.ALL_COLOURS)[1])
    self.rect = self.image.get_rect(center=(x,y))
    self.speed = speed
    self.v_shift = v_shift
    self.lives = lives

  def update(self):
    if self.rect.left < 0 or self.rect.right > WIDTH:
      self.speed = -self.speed
      self.rect.move_ip(self.speed, self.v_shift)
      return
    if self.rect.y > HEIGHT:
      self.kill()
    self.rect.move_ip(self.speed, 0)
  
  def drop_bomb(self):
    new_bomb = Bomb(self.rect.centerx, self.rect.bottom)
    all_sprites.add(new_bomb)
    bombs.add(new_bomb)

  def take_hit(self):
    self.lives -= 1
    if self.lives == 0: self.kill()

class MotherShip(Alien):
  def __init__(self, x, y, lives):
    super(MotherShip, self).__init__(x,y,50,50,5,60,lives)
    self.image = pygame.Surface((50, 50))
    self.image.fill(choice(colours.ALL_COLOURS)[1])

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
is_game_over = False

frames = 0
timer = 0

game_level = 1

player_lives = 1
player_score = 0

alien_speed = 0
alien_fire_rate = 0 
num_waves = 0
num_ships = 0
mothership_lives = 0
alien_hit_points = 0

# Game Settings
game_settings = game_settings.main_settings

# Gameplay Stats
gameplay_stats = {
  'games_played': 0,
  'total_score': 0,
  'high_score': 0,
  'lives_lost': 0,
  'alien_kills': 0,
  'mothership_kills': 0,
  'waves_fought': 0,
  'shots_fired': 0,
  'shortest_game': 0,
  'longest_game': 0,
  'total_time': 0,
}

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
  menu_surf = pygame.Surface((WIDTH, HEIGHT))
  menu_surf.fill(colours.YELLOW)
  menu_rect = menu_surf.get_rect(center=(WIDTH/2, HEIGHT/2))
  draw_text(menu_surf, 'GAME OVER', 96, 270, 100)
  screen.blit(menu_surf, menu_rect)

# UTILITY FUNCTIONS
def set_aliens():
  for i in range(60, 301, 60):
    for j in range(20, WIDTH, 40):
      new_alien = Alien(x=j, y=i, speed=alien_speed)
      all_sprites.add(new_alien)
      aliens.add(new_alien)

def set_motherships(num_ships):
  for i in range(num_ships):
    new_mothership = MotherShip((i+1) * (WIDTH // (num_ships + 1)), 60, mothership_lives)
    all_sprites.add(new_mothership)
    aliens.add(new_mothership)
    
def set_game_settings(level):
  global alien_speed, alien_fire_rate, num_waves, num_ships, alien_hit_points, mothership_lives
  alien_speed = game_settings[level]['alien_speed']
  alien_fire_rate = game_settings[level]['alien_fire_rate']
  num_waves = game_settings[level]['num_waves']
  num_ships = game_settings[level]['num_ships']
  mothership_lives = game_settings[level]['mothership_lives']
  alien_hit_points = game_settings[level]['alien_hit_points']

def reset_game():
  global frames, timer, game_level, player_lives, player_score, alien_speed, alien_fire_rate, num_waves, num_ships, mothership_lives, alien_hit_points
  frames = 0
  timer = 0
  game_level = 1
  player_lives = 10
  player_score = 0
  alien_speed = 0
  alien_fire_rate = 0 
  num_waves = 0
  num_ships = 0
  mothership_lives = 0
  alien_hit_points = 0

def set_game_stats():
  gameplay_stats['games_played'] += 1
  gameplay_stats['total_score'] += player_score
  gameplay_stats['high_score'] = player_score if player_score > gameplay_stats['high_score'] else gameplay_stats['high_score']
  gameplay_stats['lives_lost'] += 10 - player_lives
  gameplay_stats['total_time'] += timer

# Function Calls
set_game_settings(game_level)
set_aliens()
num_waves -= 1

# GAME LOOP
running = True

while running:
  # Process Input (events)
  for event in pygame.event.get():
    if event.type == pygame.QUIT: # check for closing the window
      running = False
    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not is_game_over:
      player.fire_bullet()
      gameplay_stats['shots_fired'] += 1
    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
      for alien in aliens:
        alien.kill()

  # Update
  if is_game_over: continue # if the game is not in play move on

  all_sprites.update()
  
  alien_kills = pygame.sprite.groupcollide(bullets, aliens, True, False) # check for alien kills
  for alien in alien_kills.values():
    alien[0].take_hit()
    player_score += alien_hit_points
    if num_waves == 0:
      gameplay_stats['mothership_kills'] += 1
    else:
      gameplay_stats['alien_kills'] += 1
  
  chosen_aliens = [alien for alien in aliens if alien.rect.centery < 360] # check to see if aliens should be spawned
  if len(chosen_aliens) == 0:
    if num_waves == 0 and game_level == 5 and list(aliens) == []:
      is_game_over = True
    elif num_waves == 0 and list(aliens) == []:
      game_level += 1
      set_game_settings(game_level)
    elif num_waves == 1:
      set_motherships(num_ships)
      gameplay_stats['waves_fought'] += 1
      num_waves -= 1
    elif num_waves != 0: 
      set_aliens()
      gameplay_stats['waves_fought'] += 1
      num_waves -= 1
    
  pygame.sprite.groupcollide(bullets, bombs, True, True) # collisions between bullets and bombs

  if pygame.sprite.spritecollide(player, bombs, True): # collisions between player and bombs
    sleep(0.2)
    player_lives -= 1
    if player_lives == 0:
      is_game_over = True
  elif pygame.sprite.spritecollide(player, aliens, False):
    sleep(0.25)
    is_game_over = True

  frames += 1

  if frames % (alien_fire_rate * FPS) == 0: # check to see if aliens should fire bombs
    if list(aliens) != []:
      chosen_alien = choice(list(aliens))
      if chosen_alien != None: chosen_alien.drop_bomb()
  
  if frames % 60 == 0: # implementation of timer
    timer = frames // FPS 

  # Draw / Render
  screen.fill(colours.WHITE)
  if is_game_over:
    draw_menu(screen)
    for sprite in all_sprites:
      sprite.kill()
    set_game_stats()
    reset_game()
    print(gameplay_stats)
  else:
    all_sprites.draw(screen)
    for i, text in enumerate([f"Time: {timer}s", f"Score: {player_score}", f"Lives: {player_lives}", f"Level: {game_level}"]):
      draw_text(screen, text, 18, 108 * (i+1), 20)

  # AFTER Drawing Everything, Flip the Display
  pygame.display.flip()

  # Keep Game Loop Running at Given FPS
  clock.tick(FPS)