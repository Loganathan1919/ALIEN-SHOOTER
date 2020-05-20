import pygame
import random
import math
import sys
from pygame import mixer

clock = pygame.time.Clock()
FPS = 60 
pygame.init()




screen = pygame.display.set_mode((1000,600))


background = pygame.image.load('background.png')


mixer.music.load("background.wav")
mixer.music.play(-1)

pygame.display.set_caption("First game")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)


playerimg = pygame.image.load('player.png')
playerX = 450
playerY = 480
xmove = 0

enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 12

for i in range(num_of_enemies):
    enemyimg.append(pygame.image.load('enemy.png')) 
    enemyX.append( random.randint(0,936))
    enemyY.append(random.randint(0,64))
    enemyX_change.append(12)
    enemyY_change.append(32)

bulletimg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 25
bullet_state = "ready"

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX =10
textY = 10

over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x,y):
    score = font.render("Score : " +str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (299, 250))

def player (x,y):
    screen.blit(playerimg, (x,y))

def enemy (x,y,i):
    screen.blit(enemyimg[i], (x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg,(x+16,y+4))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2)) +( math.pow(enemyY-bulletY,2) ))
    if distance < 27:
        return True
    else:
        return False


running = True
while running:

    clock.tick(FPS)

    screen.fill((0,0,0))

    screen.blit(background, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
             running = False
    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                xmove = -15
            if event.key == pygame.K_RIGHT:
                xmove = 15
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                xmove = 0
        

    playerX += xmove

    if playerX <= 0:
        playerX = 0
    elif playerX >= 1000-64:
        playerX = 1000-64

    for i in range(num_of_enemies):
        #game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break



        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 936:
            enemyX_change[i] = -5
            enemyY[i] += enemyY_change[i]

        Collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if Collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0,936)
            enemyY[i] = random.randint(0,64)

        enemy (enemyX[i],enemyY[i],i)
#bullet movement
    if bulletY <=0 :
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change
    

    
    player (playerX,playerY)
    show_score(textX,textY)
    pygame.display.update()