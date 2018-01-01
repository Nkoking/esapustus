import pygame #importing modules
import random
import time
pygame.init() #initializing pygame      

display_width = 800 # resolution
display_height = 600

black = (0,0,0)
white = (255,255,255)
deaths = 0

gameDisplay = pygame.display.set_mode((display_width, display_height)) # setting resolution
pygame.display.set_caption('Ruoka apustus') # Text on the top of the window
clock = pygame.time.Clock() # tick

class Esine(): # Parent class for all objects
    def __init__(self):
        self.rect = self.img.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def move(self, dX=0, dY=0):
        self.x += dX
        self.y += dY
        self.rect.x = self.x
        self.rect.y = self.y

class ES(Esine): #Es class which extends esine class
    def __init__(self):
        self.speed = 7
        self.width = 100
        self.active = True
        self.resetPosition()
        self.stop()
        Esine.__init__(self)

    def resetPosition(self):
        rand = random.randrange(0, 99)
        if rand == 0:
            self.img = pygame.image.load('images/golden_es.png')
            self.point_value = 1000
        else:
            self.img = pygame.image.load('images/es.png')
            self.point_value = 1
        self.x = random.randrange(0, display_width - self.width)
        self.y = -30

    def stop(self):
        if self.active:
            self.speed = 7
        else: self.speed = 0
        self.active = not self.active 

class Player(Esine):
    img = pygame.image.load('images/apustus.png') # Images
    
    def __init__(self):
        self.x = (display_width * 0.45) # coordinates for player
        self.y = (display_height * 0.82)
        self.width = 100
        self.points = 0
        self.can_right = True
        self.can_left = True
        Esine.__init__(self)
    
def start():
    game_loop(Player(), ES())

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_display(text):
    newText = pygame.font.Font('freesansbold.ttf',30)
    TextSurf, TextRect = text_objects(text, newText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update() # update display with text
    time.sleep(2)
    start()

def drawPoints(player):
    pointFont = pygame.font.Font('freesansbold.ttf', 20)
    textSurface = pointFont.render("Points: " + str(player.points) + " Deaths: " + str(deaths), False, (0, 0, 0))
    gameDisplay.blit(textSurface, (0, 0))

def crash(text): # if you hit the edge you will crash + crash text
    global deaths
    deaths  += 1
    message_display(text)

def playerCollidesWithES(player, es):
    return player.rect.colliderect(es.rect)

def game_loop(player, es): # game

    while True: # logic loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.event.pump()
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] and player.can_left: # recording keystrokes and moving
            player.move(dX=-10)
        elif keys[pygame.K_RIGHT] and player.can_right:
            player.move(dX=10)
        elif keys[pygame.K_p]:
            es.stop()
        elif keys[pygame.K_ESCAPE]:
            pygame.quit()
            quit()
        
        gameDisplay.fill(white) #drawing graphics
        gameDisplay.blit(player.img, (player.x, player.y))

        es.move(dY=es.speed)
        gameDisplay.blit(es.img, (es.x, es.y))

        drawPoints(player)

        if player.x < 0:
            player.can_left = False
        else: player.can_left = True
        if player.x > (display_width - player.width):
            player.can_right = False
        else: player.can_right = True
            
        if playerCollidesWithES(player, es):
            player.points += es.point_value
            es.resetPosition()

        elif es.y > display_height:
            crash("You didnt catch the ES in time.")
            
        pygame.display.update() # updating screen
        clock.tick(60) # fps

start()
pygame.quit() 
quit()
