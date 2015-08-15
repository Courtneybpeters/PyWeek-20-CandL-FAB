import pygame, sys, os, data
from pygame.locals import *


#Tiletype
"""
9 - end of enemy path (you lose life if they make it here)
8 - start of enemy path
7 - non building area (UI)
6 - capacitors?
1 - path
0 - background
"""
TILETYPE = ["background","path","weapon","unused","unused","unused","capacitors","nobuild","pathstart","pathend"]

#TODO: move to config file
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
CELL_SIZE = 64
BOARD_WIDTH = 16
BOARD_HEIGHT = 12

BGCOLOR = (0,160,0)
PATHCOLOR = (150,150,0)
UIBGCOLOR = (125,125,125)
BLACK = (0,0,0)
PATHSTARTCOLOR = (0,0,255)
PATHENDCOLOR = (255,0,0)

#TODO: Global font????????

class Map (object):
    map_rect = pygame.Rect((0, 65), (1024, 640))

    def __init__(self, levelname):
        filename = levelname + ".txt"
        self.mapdata = []
        for line in data.load(filename, 'r').readlines():
            temp = []
            for char in line.strip():
                temp.append(int(char))
            self.mapdata.append(temp)

    def get(self, x, y):
        return TILETYPE[self.mapdata[y][x]]
    def set(self, x, y, celltype):
        self.mapdata[y][x] = celltype

    def can_place(self, x, y):
        tile = self.get(x, y)
        if tile == "background":
            return True

    def draw(self, surface):
        #surface.fill(BGCOLOR, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        for x in range(BOARD_WIDTH):
            for y in range(BOARD_HEIGHT):
                #draw map
                cell = self.get(x,y)
                fillcolor = BGCOLOR
                if (cell == "path"):
                    fillcolor = PATHCOLOR
                elif (cell == "nobuild"):
                    fillcolor = UIBGCOLOR
                elif (cell == "pathstart"):
                    fillcolor = PATHSTARTCOLOR
                elif (cell == "pathend"):
                    fillcolor = PATHENDCOLOR
                surface.fill(fillcolor, (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def findpath(self):
        # determine where the start and end path are and then find all
        # consecutive paths between the start and end.
        start = end = None
        for x in range(BOARD_WIDTH):
            for y in range(BOARD_HEIGHT):
                if self.get(x,y) == "pathstart":
                    start = (x,y)
                elif self.get(x,y) == "pathend":
                    end = (x,y)
        if (start != None and end != None):
            # find path from start to end.
            current = start
            solution = []
            while current != end:
                solution.append(current)
                #find a cell up, down, left or right of our current that's not in used_paths.
                testcells = [(current[0]-1, current[1]), (current[0],current[1]-1), (current[0]+1, current[1]), (current[0], current[1]+1)]
                for cell in testcells:
                    if cell not in solution and 0 < cell[0] < BOARD_WIDTH and 0 < cell[1] < BOARD_HEIGHT and self.get(cell[0], cell[1]) in ["pathstart", "pathend", "path"]:
                        current = cell
                        break
            solution.append(end)
        return solution

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

class Lives(object):
    DATA_TXT = "DATA! DATA! DATA!"

    def __init__(self, font, lives):
        self.font = font
        self.lives = lives
        self.lives_txt = Lives.DATA_TXT[:self.lives + (self.lives / 5)]
        # size = font.size("Data! Data! Data!")
        # print "Size", size

    def draw(self, surface):
        # Lives - Data Data Data draw
        lives_txt_obj = self.font.render(self.lives_txt, True, BLACK)
        lives_txt_rect = lives_txt_obj.get_rect()
        lives_txt_rect.topleft = (600, 0)    # 10 pixels of padding
        lives_txt_rect.y = 0
        surface.blit(lives_txt_obj, lives_txt_rect)

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



class Game (object):
    def __init__(self, level, font_filename):
        self.state = "mainmenu"
        self.elapsed = 0
        self.map = self.load_level(level)
        self.font = self.load_font(font_filename)
        self.lives = Lives(self.font, 15)
        self.money = Money(self.font, 150)
        self.weapons = []
        self.costs = {"turret": 10, "bomb": 15}
        self.buttons = [Button("turret", (0, SCREEN_HEIGHT-CELL_SIZE)),
                        Button("bomb", (CELL_SIZE*2, SCREEN_HEIGHT-CELL_SIZE)),
                       ]
        self.active_button = None
        #self.weapons = {"turrets":self.turrets, "bombs":self.bombs}
        #self.buy = ""

    def set_state(self, state):
        self.state = state

    def step(self, amount): #simulate the world for x steps (amount is a float)
        #don't simulate world if game is paused.
        if self.state == "paused":
            return
        #TODO: simulate game world
        pass

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
                    weapon = Weapon(map_x, map_y, self.active_button.name,  self.costs[name])
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
        #TODO: Money and lives in one UI class?
        self.lives.draw(surface)
        self.money.draw(surface)
        self.money.draw_store(surface)

        #draw turrets
        # turrets.append(Weapon((5, 6), "turret1"))

        for weapon in self.weapons:
            weapon.draw(surface)

        #draw purchasing buttons
        for button in self.buttons:
            button.draw(surface)
        #enemies and bullets aren't on grid
        #draw enemies

        #draw bullets

def main():
    # initialize pygame window
    pygame.init()
    pygame.display.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    game = Game("map1", "brokeren.regular.ttf")
    path = game.map.findpath()
    #skip "mainmenu" state since we're in development
    game.set_state("playing")

    #Main Loop
    exit = False
    p = 0
    while not exit:

        #update screen
        game.draw(screen)
        #this is just a test to see a unit move along the path.
        p += .0015
        p %= len(path)
        p2 = int(p)
        screen.fill(BLACK, (path[p2][0]*CELL_SIZE, path[p2][1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.display.update()

        # event loop for user input
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    exit = True
            if event.type == MOUSEBUTTONDOWN:
                x, y = event.pos
                #if Map.map_rect.collidepoint(x, y): # Check if click on map
                #    game.place_weapon(x, y, game.buy)
                game.click(x, y)

            elif event.type == QUIT:
                pygame.quit()
                exit = True
