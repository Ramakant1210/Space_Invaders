import pygame as py
import random
import math
from pygame import mixer

# initialize pygame
py.init()
# create screen
screen = py.display.set_mode((800, 600))
background = py.image.load('background.jpg')

#
mixer.music.load('gameMusic.wav')
mixer.music.play(-1)

#variable for result
score = 0
font = py.font.Font('freesansbold.ttf',32)

textX = 10
textY = 10

def show_score(x,y):
    score_value = font.render("Score: "+ str(score),True,(255,255,255))
    screen.blit(score_value,(x,y))

# Load images
icon = py.image.load('spaceship.png')
player = py.image.load('jet.png')
bullet = py.image.load('bullet.png')

# caption and icon for screen
py.display.set_caption("Jet Fighter")
py.display.set_icon(icon)
# Player Co-ordinate
playerX = 370
playerY = 480

playerX_change = 0
playerY_change = 0

# Alien co_ordinate
alien=[]
alienX = []
alienY = []
alienX_change =[]
alienY_change = []
number_of_aliens = 6

for i in range(number_of_aliens):
    alien.append(py.image.load('alien.png'))
    alienX.append(random.randint(0, 736))
    alienY.append(random.randint(30, 150))
    alienX_change.append(4)
    alienY_change.append(40)

# Bullet co_ordinates
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = 'ready'


def Alien(x, y,i):
    screen.blit(alien[i], (x, y))


def Player(x, y):
    screen.blit(player, (x, y))


def Bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bullet, (x + 16, y + 10))

#checking coliision
def isCollision(alienX,alienY,bulletX,bulletY):
    distance = math.sqrt(math.pow(alienX-bulletX,2)+(math.pow(alienY-bulletY,2)))
    if distance<35:
        return True
    else:
        return False

running = True
while running:
    screen.fill((0, 240, 130))
    screen.blit(background, (0, 0))
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False

        # checking keyboard event
        if event.type == py.KEYDOWN:
            if event.key == py.K_LEFT:
                # print("Left Arrow Pressed")
                playerX_change = -5
            if event.key == py.K_RIGHT:
                # print("Right Arrow Pressed")
                playerX_change = 5
            if event.key == py.K_SPACE:
                if bullet_state == 'ready':
                    #bullet_sound = mixer.Sound('gunshot.wav')
                    #bullet_sound.play()
                    bulletX = playerX
                    Bullet(playerX, bulletY)
            '''if event.key == py.K_UP:
                playerY_change = -0.3
            if event.key == py.K_DOWN:
                playerY_change = 0.3'''
        if event.type == py.KEYUP:
            if event.key == py.K_LEFT or event.key == py.K_RIGHT:
                # print("Key has been released")
                playerX_change = 0

            # if event.key == py.K_UP or event.key == py.K_DOWN:
            # playerY_change = 0

    # For multiple bullet firing
    if bulletY < 0:
        bulletY = 480
        bullet_state = 'ready'

    # Bullet state for fired bullet
    if bullet_state is 'fire':
        Bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    for i in range(number_of_aliens):
        # bullet and alien collision
        collision = isCollision(alienX[i],alienY[i],bulletX,bulletY)
        if collision:
            crash_sound = mixer.Sound('collision.wav')
            crash_sound.play()
            bulletY = 480
            bullet_state = 'ready'
            score += 1
            alienX[i] = random.randint(0,736)
            alienY[i] = random.randint(30,150)

        alienX[i] += alienX_change[i]

        if alienX[i] > 736 or alienX[i] < 0:
            alienX_change[i] = -1 * alienX_change[i]
            alienY[i] += alienY_change[i]

        Alien(alienX[i], alienY[i],i)

    playerX += playerX_change
    # playerY += playerY_change

    if playerX < 0:
        playerX = 0
    elif playerX > 736:
        playerX = 736



    Player(playerX, playerY)
    show_score(textX,textY)

    py.display.update()

