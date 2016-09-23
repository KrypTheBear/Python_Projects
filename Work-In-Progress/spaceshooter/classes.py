'''
Written by WME/KrypTheBear
Python script to load all game relevant classes for the spaceshooter game
Ver 1.1.5 - Now more pythonic!
'''

import pygame
import traceback
import time
from settings import *

then = time.time()
things_to_display = []
projectiles = []
ships = []
particles = []

try:
    class moving_thing:                     # Defining a superclass for all moving things in the game

        def __init__(self,color,size,speed,poolsize):
            self.color = color              # Accepted colors are found in COLOR CONSTANTS
            self.size = size                # Size is stored as a (XSize, YSize) pair
            self.speed = speed              # Speed is an integer (at best something between 1-20)
            # Creating a private pool
            self.pool = []
            # Filling pool after initializing is completed
            for x in range(poolsize):
                # Generating particles outside the Viewport(-200, -200), giving them the defined size(XSize, YSize), rendering them "inactive"
                self.pool.append([pygame.Rect(-200, -200, self.size[0], self.size[1]),False])
            things_to_display.append(self)

        def create(self,position):
            # Fetching all pairs (Rectangle_Info,Status) ; item[0], item[1] respectively
            for item in self.pool:
                # Fetch Status from one pair
                if not item[1]:
                    # Changing Rectangle.x to position(>x<,y)
                    item[0].x = position[0] - 0.5*self.size[0]
                    # Changing Rectangle.y to position(x,>y<)
                    item[0].y = position[1] - 0.5*self.size[1]
                    # Changing Status to "active"
                    item[1] = True
                    # End iteration, as we only create one instance
                    break
            

        def fetch_index(self,position):         # May become obsolete, leaving this here for now.
            # Same idea as above, slightly changed
            index = 0
            for item in pool:
                index += 1
                if item[1]:
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

        def movement(self,direction):                       # Direction MUST be L,R,U,D or logical combinations (LU, UR etc)
            # Fetching all pairs in pool
            for item in self.pool:
                # If active, move in defined direction
                if item[1]:
                    if item[0].y >= 0 + 10 * self.speed:
                        if direction == "u":
                            item[0].y -= 10 * self.speed
                            break
                    if item[0].y < gameDisplayY - 10 * self.speed - self.size[1]:
                        if direction == "d":
                            item[0].y += 10 * self.speed
                            break
                    if item[0].x < gameDisplayX - 10 * self.speed - self.size[0]:
                        if direction == "r":
                            item[0].x += 10 * self.speed
                            break
                    if item[0].x >= 0 + 10 * self.speed:
                        if direction == "l":
                            item[0].x -= 10 * self.speed
                            break

        def displaythings(self):
            for item in self.pool:
                if item[1]:
                    # Get position and color, display on gameDisplay

                    pygame.draw.rect(gameDisplay, self.color, item[0])
                    
    class particle(moving_thing):

        def __init__(self,color,size,speed,poolsize,direction,persistent):
            moving_thing.__init__(self,color,size,speed,poolsize)
            self.direction = direction
            self.persistent = persistent
            particles.append(self)

        def movement(self):
            index = -1
            if self.persistent:
                for item in self.pool:
                    if item[1]:
                        if item[0].x <= 0:
                            item[0].x = gameDisplayX - 20
                        elif item[0].x >= gameDisplayX:
                            item[0].x = 20
                        elif item[0].y <= 0:
                            item[0].y = gameDisplayY - 20
                        elif item[0].y >= gameDisplayY:
                            item[0].y = 20
                        else:
                            if self.direction == "u":
                                item[0].y -= 0.5 * self.speed
                            elif self.direction == "d":
                                item[0].y += 0.5 * self.speed
                            elif self.direction == "l":
                                item[0].x -= 0.5 * self.speed
                            elif self.direction == "r":
                                item[0].x += 0.5 * self.speed
            else:
                for item in self.pool:
                    index += 1
                    if item[1]:
                        if item[0].x <= 0 or item[0].x >= gameDisplayX or item[0].y <= 0 or item[0].y >= gameDisplayY:
                            self.destroy(index)

    class projectile(moving_thing):

        def __init__(self,color,size,dmg,speed,poolsize,direction):                                 
            moving_thing.__init__(self,color,size,speed,poolsize)
            self.dmg = dmg                              # dmg should be somewhere between 1-9 (TODO: Health points)              
            self.direction = direction
            projectiles.append(self)

        def movement(self):
            # Adding an index so we can destroy any objects outside of the viewport
            index = -1
            for item in self.pool:
                index += 1
                if item[1]:
                    if self.direction == "u":
                        item[0].y -= 2 * self.speed
                    elif self.direction == "d":
                        item[0].y += 2 * self.speed
                    elif self.direction == "l":
                        item[0].x -= 2 * self.speed
                    elif self.direction == "r":
                        item[0].x += 2 * self.speed
                    if item[0].x < 0 or item[0].x > gameDisplayX or item[0].y < 0 or item[0].y > gameDisplayY:
                        self.destroy(index)
            

    class ship(moving_thing):

        def __init__(self,color,size,weapons,speed,poolsize):
            moving_thing.__init__(self,color,size,speed,poolsize)
            # Weapons are stored like this:
            # 000000, with each number being a weapon slot
            # e.g. 102011 would mean: weapon 1 in slot 1,5,6 and weapon 2 in slot 3
            self.weapons = weapons
            ships.append(self)

        # TODO: def fire_weapon

        def check_collided(self):
            index = -1
            pool_objects = []
            for x in projectiles:
                for y in x.pool:
                    pool_objects.append(y[0])
            for item in self.pool:
                index += 1
                if item[1]:
                    if item[0].collidelist(pool_objects) != -1:
                        self.destroy(index)

except Exception:
    traceback.print_exc()
    pygame.quit()
    sys.exit()

now = time.time()
load_time = now - then
print("Loaded classes successfully. Time needed: %d" % load_time)
