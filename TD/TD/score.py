import pygame, data, sys, os
from constants import *

class Score(object):

    def __init__(self, font):
        self.score = 0
        self.font = font

    def add_score(self):
        score += 1

    def draw(self, surface):
        score_txt = "Killed: " + str(self.score)
        score_txt_obj = self.font.render(score_txt, True, BLACK)
        # print "score text size: ", self.font.size(score_txt)
        score_txt_rect = score_txt_obj.get_rect()
        score_txt_rect.topleft = (812, 700)
        surface.blit(score_txt_obj, score_txt_rect)
