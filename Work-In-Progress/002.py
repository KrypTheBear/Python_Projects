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

# Required parameters and variables

amount_of_enemies = 0
free_numbers = list(range(1,101))
enemies = []
clock = pygame.time.Clock()
gameover = False
gamestate = "active"

# Avoiding a lot of headaches

try:

    # === CLASSES ===

    class Enemy:

    	projectilecount = 0

    	def __init__(self, name, hp, dmg, speed, width, height):
    		self.name = name
    		self.hp = hp
    		self.dmg = dmg
    		self.speed = speed
    		self.width = width
    		self.height = height

    	def spawn(self,x,y):
    		amount_of_enemies = amount_of_enemies + 1
    		self.number = min(free_numbers)
    		free_numbers.remove(self.number)
    		self.ID = "Enemy" + str(self.number)
    		ID = self.ID
    		enemies.append(ID)
    		ID = pygame.Rect(x + self.width/2, y + self.height/2, self.width, self.height)

    	def __del__(self):
    		amount_of_enemies = amount_of_enemies - 1
    		free_numbers.append(self.number)
    		free_numbers.sort()
    		enemies.remove(ID)

    	def movement(self,direction):
    		if direction == "ru":
    			ID.x = ID.x + 10 * self.speed
    			ID.y = ID.y - 10 * self.speed
    		elif direction == "rd":
    			ID.x = ID.x + 10 * self.speed
    			ID.y = ID.y + 10 * self.speed
    		elif direction == "ld":
    			ID.x = ID.x - 10 * self.speed
    			ID.y = ID.y + 10 * self.speed
    		elif direction == "lu":
    			ID.x = ID.x - 10 * self.speed
    			ID.y = ID.y - 10 * self.speed
    		elif direction == "l":
    			ID.x = ID.x - 10 * self.speed
    		elif direction == "r":
    			ID.x = ID.x + 10 * self.speed
    		elif direction == "u":
    			ID.y = ID.y - 10 * self.speed
    		elif direction == "d":
    			ID.y = ID.y + 10 * self.speed
    		else:
    			raise Exception('Error in Enemy.movement, please use a proper direction!')

    	def fire(self, dmg, direction):
    		projectileID = ID + "Projectile" + str(projectilecount)
    		projectileID = Projectile(direction,10,dmg,(self.x,self.y))


    class Projectile:
    	def __init__(self,direction,speed,dmg,origin):
    		self.direction = direction
    		self.speed = speed
    		self.dmg = dmg

    	def movement(self,direction):
    		if direction == "ru":
    			ID.x = ID.x + 10 * self.speed
    			ID.y = ID.y - 10 * self.speed
    		elif direction == "rd":
    			ID.x = ID.x + 10 * self.speed
    			ID.y = ID.y + 10 * self.speed
    		elif direction == "ld":
    			ID.x = ID.x - 10 * self.speed
    			ID.y = ID.y + 10 * self.speed
    		elif direction == "lu":
    			ID.x = ID.x - 10 * self.speed
    			ID.y = ID.y - 10 * self.speed
    		elif direction == "l":
    			ID.x = ID.x - 10 * self.speed
    		elif direction == "r":
    			ID.x = ID.x + 10 * self.speed
    		elif direction == "u":
    			ID.y = ID.y - 10 * self.speed
    		elif direction == "d":
    			ID.y = ID.y + 10 * self.speed
    		else:
    			raise Exception('Error in Projectile.movement, please use a proper direction!')





    # === FUNCTIONS ===

        
    # Main loop
    while not gameover:
    
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameover = True
        
        # Game Logic
        

        # Drawing Logic
        gameDisplay.fill(BLACK)

        pygame.display.update()

        clock.tick(60)
        
except Exception as e:
    print(e)
    pygame.quit()
    sys.exit()

pygame.quit()
            
