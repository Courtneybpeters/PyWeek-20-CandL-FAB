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
class Map (object):
    def __init__(self, levelname):
        filename = levelname + ".txt"
        self.mapdata = []
        for line in data.load(filename, 'r').read():
            temp = []
            for char in line:
                temp.append(char)
            self.mapdata.append(temp)

class Game (object):
    def __init__(self):
        self.state = "mainmenu"
        self.elapsed = 0

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
    def draw(self):
        for col in range(BOARD_WIDTH):
            for row in range(BOARD_HEIGHT):
                #draw map
                pass
                #if (map.)

                #draw turrets

        #enemies and bullets aren't on grid
        #draw enemies

        #draw bullets

        pass




def main():

    # initialize pygame window
    game = Game()

    #skip "mainmenu" state since we're in development
    game.set_state("playing")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    #Main Loop
    exit = False
    while not exit:

        #update screen
        screen.fill(BGCOLOR, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
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
