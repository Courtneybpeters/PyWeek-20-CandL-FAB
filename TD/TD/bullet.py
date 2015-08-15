import math

class Bullet(object):
    def __init__(self, speed, location, target_unit, color, size, sfx, damage):
        self.speed = speed
        self.location = location
        self.damage = damage
        self.target_unit = target_unit
        self.color = color
        self.size = size
        self.sfx = sfx
        self.hit = False

    def has_hit(self):
        return self.hit

    def draw(self, surface):
        surface.fill(self.color, (self.location[0]-(self.size/2), self.location[1]-(self.size/2), self.size, self.size))

    def move(self):
        unit_location = self.target_unit.get_map_center()
        # find normalized direction vector (dx, dy) between enemy and player
        dx, dy = (self.location[0] - unit_location[0], self.location[1] - unit_location[1])
        dist = math.hypot(dx, dy)
        if dist != 0:
            dx, dy = dx / dist, dy / dist
        else:
            dx = dy = 0
        #if distance to move is greater than distance to player, set it to the player and
        #set hit to true.
        #TODO: implement a real distance function
        if (dist < 5):
            self.hit = True
            self.location[0] = unit_location[0]
            self.location[1] = unit_location[1]
        else:
            #otherwise, move along this normalized vector towards the player at current speed
            self.location[0] -= dx * self.speed
            self.location[1] -= dy * self.speed
