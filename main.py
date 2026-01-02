from pico2d import *
import game_framework
import start_mode
import test_mode
import game_data as gd


open_canvas(gd.WIDTH,gd.HEIGHT)
# game_framework.run(test_mode)
game_framework.run(start_mode)
close_canvas()

