'''
Written by WME/KrypTheBear
Common abbreviations:
    et = Enemy Type
    dmg = Damage
    prj = Projectile
    l, r, u, d = Left, Right, Up, Down, works in combinations (l/r | u/d)

    Changelog:

    15.08.2016 16:41 - Set back to old version(Github) cause current version(Local) is non-working banana-code. Added changelog and traceback. Cleaned up code.
               17:00 - Added ship class, first steps for projectiles.
               17:15 - Added variable screen height and width and placeholder player-ship.
    16.08.2016 09:00 - Reworked particle and ship classes. Added projectile class (Unfinished).
               13:32 - Reworked access to members of classes (Dictionary instead of list). Made code >slightly< more efficient.
               17:13 - Fixed TypeErrors and AttributeErrors, destroying ships is working now.
    17.08.2016 15:48 - Added ShipMovement, added controls for player (W,A,S,D).
    22.08.2016 12:00 - Massive class rework (pools, improved movement etc.)
    29.08.2016 17:00 - Updated functions, classes, movement calls, rewrote some comments
'''

# === IMPORTED MODULES ===

import pygame                               # Required (obvious reasons)
import time                                 # Required (tickrate)
from math import sqrt                       # Required (movement calculation), not taking whole math cause we only need square root
import sys                                  # Fonts, recommended. If removed: 
import random                               # RNG for particles, recommended. If removed: Edit line 106
import traceback                            # Useful for debugging. If removed: Remove line 123, replace with 'print(e)'

pygame.init()
pygame.key.set_repeat(10, 10)               # Making sure we can actually hold down keys by repeating input

# === COLOR CONSTANTS ===

BLACK   = (  0,   0,   0)
WHITE   = (255, 255, 255)
RED     = (255,   0,   0)
GREEN   = (  0, 255,   0)
BLUE    = (  0,   0, 255)
YELLOW  = (255, 255,   0)

# === DISPLAY SETTINGS ===

gameDisplayX = 1200                         # X,Y can be anything within your monitor resolution
gameDisplayY = 700
gameDisplay = pygame.display.set_mode((gameDisplayX,gameDisplayY),pygame.DOUBLEBUF)
pygame.display.set_caption('Yet another sidescroller')
font = pygame.font.SysFont("Segoe UI",75)

# === CONSTANTS AND VARIABLES ===

clock = pygame.time.Clock()
gameover = False

try:
    # === CLASSES ===

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

        def create(self,position):
            # Fetching all pairs (Rectangle_Info,Status) ; item[0], item[1] respectively
            for item in self.pool:
                # Fetch Status from one pair
                if item[1] == False:
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

        def movement(self,direction):                       # Direction MUST be L,R,U,D or logical combinations (LU, UR etc)
            # Fetching all pairs in pool
            for item in self.pool:
                # If active, move in defined direction
                if item[1] == True:
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
                if item[1] == True:
                    # Get position and color, display on gameDisplay
                    pygame.draw.rect(gameDisplay, self.color, item[0])
                    

    class projectile(moving_thing):

        def __init__(self,color,size,dmg,speed,poolsize):                                 
            moving_thing.__init__(self,color,size,speed,poolsize)
            self.dmg = dmg                              # dmg should be somewhere between 1-9 (TODO: Health points)              

        # TODO def collision
            

    class ship(moving_thing):

        def __init__(self,color,size,weapons,speed,poolsize):
            moving_thing.__init__(self,color,size,speed,poolsize)
            # Weapons are stored like this:
            # 000000, with each number being a weapon slot
            # e.g. 102011 would mean: weapon 1 in slot 1,5,6 and weapon 2 in slot 3
            self.weapons = weapons

        # TODO: def fire_weapon

        # TODO: conditional on ship.destroy

    # === FUNCTIONS ===

    # A lot of obsolete functions removed - 29.08.2016 16:43
    # TODO: Do I actually need functions or will I just stuff classes?
    # Consideration: Exporting classes into a seperate .py, importing this on startup
    # Should avoid cluttering

    # === PARTICLES ===

    dust = moving_thing(WHITE,(20,20),10,200)

    # === PROJECTILES ===

    maser = projectile(GREEN,(5,5),1,10,500)

    # TODO: Enemies ( Enemy class ( in classes ) and individual enemies ( here ) )

    # TODO: Player ( Leaving the option for multiple player ships open for later. )

    player = ship(BLUE,(50,50),000000,1,1)
    player.create((100,(0.5*gameDisplayY)))

    # Main Loop, runs after everything has been loaded.
    while not gameover:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameover = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if player.pool[0] == True:
                    player.destroy(0)
                else:
                    player.create((100,(0.5*gameDisplayY)))
                
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
            maser.create((player.pool[0][0].x,player.pool[0][0].y))
            print("Maser created")

        # TODO: Write particle movement handling

        # Refreshing and displaying the screen
        gameDisplay.fill(BLACK)
        player.displaythings()
        maser.displaythings()
        dust.displaythings()
        pygame.display.update()
        clock.tick(120)                         # Pygame is very very VERY terrible at vsync. Having an relatively high clock/display rate allows me to not care about vsync.

# Exception handling 

except Exception as e:
    traceback.print_exc()
    pygame.quit()
    sys.exit()

pygame.quit()
