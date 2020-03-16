"""
Project: Space Invaders Game
Author: Harshit Varma
"""
"""
   Anything happening inside the game window is an event
   Anything "persistant" needs to go inside the game loop
   Coordinates:
       x axis along right
       y axis downwards
"""

# Imports/ Dependencies 
import pygame as pg
import random
import math
from pygame import mixer
import time
import sys
import numpy as np

# Initializes the pygame module
pg.init()

"""PERSONALIZATION"""

# This creates a window/screen of width = 800, height = 600 
screen = pg.display.set_mode((800, 600))
# This names the window title
pg.display.set_caption("Space Invaders")

# For icons always select 32*32 pixels icon
icon = pg.image.load("icons/saucer2a.ico")
pg.display.set_icon(icon)

# Background
bg_color = (5,5,5)
# BG Image
#bg_img = pg.image.load('images/background.png')
intro_bg = pg.image.load('images/si_logo.png')

# BG Sound
"""
mixer.music.load("audio/background.wav")
mixer.music.play(-1)
"""
# Fonts
big_font = pg.font.Font('fonts/Minecraft.ttf', 64)
font = pg.font.Font('fonts/Minecraft.ttf', 32) # You can download more fonts from dafont.com

# Enemy chooser
enemy_list = ['icons/saucer2a.ico', 'icons/saucer1a.ico', 'icons/saucer3a.ico']
speed_list = [0.5,0.75,1.25,1.5,1.75,2,2.25,2.5]
speed_list = np.asarray(speed_list)

"""ELEMENTS"""
main_loop = True

while main_loop:

    speed_list = [0.5,0.75,1.25,1.5,1.75,2,2.25,2.5]
    speed_list = np.asarray(speed_list)


    # Player
    playerImg = pg.image.load('icons/baseshipa.ico')
    playerX = 368 # Image width also considered, about 32 thus 400-32 is taken as X
    playerY = 480 # 20dp margin
    player_speed = 3 # Speed of the player
    playerX_change = 0


    # Enemy
    n_enemies = 6 # Total number of enemies
    enemyImg = []
    enemyX = []
    enemyY = []
    enemyX_change = []
    enemyY_change = []
    enemy_speed = []

    for i in range(n_enemies):
        enemyImg.append(pg.image.load(random.choice(enemy_list)))
        enemyX.append(random.randint(0, 735))
        enemyY.append(random.randint(50, 150)) 
        enemyX_change.append(random.choice(speed_list))
        enemy_speed.append(random.choice(speed_list))
        enemyY_change.append(40)

    # Bullet
    bulletImg = pg.image.load('images/bullet.png')
    bulletX = 0 
    bulletY = 480 
    bulletX_change = 0
    bulletY_change = 3
    bullet_state = "ready" # ready state - can't see the bullet on the screen, fire - moving state of bullet

    # Score
    score_value = 0
    scoreX = 10
    scoreY = 10 

    """ANIMATIONS"""
    explosion = pg.image.load("images/explosion.png")


    """FUNCTIONS"""

    def player(x, y): # Coordinates of the player
        screen.blit(playerImg, (x, y)) # Method use to plot the image on the game window
        
    def enemy(x, y, i):
        screen.blit(enemyImg[i], (x,y))

    def fire_bullet(x, y):
        global bullet_state
        bullet_state = "fire"
        screen.blit(bulletImg, (x + 16, y + 10)) # To ensure bullet appears at the top of the nose and centre of the spaceship
        
    def isCollision(enemyX, enemyY, bulletX, bulletY):
        distance = math.sqrt((math.pow((enemyX - bulletX),2)) + math.pow((enemyY - bulletY),2))
        if distance < 19:
            return True
        else:
            return False
        
    def show_score(x, y):
        score = font.render("SCORE : " + str(score_value), True, (255,255,255))
        screen.blit(score, (x,y))

    # For the main game loop: 
    running = True
    pause = False
    restart = False
    canYouPause = True

    """Introductory Window Loop"""
    intro = True
    while intro:
        #screen.fill(bg_color)
        screen.blit(intro_bg, (150,20))
        # Display introductory message
        intro_message = font.render("PRESS SPACEBAR TO START", True, (255,255,255))
        screen.blit(intro_message, (180, 400))

        for event in pg.event.get():    
            if event.type == pg.QUIT: # To close window when x button is pressed
                intro = False
                running = False # Quit all loops
                main_loop = False
            elif event.type == pg.KEYDOWN: # To check whether any key is pressed
                if event.key == pg.K_SPACE:
                    intro = False

        pg.display.update() # Updates the changes to the window


    """GAME LOOP"""
    while running:

        # Pause loop
        while pause:
            for event in pg.event.get():    
                if event.type == pg.QUIT: # To close window when x button is pressed
                    pause = False
                    main_loop = False
                    running = False # Quit all loops
                elif event.type == pg.KEYDOWN: # To check whether any key is pressed
                    if event.key == pg.K_p:
                        pause = False

        pg.display.update() # Updates the changes to the window

        # Change the background color, RGB tuple
        screen.fill(bg_color)
        
        pg.draw.line(screen, (255,255,255), (0,525), (800,525), 5)
        #pg.display.update()

        # Adding BG image
        #screen.blit(bg_img, (0,0)) # This increases the time taken to execute each while loop thus, increase the speeds
        
        # Events
        for event in pg.event.get():
            
            if event.type == pg.QUIT: # To close window when x button is pressed
                running = False
                main_loop = False
                
            # Moving the player    
            if event.type == pg.KEYDOWN: # To check whether any key is pressed
                if event.key == pg.K_a:
                    playerX_change = -player_speed # To move left             
                elif event.key == pg.K_d:
                    playerX_change = player_speed # To move right
                    
                # For the bullet
                elif event.key == pg.K_SPACE:
                    if bullet_state == "ready":
                        mixer.Sound("audio/shoot.wav").play()
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)

                # For pausing the game
                elif event.key == pg.K_p and canYouPause:
                    pause_message = big_font.render("PAUSED", True, (255,255,255))
                    screen.blit(pause_message, (290, 270))
                    pause = True
                    
            if event.type == pg.KEYUP: # When key is released
                if event.key == pg.K_a or event.key == pg.K_d:
                    playerX_change = 0
                    
        
        # Moving the player
        playerX += playerX_change
        # To ensure player remains in the screen boundaries
        if playerX > 736:
            playerX = 736
        if playerX < 0:
            playerX = 0
            
        # Enemy Movement
        for i in range(n_enemies):

            # GAME OVER
            distance = math.sqrt((enemyX[i] - playerX)**2 + (enemyY[i] - playerY)**2)

            if enemyY[i] > 480 or distance < 15:
                mixer.Sound("audio/gameover.wav").play()
                for j in range(n_enemies):
                    enemyY[j] = 2000
                canYouPause = False # Pause functionality removed when game
                screen.fill([10,10,10])
                pg.display.update()
                over_text = big_font.render("GAME OVER", True, (255,255,255))
                screen.blit(over_text, (210, 270))
                #again = font.render("The game restarts in 5 seconds", True, (255, 255, 255))
                #screen.blit(again, (155, 330))
                pg.display.update()
                """
                sys.stdout.flush()
                time.sleep(5)
                sys.stdout.flush()
                """
                running = False
                break # Else enemies will still move at new coordinates

            enemyX[i] += enemyX_change[i]
            if enemyX[i] >= 736: # Equality is important. (no puns intended lmao)
                enemyX_change[i] = -enemy_speed[i]
                enemyY[i] += enemyY_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = enemy_speed[i]
                enemyY[i] += enemyY_change[i]
                
            # Collision Mechanics
            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            #distance = math.sqrt((enemyX[i] - playerX)**2 + (enemyY[i] - playerY)**2)
            if collision:
                screen.blit(explosion, (enemyX[i], enemyY[i]))
                #pg.display.update()
                pg.time.delay(40)
                mixer.Sound("audio/explosion.wav").play()
                # Reload bullet
                bulletY = 480
                bullet_state = "ready"
                
                # Enemy dies, new enemy spawned
                enemyImg[i] = pg.image.load(random.choice(enemy_list))
                enemyX[i] = random.randint(0, 735) 
                enemyY[i] = random.randint(50, 150) 
                enemyX_change[i] = (random.choice(speed_list))
                enemy_speed[i] = (random.choice(speed_list))
                
                score_value += 1

                # Difficulty Progression
                if score_value in range(5, 10):
                    speed_list += 0.1
                elif score_value in range(10, 15):
                    speed_list += 0.25 
                elif score_value > 20:
                    speed_list += 0.5
            
            # Calling enemy
            enemy(enemyX[i], enemyY[i], i)
        

        # Bullet Movement
        if bulletY < 0:
            bulletY = 480
            bullet_state = "ready"
            
        if bullet_state == "fire" : 
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change
        
        # Calling the player
        player(playerX, playerY) # To be called below the screen.fill else the filled screen will appear on top of the player
        show_score(scoreX, scoreY)

        pg.display.update() # Updates the changes to the window

"""
References: 
icons, introductory logo = http://www.classicgaming.cc/classics/space-invaders/
fonts: dafont.com
"""