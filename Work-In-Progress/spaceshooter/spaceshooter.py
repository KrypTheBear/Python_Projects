'''
Written by WME/KrypTheBear
Python script responsible for game and display logic for the spaceshooter game

MAIN FILE Ver 0.5.0
Changelog moved to README.md in this folder

    Pretty much done with the base structure. Remaining major TODOs:
        - Leave squares as hitboxes, replace their display with image file (Pretty much done! I want a function for this. Currently it has to be re-coded per image file)
        - Enemy AI
        - Level generation/Enemy spawn algorithm (Thought: Spawn zone behind the screen, enemies move in, player has enough time to adjust.)
'''

# === IMPORTED MODULES ===

import pygame                               # Required (obvious reasons)
import time                                 # Required (tickrate)
import sys                                  # Required for text (to be implemented)
import random                               # Required for RNG
import traceback                            # Useful for debugging. If removed: Replace traceback.print_exc() with print(e)
from settings import *
from helper import *

# === COLOR CONSTANTS(RGB) ===

BLACK   = (  0,   0,   0)
WHITE   = (255, 255, 255)
RED     = (255,   0,   0)
GREEN   = (  0, 255,   0)
BLUE    = (  0,   0, 255)
YELLOW  = (255, 255,   0)

gameover = False

try:

    # === SPRITES ===
    # Tried to use a helper, pygame requires all of these to be done in this order, without helper functions.
    arctus = pygame.image.load("Arctus.png")
    arctus.convert_alpha()
    arctus = pygame.transform.rotate(arctus,90)
    ghosthawk = pygame.image.load("Ghosthawk.png")
    ghosthawk.convert_alpha()
    ghosthawk = pygame.transform.rotate(ghosthawk,270)

    # === PARTICLES ===

    dust = particle(WHITE,(2,2),10,200,"l",True)
    for x in range(50):
        dust.create((random.randint(0,gameDisplayX),random.randint(0,gameDisplayY)))

    # === PROJECTILES ===

    maser = projectile(GREEN,(5,5),1,5,500,"r")

    # TODO: Enemies 

    evil1 = ship(RED,(50,50),000000,0.25,10,arctus)
    evil1.create((800,(0.5*gameDisplayY)))

    # TODO: Player ( Leaving the option for multiple player ships open for later. )

    player = ship(BLUE,(50,50),000000,1,1,ghosthawk)
    player.create((100,(0.5*gameDisplayY)))

    # Main Loop, runs after everything has been loaded.
    then = time.time()
    while not gameover:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameover = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                evil1.create((800,random.randint(100,gameDisplayY-100)))
                
        keys = pygame.key.get_pressed()                 # Since eventhandling can be quite bad if connected to movement
                                                        # (holding two buttons, releasing one) I moved this outside eventhandling.
        playermovement(keys,player)

        if keys[32]:
            now = time.time()
            if now - then > 0.1:
                maser.create((player.pool[0][0].x + player.size[0],player.pool[0][0].y + 1/2 * player.size[1]))         # Generate maser so it looks like it's coming from the middle-front of the ship
                then = now

        evil1.movement("l")

        for item in projectiles:
            item.movement()
        for item in ships:
            item.check_collided()
        for item in particles:
            item.movement()

        # Refreshing and displaying the screen
        gameDisplay.fill(BLACK)
        for item in things_to_display:          # Using a list of items to display so I don't have to spam lines of "displaythings()"
            item.displaythings()
        pygame.display.update()
        clock.tick(120)                         # Pygame is very very VERY terrible at vsync. Having an relatively high clock/display rate allows me to not care about vsync.
        

# Exception handling 

except Exception as e:
    traceback.print_exc()
    pygame.quit()
    sys.exit()

pygame.quit()
