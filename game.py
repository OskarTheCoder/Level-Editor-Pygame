import pygame
from pygame.locals import *;
from pygame import mixer;
import random
import time
from pixelmondata import *;
from moves import *;

pygame.init()
pygame.mixer.init()

clock = pygame.time.Clock()

mainFont = pygame.font.Font("fonts/pixel.ttf",32)

# Testing Scene == "data"
area = "data"

victoryMusic = pygame.mixer.music.load("music/110 Wild Pokemon Defeated!.wav")


# LOAD TEAM

playerteam = []
curPixelMon = []
curStat = ""
i = 0
start = False
with open("team.txt", "r") as team:
    for line in team:
        for char in line:
            if not start:
                if char == "#":
                    start = True
            else:
                if char == "#":
                    start = False
                    curPixelMon.append(curStat)
                    curStat = ""
                    i+=1
                    if  i > 9:
                        playerteam.append(curPixelMon)
                        curPixelMon = []
                        i = 0
                else:
                    curStat += char
PlayerTeam = []
for t in range(len(playerteam)):
    PlayerTeam.append([])
    PlayerTeam[-1].append(PIXELMON(playerteam[t][0], [int(playerteam[t][1]),int(playerteam[t][2]),int(playerteam[t][3]),int(playerteam[t][4]),int(playerteam[t][5]), int(playerteam[t][6]), int(playerteam[t][9])], int(playerteam[t][7]),int(playerteam[t][8])))
    PlayerTeam[-1][-1].moves.append(MOVE("Psybeam", 9, "psychic"))

class PLAYER():
    def __init__(self, pos, speed):
        self.down = [pygame.transform.scale(pygame.image.load("player/player_down_1.png"), (24,34) ),pygame.transform.scale(pygame.image.load("player/player_down_2.png"), (24,34) ),pygame.transform.scale(pygame.image.load("player/player_down_3.png"), (24,34) ),pygame.transform.scale(pygame.image.load("player/player_down_4.png"), (24,34) )]
        self.up = [pygame.transform.scale(pygame.image.load("player/player_up_1.png"), (24,34) ),pygame.transform.scale(pygame.image.load("player/player_up_2.png"), (24,34) ),pygame.transform.scale(pygame.image.load("player/player_up_3.png"), (24,34) ),pygame.transform.scale(pygame.image.load("player/player_up_4.png"), (24,34) )]
        self.right = [pygame.transform.scale(pygame.image.load("player/player_right_1.png"), (24,34) ),pygame.transform.scale(pygame.image.load("player/player_right_2.png"), (24,34) ),pygame.transform.scale(pygame.image.load("player/player_right_3.png"), (24,34) ),pygame.transform.scale(pygame.image.load("player/player_right_4.png"), (24,34) )]
        self.left = [pygame.transform.scale(pygame.image.load("player/player_left_1.png"), (24,34) ),pygame.transform.scale(pygame.image.load("player/player_left_2.png"), (24,34) ),pygame.transform.scale(pygame.image.load("player/player_left_3.png"), (24,34) ),pygame.transform.scale(pygame.image.load("player/player_left_4.png"), (24,34) )]
        self.img = self.down[0]
        self.pos = pos
        self.dir = 0
        self.speed = speed
        self.tick = 0

    def draw(self, screen):
        screen.blit(self.img, self.pos)

    def move(self):
        self.tick+=4
        if self.tick < 25:
            if self.dir == 0:
                self.img = self.down[0]
            elif self.dir == 1:
                self.img = self.up[0]
            elif self.dir == 2:
                self.img = self.right[0]
            elif self.dir == 3:
                self.img = self.left[0]
        elif self.tick < 50:
            if self.dir == 0:
                self.img = self.down[1]
            elif self.dir == 1:
                self.img = self.up[1]
            elif self.dir == 2:
                self.img = self.right[1]
            elif self.dir == 3:
                self.img = self.left[1]
        elif self.tick < 75:
            if self.dir == 0:
                self.img = self.down[2]
            elif self.dir == 1:
                self.img = self.up[2]
            elif self.dir == 2:
                self.img = self.right[2]
            elif self.dir == 3:
                self.img = self.left[2]
        elif self.tick < 100:
            if self.dir == 0:
                self.img = self.down[3]
            elif self.dir == 1:
                self.img = self.up[3]
            elif self.dir == 2:
                self.img = self.right[3]
            elif self.dir == 3:
                self.img = self.left[3]
        else:
            self.tick = 0



    def collision(self, other):
        return pygame.rect.Rect.colliderect(self.img.get_rect(topleft=(self.pos[0],self.pos[1])), other)
    
def hasAtLeastOnePokemonLeft(list):
    print(list)
    for m in range(len(list)):
        if list[m][0].curhealth > 0:
            return True
    print("False")
    return False

def getNextPokemon(list):
    for m in range(len(PlayerTeam)):
        if list[m][0].curhealth > 0:
            return list[m][0]


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


steps = 0

playingMusic = False
def getMusic(area):
    if area == "data":
        return "105 Littleroot Town"

def getPixelmon(area):
    if area == "data":
        return random.choice(listOfPixelmons)[0]

def calculateChance(steps):
    chance = 1 + (steps*2)//5
    num = random.randint(1,1000)
    if num <= chance:
        return True
    else:
        return False

def waitUntilMouseClicked():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                return
        

def encounter(SCREEN, area):
     

    xx = 0
    xX = WIDTH-WIDTH//10

    yy = 0
    yY = HEIGHT-HEIGHT//10

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
        time.sleep(0.5)
    

    pixelmon_encountered = getPixelmon(area)
    mon = PIXELMON(pixelmon_encountered,baseStats[pixelmon_encountered], random.choice(baseLevels[pixelmon_encountered]),0)

    PlayerCurrentMon = PlayerTeam[0][0]
    if PlayerCurrentMon.curhealth <= 0:
        if hasAtLeastOnePokemonLeft(PlayerTeam):                                    
            PlayerCurrentMon = getNextPokemon(PlayerTeam)
            player_hp = PlayerCurrentMon.curhealth
            player_hp_label = mainFont.render("HP: "+str(player_hp),True,((0,0,0)))
            player_hp_label_pos = (WIDTH//5,HEIGHT-HEIGHT//3-200)
        else:
            return 0

    hp = mon.curhealth
    hp_label = mainFont.render("HP: "+str(hp),True,((0,0,0)))
    hp_label_pos = (WIDTH-WIDTH//3,HEIGHT//8)

    enemy_name_label = mainFont.render(str(mon.pixelmon_name)+" Lvl "+str(mon.level),True,((0,0,0)))
    enemy_name_label_pos = (WIDTH-WIDTH//3,HEIGHT//8-60)

    player_hp = PlayerCurrentMon.curhealth
    player_hp_label = mainFont.render("HP: "+str(player_hp),True,((0,0,0)))
    player_hp_label_pos = (WIDTH//5,HEIGHT-HEIGHT//3-200)

    player_name = PlayerCurrentMon.pixelmon_name
    player_name_label = mainFont.render(str(player_name)+" Lvl "+str(PlayerCurrentMon.level),True,((0,0,0)))
    player_name_label_pos = (WIDTH//5,HEIGHT-HEIGHT//3-60-200)


    attackbuttonwidth = WIDTH//4
    attackbuttonrect = (WIDTH-attackbuttonwidth*1.5,HEIGHT-HEIGHT//6-200,attackbuttonwidth,HEIGHT//7)
    attackbuttonlabel = mainFont.render("attack", True, ((0,0,0)))

    curMove = PlayerCurrentMon.moves[0]

    actionText = "you encountered " + mon.pixelmon_name + "!"
    action_label = mainFont.render(actionText,True,((255,255,255)))
    action_label_pos = (WIDTH//2-action_label.get_width()//2,HEIGHT-90)

    turn = ""
    if PlayerCurrentMon.speed >= mon.speed:
        turn = "player"
    else:
        turn = "enemy"

    wait = False
    victory = False
    
    def updateCanvas():
        SCREEN.fill((116,200,87))
        SCREEN.blit(mon.img, (WIDTH-WIDTH//4,HEIGHT//5))
        SCREEN.blit(PlayerCurrentMon.imgback, (WIDTH//4,HEIGHT-HEIGHT//5-200))
        SCREEN.blit(hp_label, hp_label_pos)
        SCREEN.blit(player_hp_label, player_hp_label_pos)
        pygame.draw.rect(SCREEN, ((203,10,0)), attackbuttonrect)
        SCREEN.blit(attackbuttonlabel, (attackbuttonrect[0]+32,attackbuttonrect[1]+32))    
        SCREEN.blit(player_name_label, player_name_label_pos)
        SCREEN.blit(enemy_name_label, enemy_name_label_pos)
        pygame.draw.rect(SCREEN, ((123,123,123)), (0,HEIGHT-150,WIDTH,150))
        SCREEN.blit(action_label,action_label_pos)
        pygame.display.update()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -1
            if event.type == pygame.MOUSEBUTTONDOWN:
                if victory:
                    pygame.mixer.music.stop()
                    return 0
                mousePos = pygame.mouse.get_pos()
                if not victory and not wait and pygame.rect.Rect.collidepoint(pygame.rect.Rect(attackbuttonrect[0],attackbuttonrect[1],attackbuttonrect[2],attackbuttonrect[3]), mousePos[0], mousePos[1]):
                    if turn == "player":
                        mon.curhealth-=curMove.pow
                        action_label = mainFont.render("the wild " + mon.pixelmon_name + " took " + str(curMove.pow) + " damage!", True, ((255,255,255)))
                        action_label_pos = (WIDTH//2-action_label.get_width()//2,HEIGHT-90)
                        if mon.curhealth < 0:
                            mon.curhealth = 0
                        hp = mon.curhealth
                        hp_label = mainFont.render("HP: "+str(hp),True,((0,0,0)))
                        updateCanvas()
                        waitUntilMouseClicked()
                        if mon.curhealth <= 0:
                            pygame.mixer.music.load("music/110 Wild Pokemon Defeated!.wav")
                            pygame.mixer.music.play()
                            victory = True
                        if not victory:
                            PlayerCurrentMon.curhealth -= curMove.pow
                            action_label = mainFont.render(PlayerCurrentMon.pixelmon_name + " took " + str(curMove.pow) + " damage!", True, ((255,255,255)))
                            action_label_pos = (WIDTH//2-action_label.get_width()//2,HEIGHT-90)
                            player_hp = PlayerCurrentMon.curhealth
                            player_hp_label = mainFont.render("HP: "+str(player_hp),True,((0,0,0)))
                            updateCanvas()
                            waitUntilMouseClicked()
                            if PlayerCurrentMon.curhealth <= 0:
                                if hasAtLeastOnePokemonLeft(PlayerTeam):                                    
                                    PlayerCurrentMon = getNextPokemon(PlayerTeam)
                                    player_hp = PlayerCurrentMon.curhealth
                                    player_hp_label = mainFont.render("HP: "+str(player_hp),True,((0,0,0)))
                    else:
                        PlayerCurrentMon.curhealth -= curMove.pow
                        player_hp = PlayerCurrentMon.curhealth
                        player_hp_label = mainFont.render("HP: "+str(player_hp),True,((0,0,0)))
                        action_label = mainFont.render(PlayerCurrentMon.pixelmon_name + " took " + str(curMove.pow) + " damage!", True, ((255,255,255)))
                        action_label_pos = (WIDTH//2-action_label.get_width()//2,HEIGHT-90)
                        updateCanvas()
                        waitUntilMouseClicked()
                        if PlayerCurrentMon.curhealth <= 0:
                            if hasAtLeastOnePokemonLeft(PlayerTeam):
                                PlayerCurrentMon = getNextPokemon(PlayerTeam)
                                player_hp = PlayerCurrentMon.curhealth
                                player_hp_label = mainFont.render("HP: "+str(player_hp),True,((0,0,0)))
                        mon.curhealth-= curMove.pow
                        hp = mon.curhealth
                        hp_label = mainFont.render("HP: "+str(hp),True,((0,0,0)))
                        action_label = mainFont.render("the wild " + mon.pixelmon_name + " took " + str(curMove.pow) + " damage!", True, ((255,255,255)))
                        action_label_pos = (WIDTH//2-action_label.get_width()//2,HEIGHT-90)
                        if mon.curhealth < 0:
                            mon.curhealth = 0
                        updateCanvas()
                        waitUntilMouseClicked()
                        if mon.curhealth <= 0:
                            pygame.mixer.music.load("music/110 Wild Pokemon Defeated!.wav")
                            pygame.mixer.music.play()
                            victory = True


        updateCanvas()

    return 0



WIDTH = 800
HEIGHT = 600

SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Pixelmon")

zoom = 0
scroll = [0, 0]

collidableObjects = ["basicbush.png","basictree.png","basicfence.png","largetree.png"]
pixelEncounterObjects = ["tallgrass.png"]

curOffsetX = -300
curOffsetY = -60

desiredMoveX = 0
desiredMoveY = 0

Player = PLAYER([WIDTH//2-6, HEIGHT//2-8], 4)



running = True
while(running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    SCREEN.fill((116,200,87))
    if not playingMusic:
        music = pygame.mixer.music.load(f"music/{getMusic(area)}.wav")
        pygame.mixer.music.play(-1)
        playingMusic = True

    desiredMoveX = 0
    desiredMoveY = 0
    move = True
    mightAccounter = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:    
        desiredMoveX+=Player.speed
        Player.dir = 3
    if keys[pygame.K_RIGHT]:    
        desiredMoveX-=Player.speed
        Player.dir = 2
    if keys[pygame.K_UP]:    
        desiredMoveY+=Player.speed
        Player.dir = 1
    if keys[pygame.K_DOWN]:    
        desiredMoveY-=Player.speed
        Player.dir = 0

    

    # Draw Tiles
    for t in tiles:
        ImageSource = t[2];
        PosX = int(t[0])+curOffsetX 
        PosY = int(t[1])+curOffsetY
        img = pygame.image.load(f"graphics/{ImageSource}")
        rect = img.get_rect(topleft=(PosX+desiredMoveX,PosY+desiredMoveY))
        if ImageSource in collidableObjects:
            if Player.collision(rect):
                move = False
        if ImageSource in pixelEncounterObjects:
            if Player.collision(rect):
                mightAccounter = True
        
        SCREEN.blit(img,((PosX),(PosY)))
    
        
    Player.draw(SCREEN)

    if mightAccounter and (desiredMoveX!=0 or desiredMoveY!=0):
        steps+=1
        if calculateChance(steps):
            steps = 0
            pygame.mixer.music.stop()
            music = pygame.mixer.music.load("music/109 Battle! Wild Pokemon.wav")
            pygame.mixer.music.play()
            if encounter(SCREEN, area) == -1:
                running = False
            pygame.mixer.music.stop()
            music = pygame.mixer.music.load(f"music/{getMusic(area)}.wav")
            pygame.mixer.music.play(-1)
    else:
        steps = 0

    if desiredMoveX == 0 and desiredMoveY == 0:
        if Player.dir == 0:
            Player.img = Player.down[0]
        elif Player.dir == 1:
            Player.img = Player.up[0]
        elif Player.dir == 2:
            Player.img = Player.right[0]
        elif Player.dir == 3:
            Player.img = Player.left[0]
        Player.dir = -1

    if move:
        curOffsetX += desiredMoveX
        curOffsetY += desiredMoveY
        if desiredMoveX != 0 or desiredMoveY != 0:
            Player.move()
    else:
        if Player.dir == 0:
            Player.img = Player.down[0]
        elif Player.dir == 1:
            Player.img = Player.up[0]
        elif Player.dir == 2:
            Player.img = Player.right[0]
        elif Player.dir == 3:
            Player.img = Player.left[0]
        Player.dir = -1




    pygame.display.update()
    clock.tick(40)

print(PlayerTeam)
with open("team.txt","w") as teamFile:
    
    for m in range(len(PlayerTeam)):

        teamFile.write("#")
        teamFile.write(PlayerTeam[m][0].pixelmon_name)
        teamFile.write("#")

        teamFile.write("#")
        teamFile.write(str(PlayerTeam[m][0].curhealth))
        teamFile.write("#")

        teamFile.write("#")
        teamFile.write(str(PlayerTeam[m][0].attack))
        teamFile.write("#")

        teamFile.write("#")
        teamFile.write(str(PlayerTeam[m][0].defence))
        teamFile.write("#")

        teamFile.write("#")
        teamFile.write(str(PlayerTeam[m][0].spec_attack))
        teamFile.write("#")

        teamFile.write("#")
        teamFile.write(str(PlayerTeam[m][0].spec_defence))
        teamFile.write("#")

        teamFile.write("#")
        teamFile.write(str(PlayerTeam[m][0].speed))
        teamFile.write("#")
#abra##25##20##15##105##55##90##15##0#
        teamFile.write("#")
        teamFile.write(str(PlayerTeam[m][0].level))
        teamFile.write("#")

        teamFile.write("#")
        teamFile.write(str(PlayerTeam[m][0].exp))
        teamFile.write("#")

        teamFile.write("#")
        teamFile.write(str(PlayerTeam[m][0].maxhealth))
        teamFile.write("#")


pygame.quit()
