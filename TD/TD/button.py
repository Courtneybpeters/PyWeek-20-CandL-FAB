import pygame, data, sys, os
from constants import *
class Button(object):
    def __init__(self, name, location):
        self.selected = False
        self.name = name
        self.button_image = self.load(name)
        self.location = location
        self.button_rect = self.button_image.get_rect()
        self.button_rect.topleft = location
        print self.button_rect

    def load(self, name):
        return pygame.image.load(data.load(name+"_button.png", 'rb'))

    def try_click(self, x, y):
        #if x & y are in button's rect, toggle button state.
        if self.button_rect.collidepoint(x, y):
            self.selected = True
            return True
        else:
            return False

    def deselect(self):
        self.selected = False

    def draw(self, surface):
        surface.blit(self.button_image, self.location)
        if (self.selected):
            pygame.draw.rect(surface, (0,255,0), self.button_rect.inflate(-1,-1), 2)
    #TODO: EVERYTHING SHOULD HAVE DRAW METHOD SO SHOULD BE ABLE TO DRAW A BUTTON
