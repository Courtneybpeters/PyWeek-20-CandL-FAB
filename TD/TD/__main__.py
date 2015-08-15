import pygame, data, sys, os
from pygame.locals import *
from constants import *
from game import Game as Game

#TODO: Global font????????




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
            if event.type == MOUSEBUTTONDOWN:
                x, y = event.pos
                game.click(x, y)

            elif event.type == QUIT:
                pygame.quit()
                exit = True
