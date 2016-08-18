import pygame
import sys
import time
import traceback

pygame.init()
pygame.key.set_repeat(10, 10)

BLACK   = (  0,   0,   0)
WHITE   = (255, 255, 255)
RED     = (255,   0,   0)
GREEN   = (  0, 255,   0)
BLUE    = (  0,   0, 255)
YELLOW  = (255, 255,   0)

gameDisplayX = 1200
gameDisplayY = 700
gameDisplay = pygame.display.set_mode((gameDisplayX,gameDisplayY),pygame.DOUBLEBUF)
pygame.display.set_caption('Yet another sidescroller')
font = pygame.font.SysFont("Segoe UI",75)

clock = pygame.time.Clock()
gameover = False

try:

    # Example: 
    # x = particle(GREEN,(10,10))
    # x is of particle class with parameters GREEN and (10,10)
    # x.color = GREEN
    # x.size = (10,10)
    class particle:

        def __init__(self,color,size)
            self.color = color
            self.size = size
            # Creating a private pool, works like: x.pool and not particle.pool
            self.pool = []
            # Filling pool after initializing is completed
            for x in range(50):
                # Generating particles outside the Viewport, rendering them "inactive"
                self.pool.append([pygame.Rect(-200, -200, self.size[0], self.size[1]),False])

        def create(self,position):
            # Fetching all tuples (Rectangle_Info,Status) ; item[0], item[1] respectively
            for item in pool:
                # Fetch Status from tuple
                if item[1] == False:
                    # Changing Rectangle.x to position(>x<,y)
                    item[0].x = position[0]
                    # Changing Rectangle.y to position(x,>y<)
                    item[0].y = position[1]
                    # Changing Status to "active"
                    item[1] = True
                    break

        def fetch_index(self,position):
            # Same idea as above, slightly changed
            index = 0
            for item in pool:
                index += 1
                if item[1] == True:
                    # Checking if the passed position matches any active item
                    if item[0].x == position[0] and item[0].y == position[1]:
                        # And returns the index, so we can use it (e.g. collision management)
                        return index
                        break

        def destroy(self,index):
            # Setting an item with defined index in our pool back to "inactive"
            self.pool[index][1] = False
            self.pool[index][0].x = -200
            self.pool[index][0].y = -200

        def displayparticles(self):
            for item in self.pool:
                pygame.draw.rect(gameDisplay, self.color, item[0])










except Exception:
    traceback.print_exc()
    pygame.quit()
    sys.exit()

print("Successfully exited the game")
pygame.quit()