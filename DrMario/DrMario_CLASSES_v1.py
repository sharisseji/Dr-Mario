#############################################
#   Programmer: Sharisse Ji                 #
#   Date: January 12, 2023                  #
#   File Name: DrMario_CLASSES_Final.py           #
#   Description: Dr Mario main program      #
#############################################

import pygame
from random import randint

# ------ COLOURS ----------#
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
GREY = (192, 192, 192)
COLOURS = [RED,  BLUE, YELLOW]
CLRNames = ['red', 'blue', 'yellow']
figures =  ['R',    'B',    'Y']


class Tile(object):
    def __init__(self, x = 1, y = 1, clr = 0):
        self.x = x
        self.y = y
        self.clr = clr

    def __str__(self):
        return '('+str(self.x)+','+str(self.y)+') '+CLRNames[self.clr]

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        return False

    def draw(self, surface, gridsize=25):  # gridsize will be held with GRIDSIZE variable from main
        tileX = self.x *gridsize
        tileY = self.y*gridsize
        CLR = COLOURS[self.clr]
        pygame.draw.rect(surface, CLR, (tileX, tileY,gridsize,gridsize),0)
        pygame.draw.rect(surface, WHITE, (tileX, tileY, gridsize+1, gridsize+1),1)

    def moveDown(self):
        self.y = self.y + 1

    def moveUp(self):
        self.y = self.y - 1


class Pill(object):
    def __init__(self, x=1, y=1, tileNo = 2):  # there cannot be an anchor
        self.x = x
        self.y = y
        self.clr = [randint(0,2), randint(0,2)]
        self.tiles = [Tile()]*tileNo
        self._rot = 2
        self.Xoffset = [0,0]
        self.Yoffset = [0,0]
        self.rotate()

    def __str__(self):
        return self.Xoffset

    def rotate(self):
        #                    o             x
        #           o x      x     x o     o
        # Xoffset = [[0,-1], [0,0], [0,1], [0,0]]
        # Yoffset = [[0,0], [0,-1], [0,0], [1,0]]

        Xoffset = [[0,-1], [0,0], [-1,0], [0,0]]
        Yoffset = [[0,0], [0,-1], [0,0], [-1,0]]
        self.Xoffset = Xoffset[self._rot]
        self.Yoffset = Yoffset[self._rot]
        self._update()

    def rotateClock(self):
        self._rot = (self._rot+1) % 4
        self.rotate()

    def rotateCounterClock(self):
        self._rot = (self._rot-1) % 4
        self.rotate()

    def _update(self):
        for i in range(len(self.tiles)):
            tileX = self.x + self.Xoffset[i]  # + offsets
            tileY = self.y + self.Yoffset[i]
            tileColour = self.clr[i]
            self.tiles[i] = Tile(tileX, tileY, tileColour)

    def draw(self, surface, gridsize):
        for tile in self.tiles:
            tile.draw(surface, gridsize)


class Obstacles(object):
    pass