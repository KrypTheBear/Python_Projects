'''
Written by WME/KrypTheBear
Python script to load all the settings needed for the spaceshooter game
Ver 0.2.0
Required functions:
    - Change settings ingame
'''

import pygame
import traceback
import time


try:
    then = time.time()
    pygame.init()
    pygame.key.set_repeat(10, 10)               # Making sure we can actually hold down keys by repeating input

    gameDisplayX = 1200                         # X,Y can be anything within your monitor resolution
    gameDisplayY = 700
    gameDisplay = pygame.display.set_mode((gameDisplayX,gameDisplayY),pygame.DOUBLEBUF)

    pygame.display.set_caption('Yet another sidescroller')
    font = pygame.font.SysFont("Segoe UI",75)

    clock = pygame.time.Clock()
    
except Exception:
    traceback.print_exc()
    pygame.quit()
    sys.exit()

now = time.time()
load_time = now - then
print("Loaded settings successfully. Time needed: %d" % load_time)