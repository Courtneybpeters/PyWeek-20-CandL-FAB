import pygame, data, sys, os, utils
from constants import *
from bullet import *

class Weapon(object):
    #splash is radius of damage
    def __init__(self, x, y, name, cost, game):
        self.location = (x,y)
        self.name = name
        self.weapon_image = self.load(name)
        self.cost = cost
        self.can_rotate = ROTATABLE[self.name]
        self.rotation = 0
        self.range = RANGE[self.name]
        self.regen = 0
        self.fire_speed = FIRE_SPEED[self.name]
        self.splash = SPLASH[self.name]
        self.bullet_color = BULLET_COLOR[self.name]
        self.bullet_speed = BULLET_SPEED[self.name]
        self.damage = DAMAGE[self.name]
        self.bullet_size = BULLET_SIZE[self.name]
        self.game = game #reference to game object so we can get the current
        #position of the main unit

    def step(self):
        ready_to_fire = False
        self.regen += 1
        if self.regen >= self.fire_speed:
            self.regen = self.fire_speed
            ready_to_fire = True

        #if it's ready to fire again and there's an enemy nearby, fire a bullet.
        if ready_to_fire:
            target = self.get_target()
            if target:
                self.fire(target)

    def fire(self, target_unit):
        #TODO: use a method to add the bullets instead
        self.game.bullets[utils.get_id()] = Bullet(self.bullet_speed, [self.get_map_center()[0], self.get_map_center()[1]], target_unit, self.bullet_color, self.bullet_size, self.damage)
        self.regen = 0

    def load(self, name):
        return pygame.image.load(data.load(name+".png", 'rb'))

    def rotate(self):
        if not self.can_rotate:
            return
        target = self.get_target()
        if target:
            direction = utils.aim_at(self.get_map_center(), target.get_map_center())
            self.rotation = direction

    def get_map_center(self):
        return (self.location[0] * CELL_SIZE + (CELL_SIZE/2), self.location[1] * CELL_SIZE + (CELL_SIZE/2))

    def get_target(self):
        #determine the target unit.
        target_unit = None
        target_unit_distance = 999999
        for id, unit in self.game.units.iteritems():
            dist = utils.distance(self.get_map_center(), unit.get_location())
            if dist < target_unit_distance and dist < self.range:
                target_unit_distance = dist
                target_unit = unit
        return target_unit

    def draw(self, surface):
        #draw image for weapon, rotate it toward the right direction.
        #calculate the amount of rotation required
        self.rotate()
        new_image = pygame.transform.rotate(self.weapon_image, self.rotation)
        rect = new_image.get_rect()
        rect.center = (self.location[0]*CELL_SIZE + (CELL_SIZE/2), self.location[1]*CELL_SIZE + (CELL_SIZE/2))

        #if self.weapon_type == "turret1":
        surface.blit(new_image, rect)


class Bomb(object):
    def __init__(self, location):
        self.location = location
