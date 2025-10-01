from pyray import * 
from raylib import *


class Laser:
    def __init__(self,position,speed):
        self.position = position
        self.width = 4
        self.height = 15
        # self.rect = Rectangle(self.position.x,self.position.y,self.width,self.height)
        self.speed = speed
        self.yellow = Color(243,216,63,255)
        self.active = True

    def get_rect(self):
        col_rec = Rectangle(self.position.x,self.position.y,self.width,self.height)
        return col_rec


    def update(self,delta_time):

        self.position.y += self.speed * delta_time

        if(self.position.y > get_screen_height() - 100 or self.position.y < 25):
            self.active = False

        # print(self.active)

        # self.rect.x = self.position.x
        # self.rect.y = self.position.y


    def draw(self):
        # draw_rectangle_rec(self.rect,self.yellow)
        if self.active:
            draw_rectangle_v(self.position,Vector2(self.width,self.height),self.yellow)