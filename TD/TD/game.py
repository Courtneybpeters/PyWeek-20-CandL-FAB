import pygame, data, sys, os
from constants import *
from map import *
from health import *
from money import *
from button import *
from weapon import *
from unit import *

class Game (object):
    def __init__(self, level, font_filename):
        self.state = "mainmenu"
        self.elapsed = 0
        self.map = self.load_level(level)
        self.path = self.map.findpath()
        self.font = self.load_font(font_filename)
        self.health = Health(self.font, 15)
        self.money = Money(self.font, 150)
        self.weapons = []
        self.costs = {"turret": 10, "bomb": 15}
        self.buttons = [Button("turret", (0, SCREEN_HEIGHT-CELL_SIZE)),
                        Button("bomb", (CELL_SIZE*2, SCREEN_HEIGHT-CELL_SIZE)),
                       ]
        self.units = {}
        self.active_button = None
        #todo: support multiple units
        self.unit_position = 0

    def set_state(self, state):
        self.state = state

    def step(self, amount):
        #don't simulate world if game is paused.
        if self.state == "paused":
            return

        prev_elapsed = int(self.elapsed)
        self.elapsed += amount
        steps = int(self.elapsed) - int(prev_elapsed)

        #for tests, spawn a unit every 100 steps and hurt all units every 100 steps
        if (self.elapsed % 100 == 0):
            self.units[utils.get_id()] = Unit("strongman", 1000, 3, self.path)
            #test hurting all units 5 HP
            for id, unit in self.units.iteritems():
                unit.hurt(100)
        elif (self.elapsed % 100 == 50):
            self.units[utils.get_id()] = Unit("quickman", 500, 6, self.path)

        for i in range(steps): #simulate the world for x steps
            dead_units = []
            for id, unit in self.units.iteritems():
                if unit.is_dead():
                    dead_units.append(id)
                    self.money.earn(10)
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
                    weapon = Weapon(map_x, map_y, self.active_button.name,  self.costs[name], self)
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
        self.map.draw(surface)
        #draw UI
        self.health.draw(surface)
        self.money.draw(surface)
        self.money.draw_store(surface)

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
