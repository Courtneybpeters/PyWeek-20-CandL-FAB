import pygame, data, sys, os
from pygame.locals import *
from constants import *
from game import Game as Game

def main():
    # initialize pygame window
    pygame.init()
    pygame.display.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    game = Game("map1", "brokeren.regular.ttf")
    clock = pygame.time.Clock()
    #Main Loop
    exit = False
    p = 0
    while not exit:
        text = "FPS: {0:.2f}".format(clock.get_fps())
        pygame.display.set_caption(text)
        clock.tick(100)
        #update screen
        game.step(1)
        game.draw(screen)
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
