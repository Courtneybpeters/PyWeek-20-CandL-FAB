import pygame, sys, os, data
from pygame.locals import *


#Tiletype
"""
9 - end of enemy path (you lose life if they make it here)
8 - start of enemy path
7 - non building area (UI)
6 - capacitors?
1 - path
0 - background
"""
TILETYPE = ["background","path","unused","unused","unused","unused","capacitors","nobuild","pathstart","pathend"]

#TODO: move to config file
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
CELL_SIZE = 64
BOARD_WIDTH = 16
BOARD_HEIGHT = 12

BGCOLOR = (0,160,0)
PATHCOLOR = (150,150,0)
UIBGCOLOR = (125,125,125)
BLACK = (0, 0, 0)
PATHSTARTCOLOR = (0,0,255)
PATHENDCOLOR = (255,0,0)

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
            solution = []
            while current != end:
                solution.append(current)
                #find a cell up, down, left or right of our current that's not in used_paths.
                testcells = [(current[0]-1, current[1]), (current[0],current[1]-1), (current[0]+1, current[1]), (current[0], current[1]+1)]
                for cell in testcells:
                    if cell not in solution and 0 < cell[0] < BOARD_WIDTH and 0 < cell[1] < BOARD_HEIGHT and self.get(cell[0], cell[1]) in ["pathstart", "pathend", "path"]:
                        current = cell
                        break
            solution.append(end)
        print solution
        return solution


class Game (object):
    def __init__(self):
        self.state = "mainmenu"
        self.elapsed = 0
        self.data_txt = "DATA DATA DATA"

    def set_state(self, state):
        self.state = state

    def step(self, amount): #simulate the world for x steps (amount is a float)
        #don't simulate world if game is paused.
        if self.state == "paused":
            return
        #TODO: simulate game world
        pass

    def load_level(self, levelname):
        self.map = Map(levelname)



    def draw(self, surface, font):
        #surface.fill(BGCOLOR, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        for x in range(BOARD_WIDTH):
            for y in range(BOARD_HEIGHT):
                #draw map
                cell = self.map.get(x,y)
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

        # Lives - Data Data Data draw
        data_txt_obj = font.render(self.data_txt, True, BLACK)
        data_txt_rect = data_txt_obj.get_rect()
        data_txt_rect.centerx = SCREEN_WIDTH / 2
        data_txt_rect.y = 0
        surface.blit(data_txt_obj, data_txt_rect)

        #draw turrets

        #enemies and bullets aren't on grid
        #draw enemies

        #draw bullets




def main():

    # initialize pygame window
    game = Game()
    game.load_level("map1")
    path = game.map.findpath()
    #skip "mainmenu" state since we're in development
    game.set_state("playing")
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font_filepath = data.load("brokeren.regular.ttf")
    font = pygame.font.Font(font_filepath, 20)


    #Main Loop
    exit = False
    p = 0
    while not exit:

        #update screen
        game.draw(screen, font)
        #this is just a test to see a unit move along the path.
        p += .0015
        p %= len(path)
        p2 = int(p)
        screen.fill((0,0,0), (path[p2][0]*CELL_SIZE, path[p2][1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.display.update()

        # event loop for user input
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    exit = True
            elif event.type == QUIT:
                pygame.quit()
                exit = True
