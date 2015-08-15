import pygame, data, sys, os
from constants import *
from map import *
from health import *
from money import *
from button import *
from weapon import *
from unit import *
from score import *

class Game (object):
    def __init__(self, level, font_filename):
        self.state = "playing"
        self.elapsed = 0
        self.map = self.load_level(level)
        self.path = self.map.findpath()
        self.font = self.load_font(font_filename)
        self.health = Health(self.font, 15)
        self.money = Money(self.font, 50)
        self.score = Score(self.font, 0)
        self.weapons = []
        self.costs = {"turret": 10, "bomb": 15}
        self.buttons = [Button("turret", (0, SCREEN_HEIGHT-CELL_SIZE)),
                        Button("bomb", (CELL_SIZE*2, SCREEN_HEIGHT-CELL_SIZE)),
                       ]
        self.bullets = {}
        self.units = {}
        self.active_button = None
        #todo: support multiple units
        self.unit_position = 0
        self.lifelost = pygame.mixer.Sound(data.filepath("LiveLost.wav"))

        self.difficulty = .5
        self.tickstowave = 2000
        self.wavespawns = 0

    def set_state(self, state):
        self.state = state

    def step(self, amount):
        #don't simulate world if game is paused.
        if self.state == "paused" or self.state == "lost":
            return

        prev_elapsed = int(self.elapsed)
        self.elapsed += amount
        steps = int(self.elapsed) - int(prev_elapsed)


        #for tests, spawn a unit every 100 steps and hurt all units every 100 steps
        if self.wavespawns > 0:
            if self.elapsed % 300 == 0:
                self.units[utils.get_id()] = Unit("strongman", 1000 * self.difficulty, 3, self.path)
                self.wavespawns -= 1
            elif self.elapsed % 300 == 250:
                self.units[utils.get_id()] = Unit("quickman", 500 * self.difficulty, 6, self.path)
                self.wavespawns -= 1


        for i in range(steps): #simulate the world for x steps

            #after each wave, increase difficulty by  a bit
            #waves only count down when no units are on the map.
            if len(self.units) == 0:
                self.tickstowave -= 1

            if self.tickstowave <= 0:
                self.difficulty += .5
                self.tickstowave = 1000
                self.wavespawns = 10 * self.difficulty


            for weapon in self.weapons:
                weapon.step()
            dead_bullets = []
            for id, bullet in self.bullets.iteritems():
                if bullet.has_hit():
                    dead_bullets.append(id)
                    #TODO: implement a damage radius
                    bullet.target_unit.hurt(bullet.damage)
                    bullet.sfx.play()
                else:
                    bullet.move()

            for unit_id in dead_bullets:
                del self.bullets[unit_id]

            dead_units = []
            for id, unit in self.units.iteritems():
                if unit.is_dead():
                    dead_units.append(id)
                    self.money.earn(5)
                    self.score.add()
                elif unit.has_won():
                    print "Unit won!"
                    dead_units.append(id)
                    self.health.hurt(1)
                    self.lifelost.play()
                    if (self.health.health <= 0):
                        self.state = "lost"
                else:
                    unit.move()
            for unit_id in dead_units:
                del self.units[unit_id]



            #TODO: check if unit has reached the end and subtract a life.


    def load_level(self, levelname):
        return Map(levelname)

    def load_font(self, filename):
         return pygame.font.Font(data.filepath(filename), 50)

    def click(self, x, y):
        # if click event is in the UI tray area, unselect all buttons then
        # select any that were clicked.
        if (y >= SCREEN_HEIGHT - CELL_SIZE):
            self.active_button = None
            for button in self.buttons:
                if not button.try_click(x, y):
                    button.deselect()
                else:
                    self.active_button = button

        #if the click event was on the map, and they have a selected button,
        #try to purchase that item.
        else:
            if self.active_button:
                map_x = x / CELL_SIZE
                map_y = y / CELL_SIZE
                if self.map.can_place(map_x, map_y):
                    name = self.active_button.name
                    weapon = Weapon(map_x, map_y, name,  self.costs[name], self)
                    if self.money.can_buy(weapon):
                        self.money.buy(weapon)
                        self.weapons.append(weapon)
                        self.map.set(map_x, map_y, TILETYPE.index("weapon"))
                        for button in self.buttons:
                            button.deselect() # Should we do this or no?
                            self.active_button = None
        print self.active_button
        """
        if selection is not None:# Purchasing
            if "buy" in selection:
                if "t_" in selection:
                    self.buy = "turret"
                        # TODO: Function that handles placement
                elif "b_" in selection:
                    self.buy = "bomb"

                if self.money.can_buy(self.money.costs[self.buy]):
                    self.money.purchase(self.buy)
                    if self.buy == "turret":
                        self.turrets.append(Weapon((9, 5), "turret1"))
                    if self.buy == "bomb":


                        pass
                        # add bomb function
        """
    def place_weapon(self, x, y, weapon):
        grid_x = x / CELL_SIZE
        grid_y = y / CELL_SIZE
        # if self.map.get(grid_x, grid_y) == ""
        print "Tile type: ", self.map.get(grid_x, grid_y)

    def draw(self, surface):
        if self.state == "playing":
            self.map.draw(surface)
            #draw UI
            self.health.draw(surface)
            self.money.draw(surface)
            self.score.draw(surface)

            #draw weapons
            for weapon in self.weapons:
                weapon.draw(surface)

            #draw purchasing buttons
            for button in self.buttons:
                button.draw(surface)
            #enemies and bullets aren't on grid
            #draw enemies
            for id, unit in self.units.iteritems():
                unit.draw(surface)

            #draw bullets
            for id, bullet in self.bullets.iteritems():
                bullet.draw(surface)


        elif self.state == "lost":
            surface.fill(BLACK, (0,0, SCREEN_WIDTH, SCREEN_HEIGHT))
            lose_txt = self.font.render("ERROR! ERROR! ERROR!", True, (255,255,0))
            lose_txt_rect = lose_txt.get_rect()
            lose_txt_rect.center = surface.get_rect().center
            lose_txt_rect.y -= 100
            surface.blit(lose_txt, lose_txt_rect)

            lose_txt = self.font.render("YOU. HAVE. LOST. ALL. THE. DATA.", True, (255,0,0))
            lose_txt_rect = lose_txt.get_rect()
            lose_txt_rect.center = surface.get_rect().center
            lose_txt_rect.y -= 0
            surface.blit(lose_txt, lose_txt_rect)


            lose_txt = self.font.render("SCORE. " + str(self.score.score) + ".", True, (0,255,0))
            lose_txt_rect = lose_txt.get_rect()
            lose_txt_rect.center = surface.get_rect().center
            lose_txt_rect.y += 100
            surface.blit(lose_txt, lose_txt_rect)
