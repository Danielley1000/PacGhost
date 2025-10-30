import pygame
from Boards import boards
import math
pygame.init()

#By DanielleY1000


#general veriables
WID = 900
HIGH = 950
PI = math.pi

timer = pygame.time.Clock()
color = 'blue'
line = 4 
screen = pygame.display.set_mode([WID,HIGH])
fps = 60
font = pygame.font.SysFont('Heebo', 20)
#.Font
run = True
tileHigh = (HIGH-50)//30 #floor to a whole int 
tileWid = WID//30
dirCom = 0
    
#level veriables 
levelOne = boards[0]
levelTwo = boards[1]
openScreen = True

#logo images 
logoImages = []
for i in range(1,7):
    logoImages.append(pygame.transform.scale(pygame.image.load(f'logo/logo{i}.png'), (800,600))) #pick size
imageCount = 0

#player image veriables 
playerImages = []
for i in range(1,7):
    playerImages.append(pygame.transform.scale(pygame.image.load(f'playerImages/{i}.png'), (2*tileWid,2*tileHigh))) #pick size

playerRight = [img for img in playerImages]
playerLeft  = [pygame.transform.flip(img, True, False) for img in playerImages]
playerUp    = [pygame.transform.rotate(img, 90) for img in playerImages]
playerDown  = [pygame.transform.rotate(img, 270) for img in playerImages]

#player  veriables 
playerXPos = 450
playerYPos = 450
dir = 0
count = 0 
playerSpeed = 2
energy = 10000 # to allow energy to slowly deplete
moving = False
startCounter = 0

def drawStuff():
    energyText = font.render(f'Energy: {energy//100}', True, 'black')
    screen.blit(energyText, (10, 920))
    lives = energy //2500
    for i in range(lives):
        screen.blit(pygame.transform.scale(playerRight[2], (tileWid, tileHigh)), (WID - (i+1)*(tileWid +10), 920))
    
def drawLogo():
    frameSpeed = 8
    frameCount = len(logoImages)
    f = (imageCount // frameSpeed) % frameCount  

    logo = logoImages[f]
    screen.blit(logo, (50,0))

# make dots? also make and not flicker
def drawBoard(lvl):
    
    for i in range(len(lvl)): #for every row in level 
        for j in range(len(lvl[i])): # for every col of curr row 
            if lvl[i][j] == 7:
                pygame.draw.line(screen, color,[tileWid*(j+0.5), tileHigh*i],
                                 [tileWid*j + (0.5*tileWid), tileHigh*(i+1)],line)
            if lvl[i][j] == 8:
                pygame.draw.line(screen, color,[tileWid*j, tileHigh*(i + 0.5)],
                                 [tileWid*(j+1), tileHigh*(i+0.5)],line)
            if lvl[i][j] == 3:
                pygame.draw.arc(screen, color,[tileWid*(j-0.5), tileHigh*(i+0.5),
                                               tileWid, tileHigh], 0, PI/2,line)
            if lvl[i][j] == 4:
                pygame.draw.arc(screen, color,[tileWid*(j+0.5), tileHigh*(i+0.5),
                                               tileWid, tileHigh], PI/2,PI ,line)
            if lvl[i][j] == 5:
                pygame.draw.arc(screen, color,[tileWid*(j+0.5), tileHigh*(i-0.5),
                                               tileWid, tileHigh], PI, 3*PI/2,line)
            if lvl[i][j] == 6:
                pygame.draw.arc(screen, color,[tileWid*(j-0.5), tileHigh*(i-0.5),
                                               tileWid, tileHigh], 3*PI/2,2*PI ,line)
            if lvl[i][j] == 1:
                pygame.draw.circle(screen, 'white', [tileWid*j + tileWid//2, tileHigh*i + tileHigh//2], 5)
            
def drawPlayer():
    frame = count//5 
    if dir == 0:
        image = playerRight[frame]
    elif dir == 1:
        image = playerLeft[frame]
    elif dir == 2:
        image = playerUp[frame]
    elif dir == 3:
        image = playerDown[frame]
    
    rect = image.get_rect(center=(playerXPos + tileWid // 2, playerYPos + tileHigh // 2))
    screen.blit(image, rect.topleft)


    
def checkPos(centerX, centerY): # go over
    turnsAllowed = [False, False, False, False] #R, L, U, D #tileHigh, tileWid 
    num = 15 #check collision based on center x,y of player 
    time = 0 
    if centerX //tileWid<29: 
        if dir == 0: #<1 ie 0, which is the empty tile. if changing tiles, change/replace range 
            if levelOne[centerY//tileHigh][(centerX-num)//tileWid] < 3: #multipule levels? 
                turnsAllowed[1] = True #left turn allowd
        if dir == 1:
            if levelOne[centerY//tileHigh][(centerX+num)//tileWid] < 3: #multipule levels? 
                turnsAllowed[0] = True #right turn allowed 
        if dir == 2: 
            if levelOne[(centerY+num)//tileHigh][centerX//tileWid] < 3: #multipule levels? 
                turnsAllowed[3] = True #down turn allowed
        if dir == 3: 
            if levelOne[(centerY-num)//tileHigh][centerX//tileWid] < 3: #multipule levels? 
                turnsAllowed[2] = True 
                
        if dir == 2 or dir == 3: #up or down 
            if 12<= centerX % tileWid <=18:
                if levelOne[(centerY+num)//tileHigh][centerX//tileWid] <3: # multipule levels?
                    turnsAllowed[3] = True 
                if levelOne[(centerY-num)//tileHigh][centerX//tileWid] <3: # multipule levels? 
                    turnsAllowed[2] = True 
            if 12<= centerY % tileHigh <=18: 
                if levelOne[centerY//tileHigh][(centerX-tileWid)//tileWid] <3: # multipule levels? 
                    turnsAllowed[1] = True 
                if levelOne[centerY//tileHigh][(centerX+tileWid)//tileWid] <3: # multipule levels? 
                    turnsAllowed[0] = True 
                    
        if dir == 0 or dir == 1: #left or right 
            if 12<= centerX % tileWid <=18: 
                if levelOne[(centerY+tileHigh)//tileHigh][centerX//tileWid] <3: # multipule levels? 
                    turnsAllowed[3] = True 
                if levelOne[(centerY-tileHigh)//tileHigh][centerX//tileWid] <3: # multipule levels? 
                    turnsAllowed[2] = True 
            if 12<= centerY % tileHigh <=18: 
                if levelOne[centerY//tileHigh][(centerX-num)//tileWid] <3: # multipule levels? 
                    turnsAllowed[1] = True 
                if levelOne[centerY//tileHigh][(centerX+num)//tileWid] <3: # multipule levels?
                    turnsAllowed[0] = True 
    else: 
        turnsAllowed[0] = True 
        turnsAllowed[1] = True 
        
    return turnsAllowed


def checkCollision(eng):
    if 0 < playerXPos< (WID-tileWid):
        if levelOne[playerCenterY//tileHigh][playerCenterX//tileWid] == 1: #eats object on tile based on tile number
            levelOne[playerCenterY//tileHigh][playerCenterX//tileWid] = 0
            eng +=1000 #how much does energy change? 
    return eng
        
    
    

def playerMove(playX, playY): #R,L,U,D
    if dir == 0 and validTurns[0]:
        playX +=playerSpeed
    elif dir ==1 and validTurns[1]:
        playX-=playerSpeed 
    if dir == 2 and validTurns[2]:
        playY -=playerSpeed
    elif dir == 3 and validTurns[3]:
        playY+=playerSpeed    
    return playX, playY 
    
while run:
    screen.fill('pink')

    timer.tick(fps)
    
    if count<19:
        count+=1
        if count > 3:
            flicker = False #do we want dots to flicker?
    else:
        count = 0
        flicker = True #dots to flicker? 
    
    if startCounter <120:
        moving = False
        startCounter +=1
    else:
        moving = True
        
        if energy >10:
            energy -=1
    
    
    
    while openScreen:
        timer.tick(fps)
        screen.fill('pink')
        drawLogo()
        imageCount +=1
        if imageCount > 29:
            imageCount = 0
        
        start = pygame.font.SysFont('Rubik Bold', 50)
        start = start.render(f'Press SPACE to start', True, 'black')
        textRect = start.get_rect(center=(WID // 2, HIGH // 2))
        screen.blit(start, textRect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #to quit the game 
                openScreen = False
                run = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    openScreen = False
        pygame.display.flip() 
    
    
    drawBoard(levelOne) # for multipule levels? // boards[i]
    drawPlayer()
    drawStuff()
        
    playerCenterX = (playerXPos + tileWid // 2)
    playerCenterY = (playerYPos + tileHigh // 2)
    
    validTurns = checkPos(playerCenterX, playerCenterY)
    
    if moving:
        playerXPos, playerYPos = playerMove(playerXPos, playerYPos)
    energy = checkCollision(energy)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #to quit the game 
            run = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                dirCom = 3
            if event.key == pygame.K_UP: # if key is pressed, draw based on direction 
                dirCom = 2
            if event.key == pygame.K_LEFT:
                dirCom = 1
            if event.key == pygame.K_RIGHT:
                dirCom = 0 
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN and dirCom == 3:
                dirCom = dir
            if event.key == pygame.K_UP and dirCom == 2: 
                dirCom = dir
            if event.key == pygame.K_LEFT and dirCom == 1:
                dirCom = dir
            if event.key == pygame.K_RIGHT and dirCom == 0:
                dirCom = dir
    for i in range(4):
        if dirCom == i and validTurns[i]:
            dir = i
        
    
        if playerXPos>WID:
            playerXPos = -47
        elif playerXPos<-47:
            playerXPos = WID
            
        if playerYPos>HIGH:
            playerYPos = -47
        elif playerYPos<-47:
            playerYPos = HIGH
            
    #pygame.draw.circle(screen, 'red', (playerCenterX, playerCenterY), tileHigh//2, 3)  
    pygame.display.flip()
pygame.quit()

