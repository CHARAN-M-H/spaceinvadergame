import pygame
import random
import math
from pygame import mixer

pygame.init()  # initializing game
screen = pygame.display.set_mode((800, 600))  # screen

#bg
#background = pygame.image.load('background.png')


pygame.display.set_caption("charan's game")  # title of the window

# bg sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# spaceship(player)
playerimg = pygame.image.load('spaceship.png')
playerx = 370
playery = 480
playerx_change = 0

# enemy
enemyimg = pygame.image.load('alien.png')
enemyx = random.randint(0, 735)
enemyy = random.randint(50, 150)
enemyx_change = 0.3
enemyy_change = 20

# missile
missleimg = pygame.image.load('bullet.png')
missilex = 0
missiley = 480
missilex_change = 0
missiley_change = 0.5
missile_state = "ready"

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textx = 10
texty = 10


def show_score(x, y):
    score = font.render("SCORE: " + str(score_value), True, (255, 0, 0))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerimg, (x, y))


def enemy(x, y):
    screen.blit(enemyimg, (x, y))


def fire_bullet(x, y):
    global missile_state
    missile_state = "fire"
    screen.blit(missleimg, (x + 16, y + 10))


def iscollision(enemyx, enemyy, missilex, missiley):
    distance = math.sqrt((math.pow(enemyx - missilex, 2)) + (math.pow(enemyy - missiley, 2)))
    if distance < 27:
        return True
    else:
        return False


# game looping
running = True
while running:
    screen.fill((0, 0, 0))  # (r,g,b)
    #screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                playerx_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerx_change = 0.3
            if event.key == pygame.K_SPACE:
                if missile_state is "ready":
                    missile_sound = mixer.Sound('laser.wav')
                    missile_sound.play()
                    missilex = playerx
                    fire_bullet(missilex, missiley)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change = 0

    playerx += playerx_change  # boundary limits
    if playerx <= 0:
        playerx = 0
    elif playerx >= 736:
        playerx = 736

    enemyx += enemyx_change  # enemy movement
    if enemyx <= 0:
        enemyx_change = 0.3
        enemyy += enemyy_change
    elif enemyx >= 736:
        enemyx_change = -0.3
        enemyy += enemyy_change

    # missile movement
    if missiley <= 0:
        missiley = 480
        missile_state = "ready"

    if missile_state is "fire":
        fire_bullet(missilex, missiley)
        missiley -= missiley_change

    # collision
    collison = iscollision(enemyx, enemyy, missilex, missiley)
    if collison:
        explosion_sound = mixer.Sound('explosion.wav')
        explosion_sound.play()
        missiley = 480
        missile_state = "ready"
        score_value += 1
        enemyx = random.randint(0, 735)
        enemyy = random.randint(50, 150)

    player(playerx, playery)  # player function is called
    show_score(textx, texty)
    enemy(enemyx, enemyy)
    pygame.display.update()  # updating the game window for every action
