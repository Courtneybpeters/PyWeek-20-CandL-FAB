import pygame, data, sys, os
from constants import *
class Money(object):
    def __init__(self, font, balance):
        self.balance = balance # Player always starts with a little cash to start
        self.font = font

    def can_buy(self, weapon):
        return weapon.cost <= self.balance

    def buy(self, weapon):
        if weapon.cost > self.balance:
            return
        self.balance -= weapon.cost
        print weapon.name, " purchased"

    def earn(self, gain):
        self.balance += gain

    def draw(self, surface):
        money_txt = "$" + str(self.balance)
        money_txt_obj = self.font.render(money_txt, True, BLACK)
        money_txt_rect = money_txt_obj.get_rect()
        money_txt_rect.topleft = (10, 0)
        surface.blit(money_txt_obj, money_txt_rect)
