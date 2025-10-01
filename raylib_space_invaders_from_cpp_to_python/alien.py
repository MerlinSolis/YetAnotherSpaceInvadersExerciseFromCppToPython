from pyray import *
from raylib import *
# from os.path import join

class Alien:
    def __init__(self,type,position,image_list):
        self.type = type
        self.position = position
        self.image_list = image_list
        self.image = self.image_list[self.type-1]
        self.x_speed = 60
        self.active = True

    def get_rect(self):
        col_rec = Rectangle(self.position.x,self.position.y,self.image.width,self.image.height)
        return col_rec

    def update(self,delta_time,direction):
        self.position.x += direction * self.x_speed * delta_time


    def draw(self):
        draw_texture_v(self.image,self.position,WHITE)


    def unload_images(self):
        unload_texture(self.image)
        for image in self.image_list:
            unload_texture(image)

