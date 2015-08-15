import pygame, data, sys, os, utils
from constants import *

class Map (object):
    def __init__(self, levelname):
        filename = levelname + ".txt"
        self.mapdata = []
        for line in data.load(filename, 'r').readlines():
            temp = []
            for char in line.strip():
                temp.append(int(char))
            self.mapdata.append(temp)

    def get(self, x, y):
        return TILETYPE[self.mapdata[y][x]]
    def set(self, x, y, celltype):
        self.mapdata[y][x] = celltype

    def can_place(self, x, y):
        tile = self.get(x, y)
        if tile == "background":
            return True

    def draw(self, surface):
        #surface.fill(BGCOLOR, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        for x in range(BOARD_WIDTH):
            for y in range(BOARD_HEIGHT):
                #draw map
                cell = self.get(x,y)
                fillcolor = BGCOLOR
                if (cell == "path"):
                    fillcolor = PATHCOLOR
                elif (cell == "nobuild"):
                    fillcolor = UIBGCOLOR
                elif (cell == "pathstart"):
                    fillcolor = PATHSTARTCOLOR
                elif (cell == "pathend"):
                    fillcolor = PATHENDCOLOR
                surface.fill(fillcolor, (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def findpath(self):
        # determine where the start and end path are and then find all
        # consecutive paths between the start and end.
        start = end = None
        for x in range(BOARD_WIDTH):
            for y in range(BOARD_HEIGHT):
                if self.get(x,y) == "pathstart":
                    start = (x,y)
                elif self.get(x,y) == "pathend":
                    end = (x,y)
        if (start != None and end != None):
            # find path from start to end.
            current = start
            mapsolution = []
            while current != end:
                mapsolution.append(current)
                #find a cell up, down, left or right of our current that's not in used_paths.
                testcells = [(current[0]-1, current[1]), (current[0],current[1]-1), (current[0]+1, current[1]), (current[0], current[1]+1)]
                for cell in testcells:
                    if cell not in mapsolution and 0 < cell[0] < BOARD_WIDTH and 0 < cell[1] < BOARD_HEIGHT and self.get(cell[0], cell[1]) in ["pathstart", "pathend", "path"]:
                        current = cell
                        break
            mapsolution.append(end)
        solution = []
        #convert solution to screen coordinates
        #path.append(basepath.pop(0))
        while len(mapsolution) > 1:
            solution.extend(utils.lerp((mapsolution[0][0]*CELL_SIZE, mapsolution[0][1]*CELL_SIZE), \
                                   (mapsolution[1][0]*CELL_SIZE, mapsolution[1][1]*CELL_SIZE)))
            mapsolution.pop(0)
        return solution
