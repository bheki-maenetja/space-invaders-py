# pylint: disable=no-member
# pylint: disable=too-many-function-args
# pylint: disable=no-name-in-module
# Skeleton for a new project
import pygame
from time import sleep
from pygame.locals import (
  K_RIGHT,
  K_LEFT,
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

# LOAD ALL SOUND EFFECTS
audio_dir = path.join(path.dirname(__file__), 'audio')

aud_alien_kill = pygame.mixer.Sound(path.join(audio_dir, 'alien-kill.wav'))
aud_bomb_hit = pygame.mixer.Sound(path.join(audio_dir, 'bomb-hit.wav'))
aud_bomb_launch = pygame.mixer.Sound(path.join(audio_dir, 'bomb-launch.wav'))
aud_laser_blast = pygame.mixer.Sound(path.join(audio_dir, 'laser-blast.wav'))

gameplay_music = pygame.mixer.Sound(path.join(audio_dir, 'gameplay-music.wav'))
menu_music = pygame.mixer.Sound(path.join(audio_dir, 'menu-music.wav'))

# Set volume level for all sounds
sound_volume = 0.1

gameplay_music.set_volume(sound_volume)
menu_music.set_volume(sound_volume)
aud_alien_kill.set_volume(sound_volume)
aud_bomb_hit.set_volume(sound_volume)
aud_bomb_launch.set_volume(sound_volume)
aud_laser_blast.set_volume(sound_volume)

# LOAD ALL SPRITE IMAGES
img_dir = path.join(path.dirname(__file__), 'img')

background_image = pygame.image.load(path.join(img_dir, 'background.jpg')).convert()
screen_background = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
background_rect = screen_background.get_rect()

player_image_names = [
  ('playerShip2_blue.png', 'laserBlue14.png'),
  ('playerShip2_green.png', 'laserGreen06.png'),
  ('playerShip2_orange.png', 'laserRed14.png'),
  ('playerShip2_red.png', 'laserRed14.png')
]

player_images = []

laser_image = None

alien_images = [
  'shipPink_manned.png',
  'shipGreen_manned.png',
  'shipYellow_manned.png'
]

bomb_images = [
  'bombBlue_6.png',
  'bombGreen_5.png',
  'bombRed_6.png',
  'bombYellow_4.png',
]

for name in player_image_names:
  player_images.append(pygame.image.load(path.join(img_dir, name[0])).convert())

for i in range(len(alien_images)):
  alien_images[i] = pygame.image.load(path.join(img_dir, alien_images[i])).convert()

for i in range(len(bomb_images)):
  bomb_images[i] = pygame.image.load(path.join(img_dir, bomb_images[i])).convert()

mothership_image = pygame.image.load(path.join(img_dir, 'motherShip.png')).convert()

# SETUP SPRITES

# Sprite Classes
class Player(pygame.sprite.Sprite):
  def __init__(self):
    global laser_image
    super(Player, self).__init__()
    # self.image = pygame.Surface((50, 50))
    # self.image.fill(colours.RED)
    image_choice = choice(player_images)
    laser_image_name = player_image_names[player_images.index(image_choice)][1]
    laser_image = pygame.image.load(path.join(img_dir, laser_image_name)).convert()
    self.image = pygame.transform.scale(image_choice, (75, 50))
    self.image.set_colorkey(colours.BLACK)
    self.rect = self.image.get_rect(center=(WIDTH / 2, HEIGHT - 55))
    self.radius = 20
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
    # self.image = pygame.Surface((5, 30))
    # self.image.fill(colours.BLACK)
    self.image = pygame.transform.scale(laser_image, (8,30))
    self.image.set_colorkey(colours.BLACK)
    self.rect = self.image.get_rect(center=(x,y))
    self.speed = 12
  
  def update(self):
    self.rect.move_ip(0, -self.speed)
    if self.rect.bottom < 0:
      self.kill()

class Alien(pygame.sprite.Sprite):
  def __init__(self, x=0, y=0, width=25, height=25, speed=1, v_shift=30, lives=1):
    super(Alien, self).__init__()
    # self.image = pygame.Surface((width, height))
    # self.image.fill(choice(colours.ALL_COLOURS)[1])
    self.image = pygame.transform.scale(choice(alien_images), (width, height))
    self.image.set_colorkey(colours.BLACK)
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
    super(MotherShip, self).__init__(x,y,69,50,5,60,lives)
    # self.image = pygame.Surface((50, 50))
    # self.image.fill(choice(colours.ALL_COLOURS)[1])
    self.image = pygame.transform.scale(mothership_image, (69, 50))
    self.image.set_colorkey(colours.BLACK)

class Bomb(pygame.sprite.Sprite):
  def __init__(self, x, y):
    super(Bomb, self).__init__()
    # self.image = pygame.Surface((10, 20))
    # self.image.fill(colours.RED)
    self.image = pygame.transform.scale(choice(bomb_images), (15, 30))
    self.image.set_colorkey(colours.BLACK)
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

player = None

# GAME VARIABLES
is_game_over = False

frames = 0
timer = 0

game_level = 1

player_lives = 5
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
  text_surf = font.render(text, True, colours.WHITE)
  text_rect = text_surf.get_rect()
  text_rect.center = (x,y)
  surf.blit(text_surf, text_rect)

# SCREENS
def draw_menu(screen, player_won=False):
  gameplay_music.stop()
  menu_music.play(loops=-1)

  menu_surf = pygame.Surface((WIDTH, HEIGHT))
  menu_surf.fill(colours.BLUE)
  menu_rect = menu_surf.get_rect(center=(WIDTH/2, HEIGHT/2))
  menu_surf.blit(screen_background, background_rect)

  if player_won:
    draw_text(menu_surf, 'GAME OVER', 96, WIDTH/2, 100)
    draw_text(menu_surf, 'YOU WON!!!', 80, WIDTH/2, 175)
  else:
    draw_text(menu_surf, 'GAME OVER', 96, WIDTH/2, 100)
    draw_text(menu_surf, 'DEFEAT', 80, WIDTH/2, 175)
  draw_text(menu_surf, f"Score: {player_score}", 48, WIDTH/2, HEIGHT/2 - 50)
  draw_text(menu_surf, f"High Score: {gameplay_stats['high_score']}", 48, WIDTH/2, HEIGHT/2)
  draw_text(menu_surf, f"Time: {timer}s", 48, WIDTH/2, HEIGHT/2 + 50)

  pygame.draw.rect(menu_surf, colours.TEAL, (WIDTH/2 - 125, HEIGHT/2 + 100, 250, 50))
  draw_text(menu_surf, f"PLAY AGAIN", 36, WIDTH/2, HEIGHT/2 + 125)

  pygame.draw.rect(menu_surf, colours.RED, (WIDTH/2 - 125, HEIGHT/2 + 175, 250, 50))
  draw_text(menu_surf, f"QUIT", 36, WIDTH/2, HEIGHT/2 + 200)

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
  player_lives = 5
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

def start_game():
  global num_waves, player
  set_game_settings(game_level)
  set_aliens()
  num_waves -= 1
  player = Player()
  all_sprites.add(player)
  menu_music.stop()
  gameplay_music.play(loops=-1)
  
# Function Calls
start_game()

# GAME LOOP
running = True

while running:
  # Process Input (events)
  for event in pygame.event.get():
    if event.type == pygame.QUIT: # check for closing the window
      running = False
    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not is_game_over:
      player.fire_bullet()
      aud_laser_blast.play()
      gameplay_stats['shots_fired'] += 1
    if event.type == pygame.MOUSEBUTTONDOWN and is_game_over:
      if (WIDTH/2 - 125 <= event.pos[0] <= WIDTH/2 + 125) and (HEIGHT/2 + 100 <= event.pos[1] <= HEIGHT/2 + 150):
        is_game_over = False
        start_game()
      elif (WIDTH/2 - 125 <= event.pos[0] <= WIDTH/2 + 125) and (HEIGHT/2 + 175 <= event.pos[1] <= HEIGHT/2 + 225):
        running = False
    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN: # <-- Skip through waves of aliens
      for alien in aliens:
        alien.kill()

  # Update
  if is_game_over: continue # if the game is not in play move on

  all_sprites.update()
  
  alien_kills = pygame.sprite.groupcollide(bullets, aliens, True, False) # check for alien kills
  for alien in alien_kills.values():
    alien[0].take_hit()
    aud_alien_kill.play()
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

  if pygame.sprite.spritecollide(player, bombs, True, pygame.sprite.collide_circle): # collisions between player and bombs
    aud_bomb_hit.play()
    sleep(0.5)
    player_lives -= 1
    if player_lives == 0:
      is_game_over = True
  elif pygame.sprite.spritecollide(player, aliens, False):
    sleep(0.25)
    is_game_over = True
    player_lives = 0

  frames += 1

  if frames % (alien_fire_rate * FPS) == 0: # check to see if aliens should fire bombs
    if list(aliens) != []:
      chosen_alien = choice(list(aliens))
      if chosen_alien != None: 
        chosen_alien.drop_bomb()
        aud_bomb_launch.play()
  
  if frames % 60 == 0: # implementation of timer
    timer = frames // FPS 

  # Draw / Render
  screen.fill(colours.WHITE)
  screen.blit(screen_background, background_rect)
  if is_game_over:
    for sprite in all_sprites:
      sprite.kill()
    set_game_stats()
    draw_menu(screen, player_lives > 0)
    reset_game()
  else:
    all_sprites.draw(screen)
    for i, text in enumerate([f"Time: {timer}s", f"Score: {player_score}", f"Lives: {player_lives}", f"Level: {game_level}"]):
      draw_text(screen, text, 18, 108 * (i+1), 20)

  # AFTER Drawing Everything, Flip the Display
  pygame.display.flip()

  # Keep Game Loop Running at Given FPS
  clock.tick(FPS)