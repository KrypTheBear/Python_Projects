'''
Written by WME/KrypTheBear
Python script to load all game relevant classes for the spaceshooter game
CLASSES Ver 1.2.1 - Now more pythonic!
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
    '''
    Moving_thing superclass for all moving things in the game.

    Methods:
        __init__(parameters): 
            - Saving all relevant parameters in self.parameter (color, size, speed)
            - Filling a private pool (self.pool) with inactive objects, which has a limited poolsize
            - Appending to list of classes whose objects can be displayed (things_to_display)

        create((x,y)):
            - Changing one object (the lowest in the list) to active status
            - Moving to position (x,y)

        destroy(index)
            - sets an item matching the given index in the pool back to inactive status and resets it's position to (-200,-200)

        movement(direction)
            - Function responsible for moving all active objects in the pool in a certain direction
            - TODO: Change to independant movement? Assign direction var to items in pool?

        displaythings()
            - Displays all active items in pool

    Parameters:
        - color: constant, found in COLOR CONSTANTS in settings.py
        - size: stored as a (XSize, YSize) pair, XSize & YSize are integers
        - speed: Integer value (recommended var: between 1-20)
        - poolsize: Integer value, defines the range of the pool
        - x,y: Integer value, should usually be in range(gameDisplayX),range(gameDisplayY), except when destroying items
        - direction: String value, "u","d","l","r" (case sensitive, lowercase only)
    '''
    class moving_thing:

        def __init__(self,color,size,speed,poolsize):
            self.color = color
            self.size = size
            self.speed = speed
            self.pool = []
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

        def destroy(self,index):
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
                            continue
                    if item[0].y < gameDisplayY - 10 * self.speed - self.size[1]:
                        if direction == "d":
                            item[0].y += 10 * self.speed
                            continue
                    if item[0].x < gameDisplayX - 10 * self.speed - self.size[0]:
                        if direction == "r":
                            item[0].x += 10 * self.speed
                            continue
                    if item[0].x >= 0 + 10 * self.speed:
                        if direction == "l":
                            item[0].x -= 10 * self.speed
                            continue

        def displaythings(self):
            for item in self.pool:
                if item[1]:
                    # Get position and color, display on gameDisplay
                    pygame.draw.rect(gameDisplay, self.color, item[0])

    '''
    Particle class inheriting from moving_thing class

    Methods:
        __init__(parameters):
            - color, size, speed, poolsize same as moving_thing
            - Direction is predefined and saved in self (can be changed in runtime, name.direction = newdirect)
            - Persistence states whether a particle is destroyed after reaching the border of the game display
            - self is appended to both things_to_display and particles

        movement():
            - Checks if class object is persistent
            - If persistent: Move active items in self.pool in specified direction, once it reaches the border: Let item respawn on the other side
            - If not persistent: Move active items in self.pool in specified direction, once it reaches the border: destroy item
    '''                
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

        def __init__(self,color,size,weapons,speed,poolsize,blit_name=None):
            moving_thing.__init__(self,color,size,speed,poolsize)
            # Weapons are stored like this:
            # 000000, with each number being a weapon slot
            # e.g. 102011 would mean: weapon 1 in slot 1,5,6 and weapon 2 in slot 3
            self.weapons = weapons
            self.blit_name = blit_name
            ships.append(self)

        # TODO: def fire_weapon

        def check_collided(self):
            index = -1
            pool_objects = []
            for x in projectiles:
                for y in x.pool:
                    if y[1]:
                        pool_objects.append(y[0])
            for x in ships:
                for y in x.pool:
                    if y[1]:
                        pool_objects.append(y[0])
            for x in self.pool:
                if x[1]:
                    pool_objects.remove(x[0])
            for item in self.pool:
                index += 1
                if item[1]:
                    if item[0].collidelist(pool_objects) != -1:
                        self.destroy(index)

        def displaythings(self):
            if self.blit_name:
                for item in self.pool:
                    if item[1]:
                        pygame.Surface.blit(gameDisplay,self.blit_name,item[0])
            else:
                for item in self.pool:
                    if item[1]:
                        pygame.draw.rect(gameDisplay, self.color, item[0])

    def playermovement(keys,player):
        if keys[119] and keys[115]:
            None                                        # You can't really press both at the same time, and if you do, nothing happens. The ship stops.
        elif keys[119]:                                 
            player.movement("u")                        
        elif keys[115]:
            player.movement("d")

        if keys[100] and keys[97]:
            None
        elif keys[100]:
            player.movement("r")
        elif keys[97]:
            player.movement("l")

except Exception:
    traceback.print_exc()
    pygame.quit()
    sys.exit()

now = time.time()
load_time = now - then
print("Loaded classes successfully. Time needed: %d" % load_time)
