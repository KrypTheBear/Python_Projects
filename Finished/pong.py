'''
Written by WME/KrypTheBear

Common abbreviations:
    
    L,R,U,D = Left, Right, Up, Down (as well as any combination, e.g. lu, rd)
    direct = direction
    AI = Artifical Intelligence (Sidemark: This example of AI isn't really intelligent. Just tracking the ball.)

'''

# === IMPORTED MODULES ===

import pygame               # Required (obvious reasons)
import time                 # Required (Tickrate)
import sys                  # Fonts, recommended

# Let there be light
pygame.init()


# === COLOR CONSTANTS ===

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)

# === DISPLAY SETTINGS ===

gameDisplay = pygame.display.set_mode((1200,700),pygame.DOUBLEBUF)
pygame.display.set_caption('Pong I guess')
font = pygame.font.SysFont("Segoe UI",75)

# === CONSTANTS, PARAMETERS AND VARIABLES ===

clock = pygame.time.Clock()
playerPaddle = pygame.Rect(50, 300, 20, 100)
AIPaddle = pygame.Rect(1130, 300, 20, 100)
Ball = pygame.Rect(400, 0, 20, 20)
Ball.x = 590
Ball.y = 290
difficultyfactor = 0.9
gameover = False
gamestate = "started"

# Starting direction and score
direction = "ld"
scorePlayer = 0
scoreAI = 0

# Function to render the score onto the screen
def scoreboard(player,AI):
    plyscore = font.render(str(player), 0, WHITE, BLACK)
    AIscore = font.render(str(AI), 0, WHITE, BLACK)
    gameDisplay.blit(plyscore, (100,-25))
    gameDisplay.blit(AIscore, (1050,-25))
    pygame.display.update()

# Function for any other text to be displayed on the screen (Starts at y = 300px, x is variable)
def othertext(text,x):
    gameDisplay.blit(font.render(str(text), 0, WHITE, BLACK), (x,300))
    pygame.display.update()

# Flips the Ball's direction on numerous occaisions
def direction_flip(what,where):
    if what == 1:                   # Case 1: Contact with the ceiling or floor
        if where == "lu":
            where = "ld"
        elif where == "ru":
            where = "rd"
        elif where == "ld":
            where = "lu"
        elif where == "rd":
            where = "ru"
    elif what == 2:                 # Case 2: Contact with either rudder
        if where == "lu":
            where = "ru"
        elif where == "ld":
            where = "rd"
        elif where == "ru":
            where = "lu"
        elif where == "rd":
            where = "ld"

    return where                    # Returns the new direction

# Function to determine the Ball's movement        
def Ball_Movement(direct):                           
    if Ball.y < 100:                           # Ball hits the ceiling                   
        direct = direction_flip(1,direct)
        Ball.y = 110
    elif Ball.y > 690:                         # Ball hits the floor
        direct = direction_flip(1,direct)
        Ball.y = 680
    if direct == "ru":
        Ball.x = Ball.x + 10
        Ball.y = Ball.y - 10
    elif direct == "rd":
        Ball.x = Ball.x + 10
        Ball.y = Ball.y + 10
    elif direct == "lu":
        Ball.x = Ball.x - 10
        Ball.y = Ball.y - 10
    elif direct == "ld":
        Ball.x = Ball.x - 10
        Ball.y = Ball.y + 10

    return direct                           

# Function to check if the Ball has collided with a rudder
def Collision(Object,direct):
    if Object.colliderect(Ball):
        if direct == "lu" or direct == "ld":            
            Ball.x = Ball.x + 10                        # Pushing the Ball a bit away from whatever it collided with
        elif direct == "rd" or direct == "ru":          # just to avoid a permanent collision
            Ball.x = Ball.x - 10
        return True
    else:
        return False

# Main-loop
while not gameover:
    try:
        # A "main menu" while-loop, so the game doesn't simply start without the player being ready
        while gamestate == "started" and not gameover:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameover = True
                elif event.type in (MOUSEBUTTONDOWN, KEYDOWN)
                    gamestate = "game"
            # Updating and Refreshing the screen/viewport
            gameDisplay.fill(BLACK)
            othertext("Press any button to start the game",50)
            pygame.display.update()
            clock.tick(70)
        
        # Actual game while-loop   
        while gamestate == "game" and not gameover:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameover = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        difficultyfactor = difficultyfactor + 0.05
                        othertext("Difficulty increased!",300)
                        pygame.time.wait(500)
                    elif event.button == 5:
                        difficultyfactor = difficultyfactor - 0.05
                        othertext("Difficulty decreased!",300)
                        pygame.time.wait(500)
                    else:
                        gamestate = "paused"
            # Anything mouse related, except for mouse events
            (mouseX, mouseY) = pygame.mouse.get_pos()               # Tracking the position of the mouse, as to why this isn't in events: The mouse would STOP being tracked if it would be on MOUSEMOVEMENT
            distance = playerPaddle.y - (mouseY-50)                 # Distance from the mouse to the CENTER of the rectangle
        
            # Player rudder movement
            if distance > 5:
                playerPaddle.y = playerPaddle.y - 10
            elif distance < -5:
                playerPaddle.y = playerPaddle.y + 10
            else:
                playerPaddle.y = mouseY - 50

            # AI rudder movement
            distanceAI = AIPaddle.y - (Ball.y - 50)
            if distanceAI > 5:
                AIPaddle.y = AIPaddle.y - 10 * difficultyfactor
            elif distance < -5:
                AIPaddle.y = AIPaddle.y + 10 * difficultyfactor
            else:
                AIPaddle.y = Ball.y - 50
        

            # If the player hits the ball it flies into the opposite direction
            if Collision(playerPaddle,direction):
                direction = direction_flip(2,direction)

            # If the AI hits the ball it flies into the opposite direction
            elif Collision(AIPaddle,direction):
                direction = direction_flip(2,direction)
        
            # Preventing the rectangles from crossing the top border
            if playerPaddle.y < 100:
                playerPaddle.y = 100
            if AIPaddle.y < 100:
                AIPaddle.y = 100

            # Preventing the rectangles from crossing the floor
            if playerPaddle.y > 600:
                playerPaddle.y = 600
            if AIPaddle.y > 600:
                AIPaddle.y = 600

            # Calling Movement, changing direction if necessary.
            direction = Ball_Movement(direction)

            # Detecting whether the Ball has passed the left or right border, scoring accordingly
            if Ball.x <= 0:
                scoreAI = scoreAI + 1
                Ball.x = 900
            elif Ball.x >= 1200:
                scorePlayer = scorePlayer + 1
                Ball.x = 300

            # Updating and Refreshing the screen
            gameDisplay.fill(BLACK)
            pygame.draw.rect(gameDisplay, WHITE, playerPaddle)
            pygame.draw.rect(gameDisplay, WHITE, AIPaddle)
            pygame.draw.rect(gameDisplay, WHITE, Ball)
            pygame.draw.line(gameDisplay, WHITE, (0,90), (1200,90), 20)
            scoreboard(scorePlayer,scoreAI)
            pygame.display.update()

            clock.tick(70)

        # A simple pause-function, triggered by pressing any mouse button other than the mousewheel
        while gamestate == "paused" and not gameover:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameover = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    gamestate = "game"
            # Writing "===PAUSED===" and refreshing the screen
            othertext("===PAUSED===",325)
            pygame.display.update()
            clock.tick(70)
    
    # Exception handling
    # TODO: Prevent the program from crashing, should an Exception be raised
    # Which >isn't< going to happen       
    except Exception as e:
        print(e)
        pygame.quit()
        sys.exit()
        
pygame.quit()
