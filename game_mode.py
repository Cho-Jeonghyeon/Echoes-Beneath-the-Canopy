from pico2d import *
import game_framework
from player import Player
from map import TileMap
import game_data as gd
player = None
tile_map = None
background_images = []

def init():
    global player, tile_map
    global background_images

    background_images = [
        load_image('images/outside_background_00.png'),  # 가장 먼 배경
        load_image('images/outside_background_01.png'),
        load_image('images/outside_background_02.png'),
        load_image('images/outside_background_03.png')  # 가장 앞 배경
    ]
    tile_map = TileMap('map/lils.json')
    # tile_map = TileMap('map/real_map.json')
    player = Player(tile_map)


def finish():
    global player, tile_map
    del player, tile_map
    global background_images
    background_images.clear()
    close_canvas()

def update():
    player.update()


def draw():
    clear_canvas()
    cx = get_canvas_width() // 2
    cy = get_canvas_height() // 2

    # 1️⃣ 배경 4장 순서대로 그리기
    for img in background_images:
        img.draw(cx, cy, gd.WIDTH, gd.HEIGHT)

    tile_map.draw('background', 0, 0)
    tile_map.draw('ground', 0, 0)

    player.draw()

    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            # ★ 핵심: 입력을 Player에게 전달
            player.handle_event(event)

def pause():
    pass

def resume():
    pass
