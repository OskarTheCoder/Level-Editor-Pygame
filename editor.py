from mechanize import ScalarControl
import pygame
from pygame.locals import *;
import os;


pygame.init()

WIDTH = 1200
HEIGHT = 800
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Level Editor")

imagesInCurDir = os.listdir(os.curdir+"/graphics")
possesInCurDir = []
# Ignore Pls Bad Code
for inn in imagesInCurDir:
    if (inn.find(".") == -1):
        imagesInCurDir.remove(inn)
    else:
        if (inn.split(".")[1] == "png"):
            pass
        else:
            imagesInCurDir.remove(inn)
for innn in imagesInCurDir:
    found = False
    for innnn in innn:
        if innnn == ".":
            found = True
    if (found) == False:
        imagesInCurDir.remove(innn)
wi = 100
for ni in imagesInCurDir:
    rect = pygame.image.load("graphics/"+ni).get_rect(topleft=(0,wi))
    possesInCurDir.append(rect)
    wi+=rect.w
    wi+=30
# Don't Say I didn't Warn YOU!!!

curYLogic = 100
y = 100

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


MENUMAXX = WIDTH//2-WIDTH//3;

curSelectedTile = None

running = True

while(running):
    SCREEN.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:

            save = ""
            for t in tiles:
                for i in range(2):
                    save+="#"
                    save+=f"{t[0]}"
                    save+="#"

                    save+="#"
                    save+=f"{t[1]}"
                    save+="#"

                    save+="#"
                    save+=f"{t[2]}"
                    save+="#"
            
            with open("graphics/data.txt", "w") as File:
                File.write(save)
                    
            
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            mousePos = pygame.mouse.get_pos();
            if (mousePos[0] > MENUMAXX):
                if event.button == 3:
                    for i in range(len(tiles)):
                        m = pygame.image.load("graphics/"+tiles[i][2])
                        recx = m.get_rect(topleft=(int(tiles[i][0]),int(tiles[i][1])))
                        if pygame.rect.Rect.collidepoint(recx,mousePos[0],mousePos[1]):
                            tiles.remove(tiles[i])
                            print("Collision")
                            break
                elif (curSelectedTile != None):
                    print("Place Tile In Editor Graphic Space!")
                    with open("graphics/data.txt", "w") as dataFile:
                        dataFile.write(TheContentIs)
                        dataFile.write("#")
                        dataFile.write(f"{mousePos[0]}")
                        dataFile.write("#")
                        dataFile.write("#")
                        dataFile.write(f"{mousePos[1]}")
                        dataFile.write("#")
                        dataFile.write("#")
                        dataFile.write(f"{curSelectedTile}")
                        dataFile.write("#")
                    
                    tiles.append([mousePos[0],mousePos[1],curSelectedTile])

                    with open("graphics/data.txt", "r") as dataFile:
                        for line in dataFile:
                            TheContentIs = line
                        

            else:
                for i in range(len(imagesInCurDir)):
                    recx = possesInCurDir[i]
                    if pygame.rect.Rect.collidepoint(recx,mousePos[0],mousePos[1]):
                        curSelectedTile = imagesInCurDir[i]


    # Draw Tiles

    for t in tiles:
        ImageSource = t[2];
        PosX = t[0]
        PosY = t[1]


        img = pygame.image.load(f"graphics/{ImageSource}")
        SCREEN.blit(img,(int(PosX),int(PosY)))

    #

    pygame.draw.rect(SCREEN, ((106,105,104)), (0,0,MENUMAXX,HEIGHT))

    y = 100
    for content in imagesInCurDir:
        SCREEN.blit(pygame.image.load(f"graphics/{content}"),(0,y))
        y+=pygame.image.load(f"graphics/{content}").get_width()
        y+=30



    pygame.display.update()


pygame.quit()