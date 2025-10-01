from pyray import *
from raylib import *


class MysteryShip:
    def __init__(self,image,speed):
        self.image = image
        self.position = Vector2()
        self.alive = False
        self.speed = speed

    def spawn(self):
        self.position.y = 90
        side = get_random_value(0,1)
        if side == 0:
            self.position.x = 25
            self.speed = abs(self.speed)
        elif side == 1:
            self.position.x = get_screen_width() - self.image.width - 25
            self.speed *= -1

        self.alive = True

    def update(self,delta_time):
        if self.alive:
            self.position.x += self.speed * delta_time
            if (self.position.x > get_screen_width() - self.image.width - 25) or (self.position.x < 25):
                self.alive = False


    def draw(self):
        if self.alive:
            draw_texture_v(self.image,self.position,WHITE)

    def get_rect(self):
        if self.alive:
            col_rec = Rectangle(self.position.x,self.position.y,self.image.width,self.image.height)
            return col_rec
        else:
            col_rec = Rectangle(self.position.x,self.position.y,0,0)
            return col_rec