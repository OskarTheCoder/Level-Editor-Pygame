import pygame
from pygame.locals import *;


# Load Tiles
tiles = []
actualTile = []
i = 1
tile = ""
start=False
TheContentIs = ""
with open("graphics/data.txt","r") as file:
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

WIDTH = 1200
HEIGHT = 800

SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("PixelMon")


running = True
while(running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    # Draw Tiles
    for t in tiles:
        ImageSource = t[2];
        PosX = int(t[0]) #Offset  +dif
        PosY = int(t[1]) #OffsetY +difY
        img = pygame.image.load(f"graphics/{ImageSource}")
        SCREEN.blit(img,((PosX),(PosY)))
    #

    pygame.display.update()

pygame.quit()