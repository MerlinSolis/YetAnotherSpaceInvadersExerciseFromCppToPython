from raylib import *
from pyray import *

class Block:
    def __init__(self,position):
        self.position = position
        self.size = Vector2(3,3)
        self.active = True

    def get_rect(self):
        col_rec = Rectangle(self.position.x,self.position.y,self.size.x,self.size.y)
        return col_rec

    def draw(self):
        draw_rectangle_v(self.position,self.size,Color(243,216,63,255))

