from pyray import *
from raylib import *
from laser import Laser



class Spaceship:
    def __init__(self,image,position,x_speed):
        self.image = image
        self.position = position
        self.x_speed = x_speed
        self.direction = 0
        self.laser_list = []
        self.last_fire_time = 0
        self.laser_fire_interval = 0.35
        

    def get_rect(self):
        col_rect = Rectangle(self.position.x,self.position.y,self.image.width,self.image.height)
        return col_rect

    def fire_laser(self,laser_sound):
        current_time = get_time()
        if current_time >= self.last_fire_time + self.laser_fire_interval:
            play_sound(laser_sound)
            self.laser_list.append(Laser(Vector2(self.position.x + self.image.width/2,self.position.y),-700))
            self.last_fire_time = get_time()

    def move_right(self):
        self.direction = 1

    def move_left(self):
        self.direction = -1

    def neutral_center(self):
        self.direction = 0

    def update(self,delta_time):
        self.position.x += self.x_speed * self.direction * delta_time

        if self.position.x < 25:
            self.position.x = 25

        if self.position.x > get_screen_width() - self.image.width - 25:
            self.position.x = get_screen_width() - self.image.width - 25


    def draw(self):
        draw_texture_v(self.image,self.position,WHITE)

    def reset(self):
        self.position.x = get_screen_width()/2 - self.image.width/2
        self.position.y = get_screen_height() - self.image.height - 100
        self.laser_list.clear()