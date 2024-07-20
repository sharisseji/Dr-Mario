

from DrMario_CLASSES_v2 import *
from random import randint
import pygame
import time
pygame.init()

# LOAD GAME SCREEN
# width: height = 32:28
screenWIDTH = 800
screenHEIGHT = 700
GRIDSIZE = screenHEIGHT//28  # side length of one square = 25
screen = pygame.display.set_mode((screenWIDTH, screenHEIGHT))

# GAME SCREEN DIMENSIONS----------------------------------

COLUMNS = 8
ROWS = 16
LEFT = 11
RIGHT = LEFT + COLUMNS
MIDDLE = LEFT + COLUMNS//2
TOP = 8
FLOOR = TOP + ROWS
# gameWIDTH = GRIDSIZE*COLUMNS
# gameHEIGHT = GRIDSIZE*ROWS

# LEFT = 11*GRIDSIZE
# RIGHT = LEFT + COLUMNS*GRIDSIZE
# MIDDLE = LEFT + (COLUMNS//2*GRIDSIZE)
#
# TOP = 8*GRIDSIZE
# FLOOR = TOP + ROWS*GRIDSIZE

# COLOURS -----------------------
DARKGREY = (150,150,150)

# GAME VARIABLES----------------------
Play = True
map = Map(LEFT, TOP, COLUMNS, ROWS, GRIDSIZE)
newPill = Pill(MIDDLE,TOP+1)

timer = 0
speed = 10

# FUNCTIONS---------------------------
def drawGrid():
    # draws faint gray lines in play screen
    screen.fill((0,0,0))

    print(map.__str__())
    map.updateMap(newPill.giveX(),newPill.giveXoffset(), newPill.giveY(), newPill.giveYoffset(),
                  newPill.giveColour1(), newPill.giveColour2())

    map.drawMap(screen)
#
    pygame.display.update()
#     pass

# def redrawGameScreen():
#     # testing pill
#     screen.fill((0,0,0))
#     drawGrid()
#     newPill.draw(screen, GRIDSIZE)
#     obstacle.draw(screen, GRIDSIZE)
#     print(newPill.__str__())

while Play:
    # TIMER
    timer = pygame.time.get_ticks() // 100
    time.sleep(0.08)

    drawGrid()
    # obstacle._generateTileMap(COLUMNS, ROWS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Play = False
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:
                 newPill.rotateClock()

    #             if newPill.collides(leftWall) or newPill.collides(rightWall) or newPill.collides(floor) or newPill.collides(obstacle):
    #                 newPill.rotateCounterClock(COLUMNS, ROWS)
    #
    #         if event.key == pygame.K_LEFT:
    #             newPill.moveLeft(COLUMNS, ROWS)
    #             if newPill.collides(leftWall) or newPill.collides(obstacle):
    #                 newPill.moveRight(COLUMNS, ROWS)
    #
    #         if event.key == pygame.K_RIGHT:
    #             newPill.moveRight(COLUMNS, ROWS)
    #             if newPill.collides(rightWall) or newPill.collides(obstacle):
    #                 newPill.moveLeft(COLUMNS, ROWS)
    #
    if timer % speed == 0:
        newPill.moveDown()
    #     if newPill.collides(floor):
    #         newPill.moveUp(COLUMNS, ROWS)
    #         newPill = Pill(MIDDLE, TOP)
    # # obstacle.findFour(TOP, FLOOR)
    # redrawScreen()
