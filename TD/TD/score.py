import pygame, data, sys, os
from constants import *

class Score(object):

    def __init__(self, font, score):
        self.score = score
        self.font = font

    def add(self):
        self.score += 1

    def draw(self, surface):
        score_txt = "Killed: " + str(self.score)
        score_txt_obj = self.font.render(score_txt, True, BLACK)
        score_txt_rect = score_txt_obj.get_rect()
        score_txt_rect.bottomright = (SCREEN_WIDTH-10, SCREEN_HEIGHT)
        surface.blit(score_txt_obj, score_txt_rect)
