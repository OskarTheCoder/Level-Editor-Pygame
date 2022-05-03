import pygame
from pygame.locals import *;
from pygame import mixer;
import os;

# More levels = less Data


pygame.init()



WIDTH = 1200
HEIGHT = 800
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Level Editor")

clock = pygame.time.Clock()

# // COORDINATIVE LOGIC
WORLDCENTERPOS=[WIDTH//2,HEIGHT//2]
dif = 0
difY= 0
# // COORDINATIVE LOGIC END

def drawgrid(d,dY, screen):
    gridSize = 32

    movedX = d
    movedY = dY

    #movedX-=gridSize

    #movedY-=gridSize

    mD = movedX//32
    movedX -= 32 *mD

    mDy = movedY//32
    movedY -= 32 *mDy


    for n in range(-1, WIDTH//gridSize + 1):
        pygame.draw.line(screen, ((201,200,199)), (n*gridSize + movedX, 0), (n*gridSize + movedX, HEIGHT))
    
    for m in range(-1, HEIGHT//gridSize + 1):
        pygame.draw.line(screen, ((199,200,201)), (0, m*gridSize + movedY), (WIDTH, m*gridSize + movedY))



mainFont = pygame.font.Font('fonts/pixel.ttf', 16)
cordinates = "x 0  y 0" 
label = mainFont.render(cordinates, False, ((244,244,235)))


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

tilezToRemove = []
for r in range(1,len(tiles)):
    if tiles[r] == tiles[r-1]:
        tilezToRemove.append(tiles[r-1])
    
for g in tilezToRemove:
    tiles.remove(g)

show = True


MENUMAXX = WIDTH//2-WIDTH//3;

curSelectedTile = None

running = True

while(running):
    SCREEN.fill((0,0,0))
    mp = pygame.mouse.get_pos()
    mousePos = [mp[0]-dif, mp[1]-difY]
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g or event.key == pygame.K_t:
                show = not show
            if event.key == pygame.K_q and len(tiles) > 0:
                tiles.remove(tiles[-1])

        if event.type == pygame.QUIT:

            save = ""
            for t in tiles:
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
            
            if (mp[0] > MENUMAXX):
                if event.button == 3:
                    tilesToRemove = []
                    for i in range(len(tiles)):
                        m = pygame.image.load("graphics/"+tiles[i][2])
                        recx = m.get_rect(topleft=(int(tiles[i][0]),int(tiles[i][1])))
                        if pygame.rect.Rect.collidepoint(recx,mousePos[0],mousePos[1]):
                            tilesToRemove.append(tiles[i])
                    for til in tilesToRemove:
                        tiles.remove(til)
                elif (curSelectedTile != None):
                    if show:
                        mousePos[0] = mousePos[0] // 32
                        mousePos[0] = mousePos[0] * 32
                        mousePos[1] = mousePos[1] // 32
                        mousePos[1] = mousePos[1] * 32
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
                    if pygame.rect.Rect.collidepoint(recx,mp[0],mp[1]):
                        curSelectedTile = imagesInCurDir[i]

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        WORLDCENTERPOS[0]+=5
        dif -= 5
    if keys[pygame.K_LEFT]:
        WORLDCENTERPOS[0]-=5
        dif += 5
    if keys[pygame.K_UP]:
        WORLDCENTERPOS[1]-=5
        difY += 5
    if keys[pygame.K_DOWN]:
        WORLDCENTERPOS[1]+=5
        difY -= 5


    # Draw Tiles
    for t in tiles:
        ImageSource = t[2];
        PosX = int(t[0])+dif
        PosY = int(t[1])+difY
        img = pygame.image.load(f"graphics/{ImageSource}")
        SCREEN.blit(img,((PosX),(PosY)))
    #

    if show:
        drawgrid(dif,difY,SCREEN)

    pygame.draw.rect(SCREEN, ((106,105,104)), (0,0,MENUMAXX,HEIGHT))

    y = 100
    for content in imagesInCurDir:
        SCREEN.blit(pygame.image.load(f"graphics/{content}"),(0,y))
        y+=pygame.image.load(f"graphics/{content}").get_width()
        y+=30

    label = mainFont.render(f"x {mousePos[0]-dif}  y {mousePos[1]-difY}",True,((244,244,235)))
    SCREEN.blit(label, (0,0))




    pygame.display.update()
    clock.tick(30)


pygame.quit()
