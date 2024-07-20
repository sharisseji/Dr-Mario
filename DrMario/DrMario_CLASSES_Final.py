#############################################
#   Programmer: Sharisse Ji                 #
#   Date: January 12, 2023                  #
#   File Name: DrMario_CLASSES_Final.py           #
#   Description: Dr Mario classes           #
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
COLOURS = [BLACK, RED,  BLUE, YELLOW, WHITE]
CLRNames = ['black', 'red', 'blue', 'yellow', 'white']
#            [0,    1          2        3       4]


#########################################################################
class Tile(object):
    def __init__(self, x=1, y=1, clr=1, virus=False):
        self._x = x
        self._y = y
        self._clr = clr
        self.virus = virus

    def __str__(self):
        return '('+str(self._x)+','+str(self._y)+') '+CLRNames[self._clr]

    def __eq__(self, other):                                # overload == operator
        if self._x == other._x and self._y == other._y:
            return True
        return False

    def draw(self, surface, gridsize=25):                   # draws ONE tile
        tileX = self._x *gridsize
        tileY = self._y*gridsize
        CLR = COLOURS[self._clr]
        if self.virus is False:                             # regular pill half/obstacle
            pygame.draw.rect(surface, CLR, (tileX, tileY, gridsize, gridsize), 0)
            pygame.draw.rect(surface, WHITE, (tileX, tileY, gridsize+1, gridsize+1), 1)
        else:                                               # virus
            pygame.draw.rect(surface, CLR, (tileX, tileY, gridsize, gridsize), 0)
            pygame.draw.rect(surface, WHITE, (tileX, tileY, gridsize+1, gridsize+1), 3)  # make border thicker


#########################################################################
class Group(object):
    def __init__(self, groupX=1, groupY=1, groupTileNo=2):  # for pill, blockNo will be 2
        self.x = groupX
        self.y = groupY
        self.tiles = [Tile()]*groupTileNo
        self.Xoffset = [0]*groupTileNo                      # need to be the same as in the Pill class
        self.Yoffset = [0]*groupTileNo
        self.clr = []

        for i in range(groupTileNo):
            i = randint(1,3)
            self.clr.append(i)

    def _update(self):                                      # loads all given attributes into a list of objects
        for i in range((len(self.tiles))):
            tileX = self.x + self.Xoffset[i]
            tileY = self.y + self.Yoffset[i]
            tileColour = self.clr[i]
            self.tiles[i] = Tile(tileX, tileY, tileColour, False)

    def draw(self, surface, gridsize):
        for tile in self.tiles:
            tile.draw(surface, gridsize)

    def collides(self, other):                              # if a group of tiles collides with another group
        for tile in self.tiles:                             # check every tile in this group with every tile in other
            for obstacle in other.tiles:
                if tile == obstacle:
                    return True
        return False

    def append(self, other):                                # will be used to combine groups to Obstacles class
        for tile in other.tiles:
            self.tiles.append(tile)


#########################################################################
class Pill(Group):
    def __init__(self, x=1, y=1, tileNo=2):                 # given from the outside
        Group.__init__(self, x, y, tileNo)                  # inherit everything from __init__ in Group class
        self.x = x
        self.y = y
        self._rot = 2
        self._rotate()

    def _rotate(self):
        #                    o             x
        #           o x      x     x o     o
        Xoffset = [[-1,0], [0,0], [0,-1], [0,0]]
        Yoffset = [[0,0], [-1,0], [0,0], [0,-1]]
        self.Xoffset = Xoffset[self._rot]
        self.Yoffset = Yoffset[self._rot]
        self._update()

    # MOVE THE PILL #
    def moveLeft(self):
        self.x = self.x - 1
        self._update()

    def moveRight(self):
        self.x = self.x + 1
        self._update()

    def moveDown(self):
        self.y = self.y + 1
        self._update()

    def moveUp(self):
        self.y = self.y - 1
        self._update()

    # ROTATE THE PILL #
    def rotateClock(self):
        self._rot = (self._rot+1) % 4
        self._rotate()

    def rotateCounterClock(self):
        self._rot = (self._rot-1) % 4
        self._rotate()


#########################################################################
class Viruses(Group):
    def __init__(self, x1, x2, y1, y2, numVirus):           # x and y will just be the random range
        Group.__init__(self, x1, y1, numVirus)
        self.x = []
        self.y = []
        self.clr = []
        self.virus = True                                   # virus, not tile
        for i in range(numVirus):                           # append random coordinates to lists
            self.x.append(randint(x1, x2))
            self.y.append(randint(y1, y2))
            self.clr.append(randint(1, 3))

        self._update()

    def _update(self):                                      # draws group of tiles using lists of tile class
        for i in range((len(self.tiles))):                  # for i in range (2)
            self.tiles[i] = Tile(self.x[i], self.y[i], self.clr[i], True)


#########################################################################
class Obstacles(Group):
    def __init__(self, x=0, y=0, tileNo=0):
        Group.__init__(self, x, y, tileNo)

        self.virusRemoved = False

    def __str__(self):
        return str(self.grid)

    def generateMap(self, columns, rows):                   # map is based on the columns and rows of game screen
        self.columns = columns
        self.rows = rows
        self.grid = []

        for x in range(columns):                            # INVERTED XY MAP (goes by Y then X)
            self.grid.append([])
            for y in range(rows):
                self.grid[x].append(0)

    def updateMap(self, left, top):                         # find the colours of every block and save it into map
        for tile in self.tiles:
            tileX = tile._x-left
            tileY = tile._y-top
            for x in range(self.columns):
                for y in range(self.rows):
                    if (tileX == x) and (tileY == y):
                        self.grid[x][y] = tile._clr

    def findFour(self, left, top):                          # needs to return multiple values
        self.counter = [1]*8
        self.currentCLR = 0

        for x in range(self.columns):
            for y in reversed(range(self.rows)):
                if (self.grid[x][y] == self.currentCLR) and (self.currentCLR != 0):
                    self.counter[x] += 1
                    if self.counter[x] >= 4:
                        self.removeFour(left, top, x, y, self.counter[x])
                else:
                    self.currentCLR = self.grid[x][y]       # update previous clr to current clr (compare with next)
            print(self.counter[x])

    def removeFour(self, left, top, columnX, rowY, counter):
        for i in reversed(range(len(self.tiles))):          # must be reversed to not go out of range
            pop = False
            for num in range(0,counter):                    # must append all of the tiles found in a row, not just one
                # column is same for all of them, starts with the y closest to the top, appends them going down
                if (self.tiles[i]._x-left == columnX) and (self.tiles[i]._y-top == rowY+num):
                    pop = True
                    if self.tiles[i].virus is True:
                        self.virusRemoved = True            # for score keeping in the main program
            if pop is True:
                self.tiles.pop(i)

    def virusDisappear(self):                               # for score keeping in main program
        if self.virusRemoved is True:
            self.virusRemoved = False
            return True
        return False


#########################################################################
class Bottom(Group):                                        # collisions with the floor
    def __init__(self,x=1, y=1, tileNo=1):
        Group.__init__(self, x, y, tileNo)
        self.clr = [4]*tileNo                               # draw it white for testing
        for i in range(0,tileNo):                           # horizontal line of blocks
            self.Xoffset[i] = i
        self._update()


class Wall(Group):                                          # collisions with the walls
    def __init__(self, x=1, y=1, tileNo=1):
        Group.__init__(self, x, y, tileNo)
        self.clr = [4]*tileNo                               # draw it white for testing
        for i in range(0,tileNo):                           # Vertical line of blocks
            self.Yoffset[i] = i
        self._update()

