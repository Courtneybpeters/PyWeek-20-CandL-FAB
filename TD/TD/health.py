import pygame, data, sys, os
from constants import *
class Health(object):
    def __init__(self, font, health):
        self.font = font
        self.health = health
        self.health_txt = HEALTH_TXT
    def hurt(self, amount):
        self.health -= amount
        self.health_txt = HEALTH_TXT[:self.health + (self.health / 5)]

    def draw(self, surface):
        # Health - Data Data Data draw
        health_txt_obj = self.font.render(self.health_txt, True, BLACK)
        health_txt_rect = health_txt_obj.get_rect()
        health_txt_rect.topleft = (600, 0)    # 10 pixels of padding
        health_txt_rect.y = 0
        surface.blit(health_txt_obj, health_txt_rect)
