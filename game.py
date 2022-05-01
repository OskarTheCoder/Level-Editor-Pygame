import pygame
from pygame.locals import *;
import random
import time

# Level 1 == "data"
area = "data"

class PLAYER():
    def __init__(self, pos, speed):
        self.down = [pygame.image.load("player/player_down_1.png")]
        self.img = pygame.transform.scale( self.down[0], (24,34) )
        self.pos = pos
        self.dirX = 0
        self.dirY = 0
        self.speed = speed
        self.tick = 0

    def draw(self, screen):
        screen.blit(self.img, self.pos)

    def move(self):
        self.tick+=1


    def collision(self, other):
        return pygame.rect.Rect.colliderect(self.img.get_rect(topleft=(self.pos[0],self.pos[1])), other)

# Load Tiles
tiles = []
actualTile = []
i = 1
tile = ""
start=False
TheContentIs = ""
with open(f"graphics/{area}.txt","r") as file:
    for line in file:
        TheContentIs = line
        for char in line:
            if start == True:
                if char == "#":
                    start = False
                    i+=1
                    actualTile.append(tile)
                    if (i > 3):
                        tiles.append(actualTile)
                        i = 1
                        actualTile = []
                else:
                    tile += char
            else:
                if char == "#":
                    start = True
                    tile = ""

file.close()

tilezToRemove = []
for r in range(1,len(tiles)):
    if tiles[r] == tiles[r-1]:
        tilezToRemove.append(tiles[r-1])
    
for g in tilezToRemove:
    tiles.remove(g)

#print(tiles)

steps = 0

def getPixelmon(area):
    return "Pixelmon"

def calculateChance(steps):
    print(steps)
    chance = 1 + (steps*2)//5
    num = random.randint(1,1000)
    if num <= chance:
        return True
    else:
        return False

def encounter(SCREEN, area):
    print("Encounter Started!")
     
    xx = 0
    xX = WIDTH-WIDTH//10

    yy = 0
    yY = HEIGHT-HEIGHT//10

    # Play The Animation
    for i in range(5):
        pygame.draw.rect(SCREEN, ((255,255,255)), (xx,0,WIDTH//10,HEIGHT))
        pygame.draw.rect(SCREEN, ((255,255,255)), (xX,0,WIDTH//10,HEIGHT))
        
        pygame.draw.rect(SCREEN, ((255,255,255)), (0,yy,WIDTH,HEIGHT//10))
        pygame.draw.rect(SCREEN, ((255,255,255)), (0,yY,WIDTH,HEIGHT//10))

        xx += WIDTH//10
        xX -= WIDTH//10
        yy += HEIGHT//10
        yY -= HEIGHT//10
        pygame.display.update()
        time.sleep(1)   
    #

    pixelmon_encountered = ""
    # Start Encounter

    pixelmon_encountered = getPixelmon(area)

    



    #




WIDTH = 800
HEIGHT = 600

SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Pixelmon")

zoom = 0
scroll = [0, 0]

collidableObjects = ["basicbush.png","basictree.png","basicfence.png","largetree.png"]
pixelAccounterObjects = ["tallgrass.png"]

curOffsetX = -300
curOffsetY = -100

desiredMoveX = 0
desiredMoveY = 0

Player = PLAYER([WIDTH//2-6, HEIGHT//2-8], 5)


running = True
while(running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    SCREEN.fill((0,0,0))

    desiredMoveX = 0
    desiredMoveY = 0
    move = True
    mightAccounter = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:    
        desiredMoveX+=Player.speed
    if keys[pygame.K_RIGHT]:    
        desiredMoveX-=Player.speed
    if keys[pygame.K_UP]:    
        desiredMoveY+=Player.speed
    if keys[pygame.K_DOWN]:    
        desiredMoveY-=Player.speed

    

    # Draw Tiles
    for t in tiles:
        ImageSource = t[2];
        PosX = int(t[0])+curOffsetX #Offset  +dif
        PosY = int(t[1])+curOffsetY #OffsetY +difY
        img = pygame.image.load(f"graphics/{ImageSource}")
        rect = img.get_rect(topleft=(PosX+desiredMoveX,PosY+desiredMoveY))
        if ImageSource in collidableObjects:
            if Player.collision(rect):
                move = False
        if ImageSource in pixelAccounterObjects:
            if Player.collision(rect):
                mightAccounter = True
        
        SCREEN.blit(img,((PosX),(PosY)))
    #
        
    Player.draw(SCREEN)

    if mightAccounter and (desiredMoveX!=0 or desiredMoveY!=0):
        steps+=1
        if calculateChance(steps):
            steps = 0
            encounter(SCREEN, area)
    else:
        steps = 0

    if move:
        curOffsetX += desiredMoveX
        curOffsetY += desiredMoveY




    pygame.display.update()

pygame.quit()
