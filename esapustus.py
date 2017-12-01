import pygame #importing modules
import random
import time
pygame.init() #initializing pygame      

display_width = 800 # resolution
display_height = 600

black = (0,0,0)
white = (255,255,255)

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
    speed = 4
    width = 100

    def __init__(self):
        self.resetPosition()
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

class Player(Esine):
    img = pygame.image.load('images/apustus.png') # Images
    width = 100

    def __init__(self):
        self.x = (display_width * 0.45) # cordinates for player
        self.y = (display_height * 0.82)
        self.points = 0
        Esine.__init__(self)

def start():
    player = Player()
    es = ES()
    game_loop(player, es)

def text_objects(text, font): #text
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_display(text): #text
    newText = pygame.font.Font('freesansbold.ttf',70)
    TextSurf, TextRect = text_objects(text, newText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update() # update display with text

    time.sleep(2) # wait 2 seconds
    start()

pointFont = pygame.font.Font('freesansbold.ttf', 20)

def drawPoints(player):
    textSurface = pointFont.render("Points: " + str(player.points), False, (0, 0, 0))
    gameDisplay.blit(textSurface, (0, 0))

def crash(): # if you hit the edge you will crash + crash text
    message_display('KaMErUS kUoLI')

def playerCollidesWithES(player, es):
    return player.rect.colliderect(es.rect)

def game_loop(player, es): # game
    
    gameExit = False
    
    while not gameExit: # logic loop
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.event.pump()
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]: # recording keystrokes and moving
            player.move(dX=-10)
        elif keys[pygame.K_RIGHT]:
            player.move(dX=10)
        elif keys[pygame.K_ESCAPE]:
            pygame.quit()
            quit()
        
        gameDisplay.fill(white) #drawing graphics
        gameDisplay.blit(player.img, (player.x, player.y))

        es.move(dY=es.speed)
        gameDisplay.blit(es.img, (es.x, es.y))

        drawPoints(player)

        if player.x > (display_width - player.width) or player.x < 0: # if you hit edge you DIE
            crash()
        elif playerCollidesWithES(player, es):
            player.points += es.point_value
            es.resetPosition()
        elif es.y > display_height:
            crash()

        pygame.display.update() # updating screen
        clock.tick(60) # fps

start()
pygame.quit() 
quit()
