#############################################
#             DrMario_CLASSES_Final.py            #
#           Dr. Mario MAIN PROGRAM          #
#                 Sharisse Ji               #
#              January 12, 2023             #
#############################################

from DrMario_CLASSES_Final import *
from math import sqrt
import pygame
import time
pygame.init()

# LOAD GAME SCREEN
# width: height = 32:28
WIDTH = 800
HEIGHT = 700
GRIDSIZE = HEIGHT//28  # side length of one square = 25
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# -----------------------------------#
#           SETUP VARIABLES          #
# -----------------------------------#

# MUSIC AND SOUND EFFECTS----------------------#
# will be added in replit version

# FONTS----------------------------------------#
font = pygame.font.Font("Minecraft.otf", 40)

# IMAGES-------------------------------------------------
introBG = pygame.image.load("DrMario_introscreen.png")
introBG = pygame.transform.scale(introBG, (WIDTH,HEIGHT))
gameBG = pygame.image.load("DrMario_gamescreen.png")
gameBG = pygame.transform.scale(gameBG, (WIDTH, HEIGHT))
endBG = pygame.image.load("DrMario_endscreen.png")
endBG = pygame.transform.scale(endBG, (WIDTH, HEIGHT))
controlBG = pygame.image.load("DrMario_controlscreen.png")
controlBG = pygame.transform.scale(controlBG, (WIDTH, HEIGHT))

pauseMenu = pygame.image.load("DrMario_pausescreen.png")
pauseMenu = pygame.transform.scale(pauseMenu, (WIDTH, HEIGHT))

# BUTTONS---------------------------------------#
playButton = pygame.Rect(325, 495, 175, 55)  # rectangular button area to detect clicks (not drawn)
controlButton = pygame.Rect(245, 560, 335, 55)
control_returnButton = pygame.Rect(270, 530,250,55)

pauseResumeButton = pygame.Rect(275, 360, 290, 60)
pauseRestartButton = pygame.Rect(260, 470, 320, 60)

restartButton = pygame.Rect(325,575,155,45)

# GAME SCREEN DIMENSIONS------------------------#
COLUMNS = 8
ROWS = 16
LEFT = 12
RIGHT = LEFT + COLUMNS
MIDDLE = LEFT + COLUMNS//2
TOP = 9
FLOOR = TOP + ROWS

# COLOURS --------------------------------------#
DARKGREY = (150,150,150)


# -----------------------------------#
#           GAME VARIABLES           #
# -----------------------------------#
# GAME SCREENS----------------------------------#
Play = True
state = 1
pause = False

# SCORING---------------------------------------#
timer = 0
score = 0
highscore = 0
speed = 8
level = 0

# GAME VARIABLES------------------------------#
floor = Bottom(LEFT, FLOOR, COLUMNS)
leftWall = Wall(LEFT-1, TOP, ROWS)
rightWall = Wall(RIGHT, TOP, ROWS)
ceiling = Bottom(LEFT+3, TOP, 2)

obstacle = Obstacles(LEFT, FLOOR)
numViruses = 4
virusesRemoved = 0
viruses = Viruses(LEFT+1, RIGHT-1, TOP+8, FLOOR-1, numViruses)
obstacle.append(viruses)


# -----------------------------------#
#           FUNCTIONS                #
# -----------------------------------#

def drawGrid():  # draws faint gray lines in play screen
    for x in range(0, WIDTH, GRIDSIZE):    # draw vertical
        pygame.draw.line(screen, DARKGREY, (x, 0), (x, HEIGHT))

    for y in range(0, HEIGHT, GRIDSIZE):     # draw horizontal
        pygame.draw.line(screen, DARKGREY, (0, y), (WIDTH, y))


# DRAW SCREEN 1
def introScreen():
    screen.blit(introBG, (0, 0))
    pygame.display.update()


# DRAW SCREEN 2
def controlScreen():
    screen.blit(controlBG, (0,0))
    pygame.display.update()


# DRAW SCREEN 3
def redrawScreen():
    # testing pill
    if pause is True:
        pauseScreen()
    else:
        screen.fill((0,0,0))
        drawGrid()
        screen.blit(gameBG, (0,0))

        printScore = font.render(str(highscore), True, BLACK)
        screen.blit(printScore, (100, 167))

        printScore = font.render(str(score), True, BLACK)
        screen.blit(printScore, (100, 247))

        printLevel = font.render(str(level), True, BLACK)
        screen.blit(printLevel, (620, 450))

        printSpeed = font.render(str(speed), True, BLACK)
        screen.blit(printSpeed, (620, 520))

        printVirus = font.render(str(numViruses), True, BLACK)
        screen.blit(printVirus, (620, 600))

        newPill.draw(screen, GRIDSIZE)
        obstacle.draw(screen, GRIDSIZE)

        pygame.display.update()


# DRAW SCREEN 4
def endScreen():
    screen.blit(endBG, (0, 0))
    pygame.display.update()


# DRAW PAUSE SCREEN
def pauseScreen():
    screen.fill((0,0,0))
    screen.blit(pauseMenu, (20, 20))
    pygame.display.update()


def distance(x1, y1, x2, y2):  # used for buttons

    return sqrt((x1 - x2)**2 + (y1 - y2)**2)

# -----------------------------------#
#           GAME PLAY                #
# -----------------------------------#
while Play:
    # SCREEN 1: INTRO SCREEN-----------------------------#
    if state == 1:
        pause = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Play = False
            (cursorX, cursorY) = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:                        # if play is clicked, reset everything
                if playButton.collidepoint(cursorX, cursorY) is True:
                    obstacle = Obstacles(LEFT, FLOOR)
                    level += 1
                    speed += 2

                    numViruses = numViruses+1
                    virusesRemoved = 0
                    viruses = Viruses(LEFT+1, RIGHT-1, TOP+8, FLOOR-1, numViruses)
                    obstacle.append(viruses)

                    if highscore <= score:
                        highscore = score
                    state = 3

                if controlButton.collidepoint(cursorX, cursorY) is True:
                    state = 2
        introScreen()
        newPill = Pill(MIDDLE, TOP, 2)

    # SCREEN 2: CONTROL SCREEN--------------------------#
    if state == 2:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Play = False
            (cursorX, cursorY) = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if control_returnButton.collidepoint(cursorX, cursorY) is True:
                    state = 1
        controlScreen()

    # SCREEN 3: GAMEPLAY--------------------------------#
    if state == 3:
        # TIME
        timer = pygame.time.get_ticks() // 100
        time.sleep(0.1)

        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Play = False

            (cursorX, cursorY) = pygame.mouse.get_pos()
            if pause is True:
                if pauseResumeButton.collidepoint(cursorX, cursorY) is True:  # if resume button is clicked
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pause = False

                if pauseRestartButton.collidepoint(cursorX, cursorY) is True:    # if exit button is clicked
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        state = 1

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause = True

                if event.key == pygame.K_DOWN:
                    newPill.moveDown()
                    if newPill.collides(floor) or newPill.collides(obstacle):
                        newPill.moveUp()

                if event.key == pygame.K_UP:
                    newPill.rotateClock()
                    if newPill.collides(leftWall) or newPill.collides(rightWall) or newPill.collides(floor) or newPill.collides(obstacle):
                        newPill.rotateCounterClock()

                if event.key == pygame.K_LEFT:
                    newPill.moveLeft()
                    if newPill.collides(leftWall) or newPill.collides(obstacle):
                        newPill.moveRight()

                if event.key == pygame.K_RIGHT:
                    newPill.moveRight()
                    if newPill.collides(rightWall) or newPill.collides(obstacle):
                        newPill.moveLeft()

        # MAP
        obstacle.generateMap(COLUMNS, ROWS)
        obstacle.updateMap(LEFT, TOP)

        if timer % speed == 0:
            newPill.moveDown()
            if newPill.collides(floor) or newPill.collides(obstacle):
                newPill.moveUp()

                # FIND FOUR IN A ROW
                obstacle.append(newPill)
                obstacle.updateMap(LEFT, TOP)
                obstacle.findFour(LEFT, TOP)
                virusScore = obstacle.virusDisappear()
                if virusScore is True:
                    score += 1
                    virusesRemoved += 1
                newPill = Pill(MIDDLE, TOP)

        # YOU WIN
        if virusesRemoved == numViruses:
            Play = False
        if obstacle.collides(ceiling):
            state = 4

        redrawScreen()

    if state == 4:
        endScreen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Play = False
            (cursorX, cursorY) = pygame.mouse.get_pos()
            if restartButton.collidepoint(cursorX, cursorY) is True:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    state = 1

pygame.quit()
