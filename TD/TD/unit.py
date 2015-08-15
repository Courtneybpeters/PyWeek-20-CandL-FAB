import pygame, data, sys, os, utils
from constants import *
class Unit(object):
    def __init__(self, name, health, speed, path):
        self.name = name
        self.unit_image = self.load_image(name)
        self.max_health = health
        self.health = health
        self.speed = speed # speed is a 1-10 value.
        self.path = path
        self.position = 0 #start at position 0.
        self.slowfactor = 1

    def slow(self, factor):
        self.slowfactor = factor

    def unslow(self, factor):
        self.slowfactor = 1

    def is_dead(self):
        return self.health < 0
    def has_won(self):
        return int(self.position) >= len(self.path)-1

    def move(self):
        self.position += (self.speed / 10.0) * 2.5 * self.slowfactor

    def get_map_center(self):
        return (self.get_location()[0] + (CELL_SIZE / 2), self.get_location()[1] + (CELL_SIZE / 2))

    def get_location(self):
        p = int(self.position)
        return (self.path[p][0], self.path[p][1])

    def draw(self, surface):
        p = int(self.position)
        #draw their health bar.
        green_width = CELL_SIZE*(float(self.health)/self.max_health)
        health_green_rect = (self.path[p][0], self.path[p][1], green_width, 5)
        #print health_green_rect
        health_red_rect = (self.path[p][0]+green_width, self.path[p][1], CELL_SIZE-green_width, 5)
        #print health_red_rect
        surface.blit(self.unit_image, (self.path[p][0], self.path[p][1], CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(surface, (0,255,0), health_green_rect)
        pygame.draw.rect(surface, (255,0,0), health_red_rect)

    def hurt(self, amount):
        self.health -= amount

    def load_image(self, name):
        print name
        return pygame.image.load(data.load(name+".png", 'rb'))
