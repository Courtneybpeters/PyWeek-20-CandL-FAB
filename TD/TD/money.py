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

    def draw_store(self, surface):
        pass
        """
        turret = pygame.image.load(data.load("test_turret.png", 'rb'))
        bomb = pygame.image.load(data.load("bomb.png", 'rb'))
        t_buy_rect = pygame.Rect((0, 704), (64, 64))
        b_buy_rect = pygame.Rect((70, 704), (64, 64))
        surface.blit(turret, t_buy_rect.topleft)
        surface.blit(bomb, b_buy_rect.topleft)

        if not self.buttons:
            Buttons.add_button({"t_buy":t_buy_rect, "b_buy":b_buy_rect})
            self.buttons = True
        """
