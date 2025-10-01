from raylib import *
from pyray import *
import os
from os.path import join
from spaceship import Spaceship
from laser import Laser
from obstacle import Obstacle
from alien import Alien
from mysteryship import MysteryShip

class Game:
    def __init__(self):
        self.window_width = 750
        self.window_height = 700
        self.offset = 50
        self.app_title = "Space Invaders in Py Raylib"
        init_window(self.window_width + self.offset,self.window_height + self.offset*2,self.app_title)
        init_audio_device()
        self.fps_cap = 60
        set_target_fps(self.fps_cap)
        self.grey = Color(29,29,27,255)
        self.yellow = Color(243,216,63,255)
        self.score = 0
        self.level = 1
        self.highscore = 0
        self.load_highscore_from_file()

        self.font = load_font_ex(join("Font","monogram.ttf"),64,ffi.NULL,0)
        
        self.bgm = load_music_stream(join("Sounds","music.ogg"))
        set_music_volume(self.bgm,0.3)
        play_music_stream(self.bgm)
        self.laser_sound = load_sound(join("Sounds","laser.ogg"))
        self.explosion_sound = load_sound(join("Sounds","explosion.ogg"))

        self.mystery_ship_image = load_texture(join("Graphics","mystery.png"))
        self.mysteryship = MysteryShip(self.mystery_ship_image,180)

        self.spaceship_image = load_texture(join("Graphics","spaceship.png"))
        self.spaceship = Spaceship(self.spaceship_image,Vector2(get_screen_width()/2 - self.spaceship_image.width/2,
                                                                get_screen_height() - self.spaceship_image.height - 100),420)

        # self.laser = Laser(Vector2(self.window_width/2,self.window_height/2),-420)


        # self.obstacle = Obstacle(Vector2(self.window_width/2,self.window_height/2))
        self.obstacle_list = []
        self.create_obstacles()

        self.alien_image_list = []
        for alien_num in range(3):
            self.alien_image_list.append(load_texture(join("Graphics",f"alien_{alien_num+1}.png")))

        self.alien_laser_list = []
        self.alien_list = []
        self.create_aliens()

        self.alien_direction = 1
        self.last_alien_laser_fired_time = 0
        self.alien_laser_fire_interval = 0.35

        self.mystery_ship_spawn_time = 0
        self.mystery_ship_spawn_interval = get_random_value(10,20)
        
        self.player_lives = 3
        self.game_active = True

    def check_for_highscore(self):
        if self.score > self.highscore:
            self.highscore = self.score
            self.write_highscore_to_file()

    def load_highscore_from_file(self):
        # with open("highscore.txt","r") as f:
        #     try:
        #         self.highscore = int(f.read())
        #     except:
        #         self.highscore = 0
        if os.path.exists(join("highscore.txt")):
            with open(join("highscore.txt"),"r") as f:
                self.highscore = int(f.read())
        else:
            self.highscore = 0

    def write_highscore_to_file(self):
        with open(join("highscore.txt"),"w") as f:
            f.write(str(self.highscore))
        
    def format_with_leading_zeros(self,number,number_width):
        number_string = str(number)
        leading_zeros = int(number_width - len(number_string))
        number_string = leading_zeros * "0" + number_string
        return number_string   

    def check_for_collision(self):

        for laser in self.spaceship.laser_list:
            for alien in self.alien_list:
                if check_collision_recs(laser.get_rect(),alien.get_rect()):

                    if alien.type == 1:
                        self.score += 100
                    elif alien.type == 2:
                        self.score += 200
                    elif alien.type == 3:
                        self.score += 300

                    play_sound(self.explosion_sound)

                    alien.active = False
                    laser.active = False

            for obstacle in self.obstacle_list:
                if check_collision_recs(laser.get_rect(),obstacle.get_rect()):
                    for block in obstacle.blocks:
                        if check_collision_recs(laser.get_rect(),block.get_rect()):
                            laser.active = False
                            block.active = False

            if check_collision_recs(laser.get_rect(),self.mysteryship.get_rect()):
                play_sound(self.explosion_sound)
                self.score += 500
                laser.active = False
                self.mysteryship.alive = False

        
        # for alien in self.alien_list:
        #     for obstacle in self.obstacle_list:
        #         for block in obstacle.blocks:
        #             if check_collision_recs(alien.get_rect(),block.get_rect()):
        #                 block.active = False
        
        for alien in self.alien_list:
            for obstacle in self.obstacle_list:
                if check_collision_recs(alien.get_rect(),obstacle.get_rect()):
                    for block in obstacle.blocks:
                        if check_collision_recs(alien.get_rect(),block.get_rect()):
                            block.active = False

            
            if check_collision_recs(alien.get_rect(),self.spaceship.get_rect()):
                self.game_over()

        for laser in self.alien_laser_list:
            for obstacle in self.obstacle_list:
                if check_collision_recs(laser.get_rect(),obstacle.get_rect()):
                    for block in obstacle.blocks:
                        if check_collision_recs(laser.get_rect(),block.get_rect()):
                            # play_sound(self.explosion_sound)
                            laser.active = False
                            block.active = False
            if check_collision_recs(laser.get_rect(),self.spaceship.get_rect()):
                play_sound(self.explosion_sound)
                laser.active = False
                self.player_lives -= 1
                if(self.player_lives <= 0):
                    self.game_over()

                
    def game_over(self):
        self.game_active = False

    def handle_input(self):
        if is_key_down(KEY_RIGHT):
            self.spaceship.move_right()
        elif is_key_down(KEY_LEFT):
            self.spaceship.move_left()
        else:
            self.spaceship.neutral_center()

        if is_key_down(KEY_SPACE):
            self.spaceship.fire_laser(self.laser_sound)

    def delete_inactive_lasers(self):
        self.spaceship.laser_list = [laser for laser in self.spaceship.laser_list if laser.active]
        self.alien_laser_list = [laser for laser in self.alien_laser_list if laser.active]

    def delete_inactive_aliens(self):
        self.alien_list = [alien for alien in self.alien_list if alien.active]

    def delete_inactive_blocks(self):
        for obstacle in self.obstacle_list:
            obstacle.blocks = [block for block in obstacle.blocks if block.active]
    

    def update_lasers(self,delta_time):
        for laser in self.spaceship.laser_list:
            laser.update(delta_time)

        for laser in self.alien_laser_list:
            laser.update(delta_time)


    def draw_lasers(self):
        for laser in self.spaceship.laser_list:
            laser.draw()

        for laser in self.alien_laser_list:
            laser.draw()

    def draw_level_text(self):
        draw_text_ex(self.font,f"LEVEL{self.level}",Vector2(570,740),34,2,self.yellow)

    def draw_game_over_text(self):
        draw_text_ex(self.font,"GAME OVER",Vector2(570,740),34,2,self.yellow)

    def draw_score(self):
        draw_text_ex(self.font,"SCORE",Vector2(50,15),34,2,self.yellow)
        score_text = self.format_with_leading_zeros(self.score,5)
        draw_text_ex(self.font,score_text,Vector2(50,40),34,2,self.yellow)

    def draw_highscore(self):
        draw_text_ex(self.font,"HIGH-SCORE",Vector2(570,15),34,2,self.yellow)
        highscore_text = self.format_with_leading_zeros(self.highscore,5)
        draw_text_ex(self.font,highscore_text,Vector2(655,40),34,2,self.yellow)

    def reset(self):
        self.spaceship.reset()
        self.alien_list.clear()
        self.alien_laser_list.clear()
        self.obstacle_list.clear()

    def initialize(self):
        self.score = 0
        self.load_highscore_from_file()
        self.game_active = True
        self.create_obstacles()
        self.create_aliens()
        self.alien_direction = 1
        self.last_alien_fired_time = 0
        self.mystery_ship_spawn_time = 0
        self.mystery_ship_spawn_time_interval = get_random_value(10,20)
        self.player_lives = 3

    def next_level(self):
        self.reset()
        self.create_obstacles()
        self.create_aliens()
        self.alien_direction = 1
        self.last_alien_fired_time = 0
        self.mystery_ship_spawn_time = 0
        self.mystery_ship_spawn_time_interval = get_random_value(10,20)
        self.player_lives = 3
        self.level += 1


    def update(self):
        update_music_stream(self.bgm)
        if self.game_active:
            delta_time = get_frame_time()
            self.handle_input()
            self.spaceship.update(delta_time)
            # self.laser.update(delta_time)
            self.update_lasers(delta_time)

            

            
            self.move_aliens(delta_time)
            
            self.aliens_shoot_lasers()

            current_time = get_time()
            if(current_time >= self.mystery_ship_spawn_time + self.mystery_ship_spawn_interval):
                self.mysteryship.spawn()
                self.mystery_ship_spawn_time = get_time()
                self.mystery_ship_spawn_time_interval = get_random_value(0,10)

            self.mysteryship.update(delta_time)

            self.check_for_collision()
            self.delete_inactive_lasers()
            self.delete_inactive_aliens()
            self.delete_inactive_blocks()
            self.check_for_highscore()
            self.check_for_next_level()

            # print(len(self.spaceship.laser_list))
            # self.create_obstacles()
            # print(len(self.alien_image_list))
            # print(self.alien_image_list)
        else:
            if is_key_pressed(KEY_ENTER):
                self.reset()
                self.initialize()
    
    def check_for_next_level(self):
        if len(self.alien_list) == 0:
            self.next_level()

    def draw(self):
        begin_drawing()
        clear_background(self.grey)
        draw_rectangle_rounded_lines_ex(Rectangle(10,10,780,780),0.18,20,2,self.yellow)
        draw_line_ex(Vector2(25,730),Vector2(775,730),3,self.yellow)
        
        self.draw_lasers()
        self.spaceship.draw()
        self.draw_obstacles()
        self.draw_aliens()
        self.mysteryship.draw()
        self.draw_player_lives()
        self.draw_score()
        self.draw_highscore()

        if self.game_active:
            self.draw_level_text()
        else:
            self.draw_game_over_text()

        # self.laser.draw()

        # self.obstacle.draw()

        end_drawing()


    def run(self):
        while not window_should_close():
            self.update()
            self.draw()

        self.unload()
        close_audio_device()
        close_window()

    def draw_player_lives(self):
        for i in range(self.player_lives):
            x = 50 * i + 50
            y = 745
            draw_texture_v(self.spaceship_image,Vector2(x,y),WHITE)


    def create_obstacles(self):
        # print(len(Obstacle.grid))
        obstacle_width = len(Obstacle.grid[0]) * 3
        gap = (get_screen_width() - obstacle_width * 4)/5
        num_of_obstacles = 4
        for i in range(num_of_obstacles):
            offset_x = (i+1) * gap + i * obstacle_width
            self.obstacle_list.append(Obstacle(Vector2(offset_x,get_screen_height()-200)))


    def draw_obstacles(self):
        for obstacle in self.obstacle_list:
            obstacle.draw()

    def create_aliens(self):
        for row in range(5):
            for col in range(11):
                if row == 0:
                    alien_type = 3
                elif row == 1 or row == 2:
                    alien_type = 2
                else:
                    alien_type = 1

                x_offset = 75
                y_offset = 110
                cell_size = 55
                x = x_offset + col * cell_size
                y = y_offset + row * cell_size
                self.alien_list.append(Alien(alien_type,Vector2(x,y),self.alien_image_list))

    def draw_aliens(self):
        for alien in self.alien_list:
            alien.draw()

    def move_down_aliens(self,distance):
        for alien in self.alien_list:
            alien.position.y += distance


    def move_aliens(self,delta_time):
        for alien in self.alien_list:
            

            if alien.position.x + alien.image.width > get_screen_width() - 25:
                self.alien_direction = -1
                self.move_down_aliens(4)
            if alien.position.x < 25:
                self.alien_direction = 1
                self.move_down_aliens(4)


            alien.update(delta_time,self.alien_direction)

    def aliens_shoot_lasers(self):
        current_time = get_time()
        if (current_time >= self.last_alien_laser_fired_time + self.alien_laser_fire_interval) and len(self.alien_list) != 0:
            random_index = get_random_value(0,len(self.alien_list) - 1)
            alien = self.alien_list[random_index]
            self.alien_laser_list.append(Laser(Vector2(alien.position.x + alien.image.width/2,alien.position.y + alien.image.height),210))
            self.last_alien_laser_fired_time = get_time()




    def unload(self):
        unload_texture(self.spaceship_image)
        unload_texture(self.spaceship.image)

        for alien_image in self.alien_image_list:
            unload_texture(alien_image)

        for alien in self.alien_list:
            alien.unload_images()

        unload_sound(self.laser_sound)
        unload_sound(self.explosion_sound)
        unload_music_stream(self.bgm)
        





if __name__ == "__main__":
    game = Game()
    game.run()