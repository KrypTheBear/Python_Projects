'''
Written by WME/KrypTheBear
Common abbreviations:
    oc = Object Class
    et = Enemy Type
    dmg = Damage
    lt = Last Tick ; ct = Current Tick; dt = Delta Time
    prj = Projectile

    Changelog:

    15.08.2016 16:41 - Set back to old version(Github) cause current version(Local) is non-working banana-code. Added changelog and traceback. Cleaned up code.
               17:00 - Added ship class, first steps for projectiles.
               17:15 - Added variable screen height and width and placeholder player-ship.
    16.08.2016 09:00 - Reworked particle and ship classes. Added projectile class (Unfinished).
               13:32 - Reworked access to members of classes (Dictionary instead of list). Made code >slightly< more efficient.
               17:13 - Fixed TypeErrors and AttributeErrors, destroying ships is working now.
    17.08.2016 15:48 - Added ShipMovement, added controls for player (W,A,S,D).
    22.08.2016 12:00 - Massive class rework (pools, improved movement etc.) 
'''

# === IMPORTED MODULES ===

import pygame                               # Required (obvious reasons)
import time                                 # Required (tickrate)
import math                                 # Required (movement calculation)
import sys                                  # Fonts, recommended. If removed: 
import random                               # RNG for particles, recommended. If removed: Edit line 106
import traceback                            # Useful for debugging. If removed: Remove line 123, replace with 'print(e)'

pygame.init()
pygame.key.set_repeat(10, 10)

# === COLOR CONSTANTS ===

BLACK   = (  0,   0,   0)
WHITE   = (255, 255, 255)
RED     = (255,   0,   0)
GREEN   = (  0, 255,   0)
BLUE    = (  0,   0, 255)
YELLOW  = (255, 255,   0)

# === DISPLAY SETTINGS ===

gameDisplayX = 1200
gameDisplayY = 700
gameDisplay = pygame.display.set_mode((gameDisplayX,gameDisplayY),pygame.DOUBLEBUF)
pygame.display.set_caption('Yet another sidescroller')
font = pygame.font.SysFont("Segoe UI",75)

# === CONSTANTS AND VARIABLES ===

clock = pygame.time.Clock()
gameover = False

try:
    # === CLASSES ===

    class thing:

        def __init__(self,color,size):
            self.color = color
            self.size = size        # Size is a 
            # Creating a private pool, works like: x.pool and not particle.pool
            self.pool = []
            # Filling pool after initializing is completed
            for x in range(1000):
                # Generating particles outside the Viewport, rendering them "inactive"
                self.pool.append([pygame.Rect(-200, -200, self.size[0], self.size[1]),False])

        def create(self,position):
            # Fetching all pairs (Rectangle_Info,Status) ; item[0], item[1] respectively
            for item in self.pool:
                # Fetch Status from pair
                if item[1] == False:
                    # Changing Rectangle.x to position(>x<,y)
                    item[0].x = position[0] - 0.5*self.size[0]
                    # Changing Rectangle.y to position(x,>y<)
                    item[0].y = position[1] - 0.5*self.size[1]
                    # Changing Status to "active"
                    item[1] = True
                    break

        def fetch_index(self,position):         # May become obsolete
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

        def displaythings(self):
            for item in self.pool:
                if item[1] == True:
                    # Get position and color, display on gameDisplay
                    pygame.draw.rect(gameDisplay, self.color, item[0])

    class projectile(thing):

        def __init__(self,color,size,dmg,speed):                                 
            thing.__init__(self,color,size)
            self.dmg = dmg
            self.speed = speed     

        def create(self,position,direction):
            thing.create(self,position)
            self.direction = direction

        def projectilemovement(self):
            for item in self.pool:
                if item[1] == True:
                    if self.direction == "u":
                        item[0].y -= 10 * speed
                    elif self.direction == "ru":
                        item[0].x += sqrt(10 * speed)
                        item[0].y -= sqrt(10 * speed)
                    elif self.direction == "r":
                        item[0].x += 10 * speed
                    elif self.direction == "rd":
                        item[0].x += sqrt(10 * speed)
                        item[0].y += sqrt(10 * speed)
                    elif self.direction == "d":
                        item[0].y += 10 * speed
                    elif self.direction == "ld":
                        item[0].x -= sqrt(10 * speed)
                        item[0].y += sqrt(10 * speed)
                    elif self.direction == "l":
                        item[0].x -= 10 * speed
                    elif self.direction == "ul":
                        item[0].x -= sqrt(10 * speed)
                        item[0].y -= sqrt(10 * speed)


    class ship:

        def __init__(self,color,size):
            thing.__init__(self,color,size)

        def create(self,position):
            thing.destroy(self,position)

        def destroy(self,instance):
            self.ship_amount -= 1
            del self.active_instances[instance]

    # === FUNCTIONS ===

    def particleMovement(oc):
        for Object in oc.active_instances.values():
            if Object.x <= 0:
                Object.x = 1200
            else:
                Object.x = Object.x - 5

    def projectileMovement(oc):
        new_instances = {}
        for Object in oc.active_instances:
            if oc.active_instances[Object].x <= 0 or oc.active_instances[Object].x >= gameDisplayX:
                new_instances = oc.destroy("%s" % Object)
            elif oc.direction == "left":
                oc.active_instances[Object].x -= 10
                new_instances = oc.active_instances
            elif oc.direction == "right":
                oc.active_instances[Object].x += 10
                new_instances = oc.active_instances

        return new_instances

    def shipMovement(name,direction):
        Object = ship.active_instances[name]
        # Handling Movement for X - Coordinates
        if Object.x < 0:
            Object.x = 0
        elif Object.x + Object[2] > gameDisplayX:
            Object.x = gameDisplayX - Object[2]
        else:
            if direction == "left":
                Object.x -= 5
            elif direction == "right":
                Object.x += 5

        # Handling Movement for Y - Coordinates
        if Object.y < 0:
            Object.y = 0
        elif Object.y + Object[3] > gameDisplayY:
            Object.y = gameDisplayY - Object[3]
        else:
            if direction == "up":
                Object.y -= 5
            elif direction == "down":
                Object.y += 5
            
    def displayObjects(Object_class):
        for Object in Object_class.active_instances.values():
            pygame.draw.rect(gameDisplay, Object_class.color, Object)

    # === PARTICLES ===

    dust = particle(WHITE,(5,5),"dust")
    for x in range(50):
        dust.create((random.randint(1,1200),random.randint(1,700)))

    # === PROJECTILES ===

    maser = projectile(GREEN,(5,5),5,5,"maser")

    # TODO: Enemies ( Enemy class ( in classes ) and individual enemies ( here ) )

    # TODO: Player ( Leaving the option for multiple player ships open for later. )

    player = ship(BLUE,(50,50),"player")
    player.create((100,(0.5*gameDisplayY)))

    # Main Loop, runs after everything has been loaded.
    while not gameover:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameover = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if "player1" in ship.active_instances.keys():
                    player.destroy("player")
                else:
                    player.create((100,(0.5*gameDisplayY)))
                
        keys = pygame.key.get_pressed()                 # Since eventhandling can be quite bad if connected to movement
                                                        # (holding two buttons, releasing one) I moved this outside eventhandling.
        if keys[119] and keys[115]:
            None                                        # Just like in my Pong project. Works just as intended.
        elif keys[119]:                                 # As to why I elif'ed U,D & R,L:
            shipMovement("player","up")                 # You can't really press both at the same time, and if you do, nothing happens. The ship stops.
        elif keys[115]:
            shipMovement("player","down")

        if keys[100] and keys[97]:
            None
        elif keys[100]:
            shipMovement("player","right")
        elif keys[97]:
            shipMovement("player","left")

        if keys[32]:
            maser.create((player.active_instances["player"].x,player.active_instances["player"].y),"right")
            print("Maser created")

        # Moving particles
        for oc in active_object_classes:                # Just in case I wish to seperate certain particles from others (like explosions)
            if oc.object_type == "particle":
                particleMovement(oc)
            if oc.object_type == "projectile":
                oc.active_instances = projectileMovement(oc)

        # Refreshing and displaying the screen
        gameDisplay.fill(BLACK)
        for oc in active_object_classes:
            displayObjects(oc)
        pygame.display.update()
        clock.tick(120)                         # Pygame is very very VERY terrible at vsync. Having an relatively high clock/display rate allows me to not care about vsync.

# Exception handling 

except Exception as e:
    traceback.print_exc()
    pygame.quit()
    sys.exit()

pygame.quit()