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
BLACK = (0,0,0)
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
        return solution

class Turret (object):
    def __init__(self, location, turret_type):
        self.location = location
        self.turret_type = turret_type
        self.turret_image = self.load(turret_type)

    def load(self, turret_type):
        return pygame.image.load(data.load(turret_type+".png", 'rb'))

    def draw(self, surface):
        if self.turret_type == "turret1":
            surface.blit(self.turret_image, (self.location[0]*CELL_SIZE, self.location[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

class Lives (object):
    DATA_TXT = "DATA! DATA! DATA!"

    def __init__(self, font, lives):
        self.font = font
        self.lives = lives
        self.lives_txt = Lives.DATA_TXT[:self.lives + 2]

    def draw(self, surface):
        # Lives - Data Data Data draw
        lives_txt_obj = self.font.render(self.lives_txt, True, BLACK)
        lives_txt_rect = lives_txt_obj.get_rect()
        lives_txt_rect.topright = ((1024 - 10), 0)    # 10 pixels of padding
        lives_txt_rect.y = 0
        surface.blit(lives_txt_obj, lives_txt_rect)

class Game (object):
    def __init__(self, level, font_filename):
        self.state = "mainmenu"
        self.elapsed = 0
        self.map = self.load_level(level)
        self.font = self.load_font(font_filename)
        self.lives = Lives(self.font, 12)
        self.deaths = 3

    def set_state(self, state):
        self.state = state

    def step(self, amount): #simulate the world for x steps (amount is a float)
        #don't simulate world if game is paused.
        if self.state == "paused":
            return
        #TODO: simulate game world
        pass

    def load_level(self, levelname):
        return Map(levelname)

    def load_font(self, filename):
         return pygame.font.Font(data.filepath(filename), 50)

    def click(self, x, y):
        pass

    def draw(self, surface):
        self.map.draw(surface)

        #draw UI
        self.lives.draw(surface)

        #draw turrets
        turrets = []
        turrets.append(Turret((9, 5), "turret1"))
        turrets.append(Turret((5, 6), "turret1"))

        for turret in turrets:
            turret.draw(surface)

        #enemies and bullets aren't on grid
        #draw enemies

        #draw bullets




def main():
    # initialize pygame window
    pygame.init()
    pygame.display.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    game = Game("map1", "brokeren.regular.ttf")
    path = game.map.findpath()
    #skip "mainmenu" state since we're in development
    game.set_state("playing")

    #Main Loop
    exit = False
    p = 0
    while not exit:

        #update screen
        game.draw(screen)
        #this is just a test to see a unit move along the path.
        p += .0015
        p %= len(path)
        p2 = int(p)
        screen.fill(BLACK, (path[p2][0]*CELL_SIZE, path[p2][1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
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
