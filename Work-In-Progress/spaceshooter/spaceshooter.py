'''
Written by WME/KrypTheBear
Python script responsible for game and display logic for the spaceshooter game

Changelog moved to README.md in this folder

    Pretty much done with the base structure. Remaining major TODOs:
        - Leave squares as hitboxes, replace their display with image file
        - Enemy AI
        - Level generation/Enemy spawn algorithm
'''

# === IMPORTED MODULES ===

import pygame                               # Required (obvious reasons)
import time                                 # Required (tickrate)
import sys                                  # Required for text (to be implemented)
import random                               # Required for RNG
import traceback                            # Useful for debugging. If removed: Replace traceback.print_exc() with print(e)
from settings import *
from classes import *

# === COLOR CONSTANTS ===

BLACK   = (  0,   0,   0)
WHITE   = (255, 255, 255)
RED     = (255,   0,   0)
GREEN   = (  0, 255,   0)
BLUE    = (  0,   0, 255)
YELLOW  = (255, 255,   0)

gameover = False

try:
    # === PARTICLES ===

    dust = particle(WHITE,(2,2),10,200,"l",True)
    for x in range(50):
        dust.create((random.randint(0,gameDisplayX),random.randint(0,gameDisplayY)))

    # === PROJECTILES ===

    maser = projectile(GREEN,(5,5),1,5,500,"r")

    # TODO: Enemies 

    evil1 = ship(RED,(50,50),000000,1,10)
    evil1.create((800,(0.5*gameDisplayY)))

    # TODO: Player ( Leaving the option for multiple player ships open for later. )

    player = ship(BLUE,(50,50),000000,1,1)
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
        if keys[119] and keys[115]:
            None                                        # Just like in my Pong project. Works just as intended.
        elif keys[119]:                                 # As to why I elif'ed U,D & R,L:
            player.movement("u")                        # You can't really press both at the same time, and if you do, nothing happens. The ship stops.
        elif keys[115]:
            player.movement("d")

        if keys[100] and keys[97]:
            None
        elif keys[100]:
            player.movement("r")
        elif keys[97]:
            player.movement("l")

        if keys[32]:
            now = time.time()
            if now - then > 0.1:
                maser.create((player.pool[0][0].x + player.size[0],player.pool[0][0].y + 1/2 * player.size[1]))         # Generate maser so it looks like it's coming from the middle-front of the ship
                then = now

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
