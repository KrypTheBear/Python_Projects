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
'''

# === IMPORTED MODULES ===

import pygame                               # Required (obvious reasons)
import time                                 # Required (tickrate)
import sys                                  # Fonts, recommended. If removed: 
import random                               # RNG for particles, recommended. If removed: Edit line 106
import traceback                            # Useful for debugging. If removed: Remove line 123, replace with 'print(e)'

pygame.init()

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

active_object_classes = []
particle_limit = 100
ship_limit = 20
clock = pygame.time.Clock()
gameover = False

try:
    # === CLASSES ===

    class particle:

        object_type = "particle"
        particle_amount = 0

        def __init__(self,color,size,name):                    # Size is stored as (x,y), width and height respectively, color from color constants (obviously)
            self.color = color
            self.size = size
            self.name = name
            active_object_classes.append(self)

        active_instances = {}
            
        def create(self,position):                        # Position is stored as (x,y), just as on your typical coordinate system
            self.particle_amount += 1
            if self.particle_amount <= particle_limit:
                ID = pygame.Rect(position[0], position[1], self.size[0], self.size[1])          # In order to access the index, just use [particlename].active_instances[index]. 
                self.active_instances["%s%d" % (self.name, self.particle_amount)] = ID
            else:
                self.particle_amount =- 1
                print("Particle Limit Reached! %s not spawned!" % object_type)

        def destroy(self,instance):
            self.particle_number -= 1
            del self.active_instances[instance]

    # TODO: Projectile Class, IDs, properties

    class projectile(particle):                                     # I laughed after realizing that a projectile is basically a particle. 


        object_type = "projectile"
        particle_amount = 0

        def __init__(self,color,size,direction,dmg,speed,name):                                 
            particle.__init__(self,color,size,name)                    # Afterwards I was ashamed of myself cause this should've come to my mind faster.  
            self.direction = direction
            self.dmg = dmg
            self.speed = speed                                      # The difference between projectiles and particles is that projectiles collide with other objects
                                                                    # And happen to damage them, if they have a health bar.
        active_instances = {}        

        def create(self,position):
            particle.create(self,position)                                                  

        def destroy(self,number):  
            particle.destroy(self,number)                                                                 

    class ship:

        object_type = "ship"
        ship_amount = 0

        def __init__(self,color,size,name):
            self.color = color
            self.size = size
            self.name = name
            active_object_classes.append(self)

        active_instances = {}

        def create(self,position):
            self.ship_amount += 1
            if self.ship_amount <= ship_limit:
                ID = pygame.Rect(position[0], position[1], self.size[0], self.size[1])
                self.active_instances["%s%d" % (self.name, self.ship_amount)] = ID
            else:
                self.ship_amount =- 1
                print("Ship limit reached! %s not spawned!" % object_type)

        def destroy(self,instance):
            self.ship_amount -= 1
            del self.active_instances[instance]

        # def fire(self,number,prj_type):                       # Will be added once I finish the projectile class
            # projectile.create((self.active_instances[number].x,self.active_instances[number].y),prj_type)

    # === FUNCTIONS ===

    def particleMovement(oc):
        for Object in oc.active_instances.values():
            if Object.x <= 0:
                Object.x = 1200
            else:
                Object.x = Object.x - 5

    def displayObjects(Object_class):
        for Object in Object_class.active_instances.values():
            pygame.draw.rect(gameDisplay, Object_class.color, Object)

    # === PARTICLES ===

    dust = particle(WHITE,(5,5),"dust")
    for x in range(50):
        dust.create((random.randint(1,1200),random.randint(1,700)))

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
                    player.destroy("player1")
                else:
                    player.create((100,(0.5*gameDisplayY)))

        # Moving particles
        for oc in active_object_classes:
            if oc.object_type == "particle":
                particleMovement(oc)

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