from DrMario_CLASSES_Final import *
from random import randint
from math import sqrt
import pygame
import time
pygame.init()

# LOAD GAME SCREEN
# width: height = 32:28
WIDTH = 800
HEIGHT = 700
GRIDSIZE = HEIGHT//28  # side lenght of one square = 25
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# GAME SCREEN DIMENSIONS----------------------------------
COLUMNS = 8
ROWS = 16
LEFT = 12
RIGHT = LEFT + COLUMNS
MIDDLE = LEFT + COLUMNS//2
TOP = 9
FLOOR = TOP + ROWS

# COLOURS -----------------------
DARKGREY = (100,100,100)

# GAME VARIABLES----------------------
newPill = Pill(MIDDLE,TOP, 2)

floor = Bottom(LEFT, FLOOR, COLUMNS)
leftWall = Wall(LEFT-1, TOP, ROWS)
rightWall = Wall(RIGHT, TOP, ROWS)

obstacle = Obstacles(LEFT,FLOOR)

numViruses = 5
virusesRemoved = 0
viruses = Viruses(LEFT+1, RIGHT-1, TOP+8, FLOOR-1, numViruses)
obstacle.append(viruses)

Play = True
timer = 0
score = 0
speed = 10

def drawGrid():
    # draws faint gray lines in play screen for reference
    for x in range(0, WIDTH, GRIDSIZE):    # draw vertical
        pygame.draw.line(screen, DARKGREY, (x, 0), (x, HEIGHT))

    for y in range(0, HEIGHT, GRIDSIZE):     # draw horizontal
        pygame.draw.line(screen, DARKGREY, (0, y), (WIDTH, y))

    floor.draw(screen, GRIDSIZE)
    leftWall.draw(screen, GRIDSIZE)
    rightWall.draw(screen, GRIDSIZE)


def redrawScreen():
    screen.fill((0,0,0))
    drawGrid()
    newPill.draw(screen, GRIDSIZE)
    obstacle.draw(screen, GRIDSIZE)

    pygame.display.update()


while Play:
    # TIME
    timer = pygame.time.get_ticks() // 100
    time.sleep(0.1)

    # EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Play = False

        if event.type == pygame.KEYDOWN:
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
    redrawScreen()
