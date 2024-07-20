import pygame
from random import randint

# ------ COLOURS ----------#
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
GREY = (192, 192, 192)
COLOURS = [BLACK, RED, BLUE, YELLOW]

# RED = 0
# BLUE = 1
# YELLOW = 2
class Map(object):
    def __init__(self, startX, startY, columns, rows, gridsize):  # just the list of values, no sizing needed
        self.grid = []
        self.columns = columns
        self.rows = rows
        self.GS = gridsize
        self.sX = startX
        self.sY = startY

        for x in range(columns):
            self.grid.append([])
            for y in range(rows):
                self.grid[x].append(0)
        print(self.grid)

    def __str__(self):
        return str(self.grid)

    def drawMap(self, surface):
        for x in range(self.columns):
            for y in range(self.rows):
                if self.grid[x][y] == 0:
                    COLOUR = COLOURS[0]

                elif self.grid[x][y] == 1:  # red
                    COLOUR = COLOURS[1]

                elif self.grid[x][y] == 2:  # blue
                    COLOUR = COLOURS[2]

                elif self.grid[x][y] == 3:  # yellow
                    COLOUR = COLOURS[3]

                pygame.draw.rect(surface, COLOUR, ((x+self.sX)*self.GS, (y+self.sY)*self.GS, self.GS, self.GS),0)
                pygame.draw.rect(surface, WHITE, ((x+self.sX)*self.GS+1, (y+self.sY)*self.GS+1, self.GS+1, self.GS+1), 1)

    def updateMap(self, pillX1, pillX2, pillY1, pillY2, pillCLR1, pillCLR2):
        self.pillX1 = pillX1-self.sX
        self.pillX2 = pillX2-self.sX
        self.pillY1 = pillY1-self.sY
        self.pillY2 = pillY2-self.sY
        self.pillCLR1 = pillCLR1
        self.pillCLR2 = pillCLR2
        for x in range(self.columns):
            for y in range(self.rows):
                if (x == self.pillX1 and y == self.pillY1) or (x == self.pillX2 and y == self.pillY2):
                    self.grid[self.pillX1][self.pillY1] = self.pillCLR1
                    self.grid[self.pillX2][self.pillY2] = self.pillCLR2
                else:
                    self.grid[x][y] = 0

    def checkFour(self):
        pass

    def removeFour(self):
        pass


class Pill(object):
    def __init__(self, x=1, y=1):  # there cannot be an anchor
        # block one: anchor
        self.x = x
        self.y = y

        # block two
        self.Xoffset = [0,0]
        self.Yoffset = [0,0]

        self.clr = [randint(1,3), randint(1,3)]

        self._rot = 2
        self._rotate()

    def __eq__(self,other):
        if self.x == other.x and self.y == other.y:
            return True
        return False

    def collides(self,other):
        pass

    def _rotate(self):
        #                    o             x
        #           o x      x     x o     o
        Xoffset = [[0,-1], [0,0], [-1,0], [0,0]]
        Yoffset = [[0,0], [0,-1], [0,0], [-1,0]]
        self.Xoffset = Xoffset[self._rot]
        self.Yoffset = Yoffset[self._rot]
        # self.update()

    # MOVE THE PILL ---------------------
    def moveLeft(self):
        self.x = self.x - 1

    def moveRight(self):
        self.x = self.x + 1

    def moveDown(self):
        self.y = self.y + 1

    def moveUp(self):
        self.y = self.y - 1

    # ROTATE THE PILL ---------------------
    def rotateClock(self):
        self._rot = (self._rot+1) % 4
        self._rotate()

    def rotateCounterClock(self):
        self._rot = (self._rot-1) % 4
        self._rotate()

    # RETURN VALUES TO UPDATE MAP----------
    def giveX(self):
        return int(self.x+self.Xoffset[0])

    def giveXoffset(self):
        return self.x+self.Xoffset[1]

    def giveY(self):
        return self.y+self.Yoffset[0]

    def giveYoffset(self):
        return self.y+self.Yoffset[1]

    def giveColour1(self):
        return self.clr[0]

    def giveColour2(self):
        return self.clr[1]

# class Tile(object):
#     def __init__(self, x=0, y=0):
#         self._x = x
#         self._y = y
#
#     # def __str__(self):
#     #     return '('+str(self.tileX)+','+str(self.tileY)+') '+ PILLCOLOURS[self.tileColour]
#
#     def __eq__(self, other):
#         if self._x == other._x and self._y == other._y:
#             return True
#         return False

# class Bottom(object):
#     def __init__(self,x=1, y=1, tileNo=1, columns=0, rows=0):
#         Group.__init__(self, x,y, tileNo)
#         self.clr = [4]*tileNo  # draw it white
#         for i in range(0,tileNo):
#             self.Xoffset[i] = i
#         self._update(columns, rows)
#
#
# class Wall(object):                                # Loads the wall blocks
#     def __init__(self, x=1, y=1, tileNo=1, columns=0, rows=0):
#         Group.__init__(self, x, y, tileNo)
#         self.clr = [4]*tileNo  # draw it white
#         for i in range(0,tileNo):                   # Vertical line of blocks
#             self.Yoffset[i] = i
#         self._update(columns, rows)