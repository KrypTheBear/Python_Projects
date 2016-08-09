import pygame
import time
import sys
pygame.init()

# Color Constants

BLACK   = (  0,   0,   0)
WHITE   = (255, 255, 255)
RED     = (255,   0,   0)
GREEN   = (  0, 255,   0)
BLUE    = (  0,   0, 255)
YELLOW  = (255, 255,   0)

# Display Settings

gameDisplay = pygame.display.set_mode((1200,700),pygame.DOUBLEBUF)
pygame.display.set_caption('Yet another sidescroller')
font = pygame.font.SysFont("Segoe UI",75)

# Constants and Variables

amount_of_particles = 0
clock = pygame.time.Clock()
gameover = False

# Avoiding lots of headaches

try:
	'''
	class projectile:
		def __init__(self,direction,dmg,speed):
			self.direction = direction
			self.dmg = dmg
			self.speed = speed
		def __del__(self):
	'''
	class particle:

		def __init__(self,name,color,position,size):				# Position and Size are stored like (x,y), on the coordinate system and as width/height respectively
			self.name = name
			self.color = color
			self.position = position
			self.size = size

		def create(self):
			amount_of_particles = amount_of_particles + 1
			self.name + str(amount_of_particles) = 


	def particleMovement(Object):
	if Object.x <= 0:
		Object.x = 1200
	else:
		Object.x = Object.x - 10

	def displayObject(Object):
		pygame.draw.rect(gameDisplay, Object.color, Object)

	# def projectileMovement(Projectile):


	while not gameover:
		for event in pygame.event.get():
			if event.

		# Refreshing the screen
        gameDisplay.fill(BLACK)
        pygame.display.update()
        clock.tick(60)

# Just some random code, don't mind me

except Exception as e:
	print(e)
	pygame.quit()
	sys.exit()

pygame.quit()