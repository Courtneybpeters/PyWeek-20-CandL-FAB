import pygame, data, sys, os
from constants import *

class Weapon(object):
    def __init__(self, x, y, name, cost):
        self.location = (x,y)
        self.name = name
        self.weapon_image = self.load(name)
        self.cost = cost

    def load(self, name):
        return pygame.image.load(data.load(name+".png", 'rb'))

    def draw(self, surface):
        #draw image for weapon, rotate it toward the right direction.
        #if self.weapon_type == "turret1":
        surface.blit(self.weapon_image, (self.location[0]*CELL_SIZE, self.location[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

class Bomb(object):
    def __init__(self, location):
        self.location = location
