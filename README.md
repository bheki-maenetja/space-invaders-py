# Space Invaders
An implementation of the classic 80s arcade game built with pygame and the python standard library.

## Getting Started
### Installation
- Clone this repository by running the terminal command `git clone git@github.com:bheki-maenetja/space-invaders-py.git`
- In the root folder run the terminal command `pipenv shell`
- In the root folder run the terminal command `pipenv install` to install all necessary packages and modules

### Deployment
- To run the game locally enter `python main.py` in the terminal

## Technology Used
- Python 3 (standard library)
- Pipenv
- Pygame 2.0.0.dev6

## Overview
The game is a pythonic implementation of the popular arcade game Space Invaders. When the game begins, the player has to shoot down multiple waves of aliens that approach with increasing speed. The player moves their spacecraft with the left and right arrow keys whilst firing bullets with the spacebar. The objective of the game is to eliminate all the aliens whilst losing as few lives as possible. Points are awarded for each alien kill and bonus points are awarded for each mothership that is destroyed.

###### <figcaption>Gameplay</figcation>
|<img src="https://github.com/bheki-maenetja/space-invaders-py/blob/master/img/screencast_gamplay.gif?raw=true" /> | <img src="https://github.com/bheki-maenetja/space-invaders-py/blob/master/img/screencast_gamplay-motherships.gif?raw=true" /> |
|---|---|


###### <figcaption>The aim of the game is to eliminate all aliens and motherships whilst losing as few lives as possible</figcaption>
| <img src="https://res.cloudinary.com/dyed10v2u/image/upload/v1600344391/project_space-invaders-py/screenshot_game-over-screen-victory_uqffjv.png" /> | <img src="https://res.cloudinary.com/dyed10v2u/image/upload/v1600344391/project_space-invaders-py/screenshot_game-over-screen-defeat_u0ni7v.png" /> |
|---|---|

## Development
The game was developed over the course of 2 weeks. It was built using the python standard library and version 2 of the pygame library. The game runs from main.py. This file features all the setup code for the game, classes to represent sprites as well as the game loop. The files colour.py and game_settings.py store some of the information needed for the game setup. 

```
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
```
## Reflection
### Challenges
- The main challenge for this project was the movement of aliens and motherships. Rather than descending in the traditional way as seen in most versions of Space Invaders, the aliens 'snake' towards the spaceship with each alien moving down one level each time it comes into contact with either the left or right wall. When moving downwards each alien moves indivdually rather than in unison with the aliens in its row. This single feature required quite a lot of time to figure out and put into code.

### Room for Improvement
- **Realistic Gameplay:** the one significant area in need of improvement is the gameplay. It definitely can be made to look more realistic, perhaps with the addition of explosions and additional sprite images to make the aliens appear animated.

## Future Features
- **Menu:** the game features a rudimentary menu with only two buttons and basic information about the most recent match. In the next update I would like to create a more expansive menu where users can configure settings for their matches and view their record for all the matches that they have played.
- **Power Ups:** for the next update I will allow for the user to attain 'power ups' that can provide temporary enhancements to the user's gameplay. These enchaments may include increased fire rate, protection from bombs or reinforcement ships that can help the user take on the aliens.