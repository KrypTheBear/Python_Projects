'''
Written by WME/KrypTheBear

Common abbreviations:

    oc = Object Class
    et = Enemy Type
    dmg = Damage
    lt = Last Tick ; ct = Current Tick; dt = Delta Time

'''

# === IMPORTED MODULES ===

import pygame                               # Required (obvious reasons)
import time                                 # Required (tickrate)
import sys                                  # Fonts, recommended
import random                               # RNG for particles, recommended

# Let there be light
pygame.init()

# === COLOR CONSTANTS ===

BLACK   = (  0,   0,   0)
WHITE   = (255, 255, 255)
RED     = (255,   0,   0)
GREEN   = (  0, 255,   0)
BLUE    = (  0,   0, 255)
YELLOW  = (255, 255,   0)

# === DISPLAY SETTINGS ===

gameDisplay = pygame.display.set_mode((1200,700),pygame.DOUBLEBUF|pygame.HWSURFACE)
pygame.display.set_caption('Yet another sidescroller')
font = pygame.font.SysFont("Segoe UI",75)

# === CONSTANTS AND VARIABLES ===

active_object_classes = []
particle_slots = list(range(1,101))
clock = pygame.time.Clock()
gameover = False

# Avoiding lots of headaches
try:
    # === CLASSES ===

    # TODO: Projectile Class, IDs, properties
    '''
    class projectile:
        def __init__(self,direction,dmg,speed):
            self.direction = direction
            self.dmg = dmg
            self.speed = speed
        def __del__(self):
    '''
    class particle:

        active_instances = []
        object_type = "particle"

        def __init__(self,name,color,size):               # Size is stored as (x,y), width and height respectively
            self.name = name
            self.color = color
            self.size = size
            active_object_classes.append(self)
            
        def create(self,position):                        # Position is stored as (x,y), just as on your typical coordinate system
            particle_number = min(particle_slots)
            ID = self.name + str(particle_number)
            ID = pygame.Rect(position[0], position[1], self.size[0], self.size[1])
            particle_slots.remove(particle_number)
            self.active_instances.append(ID)

    # === FUNCTIONS ===

    def particleMovement(Object_class):
        for Object in Object_class:
            if Object.x <= 0:
                Object.x = 1200
            else:
                Object.x = Object.x - 5

    def displayObjects(Object_class):
        for Object in Object_class.active_instances:
            pygame.draw.rect(gameDisplay, Object_class.color, Object)

    # TODO: def projectileMovement(Projectile):

    # === Particles ===

    dust = particle("dust",WHITE,(5,5))

    # TODO: Enemies

    # TODO: Player

    # Main Loop, runs after everything has been loaded (hopefully)
    while not gameover:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameover = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                dust.create(((random.randint(1,1200)),(random.randint(1,700)))) # (((random x between (1 - 1200)),(random y between (1 - 700))) combined into one (x,y) bracket. Sick.
        # Moving particles
        for oc in active_object_classes:
            if oc.object_type == "particle":
                particleMovement(oc.active_instances)

        # Refreshing and displaying the screen
        gameDisplay.fill(BLACK)
        for oc in active_object_classes:
            displayObjects(oc)
        pygame.display.update()
        clock.tick(120)
# Exception handling
# TODO: Don't let the program crash everytime, instead "catch" exceptions 

except Exception as e:
    print(e)
    pygame.quit()
    sys.exit()

pygame.quit()
