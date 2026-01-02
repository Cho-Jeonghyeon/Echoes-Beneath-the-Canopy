from pico2d import *
import game_framework
import game_world
import game_data as gd
import random
import math


class Background_forest:
    image = None
    def __init__(self):
        if Background_forest.image == None:
            Background_forest.image = load_image('images/start_forest.png')
        self.x = gd.WIDTH / 2
        self.y = gd.HEIGHT / 2
        self.w = gd.WIDTH
        self.h = gd.HEIGHT

    def update(self):
        pass

    def draw(self):
        Background_forest.image.draw(self.x, self.y, self.w, self.h)

class Background_sky:
    image = None

    def __init__(self):
        if Background_sky.image is None:
            Background_sky.image = load_image('images/start_sky.png')

        self.w = self.image.w
        self.h = self.image.h

        self.y = gd.HEIGHT // 2 + 150
        self.speed = 40

        # ⭐ 하나의 offset만 관리
        self.offset = 0.0


    def update(self):
        dt = game_framework.frame_time

        # 계속 감소
        self.offset -= self.speed * dt

        # ⭐ modulo로 자연스럽게 반복
        self.offset %= self.w


    def draw(self):
        # offset 기준으로 두 장을 연속해서 그림
        x1 = -self.offset
        x2 = x1 + self.w

        self.image.draw(int(x1 + self.w // 2), self.y)
        self.image.draw(int(x2 + self.w // 2), self.y)

class StartLogo:
    def __init__(self):
        self.image = load_image('images/name.png')
        self.x = get_canvas_width() // 2
        self.y = get_canvas_height() // 2 + 100
        self.w = self.image.w - 140
        self.h = self.image.h - 80

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, self.y, self.w, self.h)

class Startpress:
    def __init__(self):
        self.image = load_image('images/press_start.png')
        self.x = get_canvas_width() // 2
        self.y = get_canvas_height() // 2 - 200

        self.base_w = self.image.w + 50
        self.base_h = self.image.h + 10

        self.time = 0.0   # 애니메이션 시간

    def update(self):
        # 프레임 시간 누적
        self.time += game_framework.frame_time

    def draw(self):
        # ⭐ 사인파 기반 펄스
        scale = 1.0 + 0.05 * math.sin(self.time * 3.0)
        alpha = 0.6 + 0.4 * math.sin(self.time * 3.0)

        w = self.base_w * scale
        h = self.base_h * scale

        # pico2d에는 alpha 직접 설정이 없으므로
        # 크기 변화만으로도 충분히 hover 느낌 남
        self.image.draw(self.x, self.y, w, h)

class Lantern:
    def __init__(self, x, y, scale=1.0):
        self.image = load_image('images/lantern1.png')

        # 🔥 스프라이트 시트 정보
        self.cols = 7
        self.rows = 6
        self.total_frames = 38

        self.frame_w = self.image.w // self.cols
        self.frame_h = self.image.h // self.rows

        # 🔥 위치
        self.x = x
        self.y = y

        # 🔥 크기 조절 (★ 여기!)
        self.scale = scale

        # 🔥 프레임 관련
        self.frame = random.randint(0, self.total_frames - 1)  # 랜덤 시작
        self.frame_time = 0.0
        self.frame_interval = 0.10  # 불빛 깜빡임 속도

        # 🔥 흔들림용
        self.swing_time = random.uniform(0, 4)

    def update(self):
        dt = game_framework.frame_time

        # 프레임 애니메이션
        self.frame_time += dt
        if self.frame_time >= self.frame_interval:
            self.frame = (self.frame + 1) % self.total_frames
            self.frame_time = 0.0

        # 흔들림 시간 누적
        self.swing_time += dt

    def draw(self):
        # 🔥 프레임 → (col, row) 계산
        col = self.frame % self.cols
        row = self.frame // self.cols

        # 🔥 미세 흔들림 (위아래)
        sway_y = 2 * math.sin(self.swing_time * 3.0)

        # 🔥 크기 조절된 draw 크기
        draw_w = self.frame_w * self.scale
        draw_h = self.frame_h * self.scale

        self.image.clip_draw(
            col * self.frame_w,
            (self.rows - 1 - row) * self.frame_h,  # pico2d는 아래가 0
            self.frame_w,
            self.frame_h,
            self.x,
            self.y + sway_y,
            draw_w,
            draw_h
        )


ground = None
player = None

from pico2d import *
import game_framework


class Player:
    def __init__(self, x, y, scale=1.0):
        # 🔥 달리기 프레임 로드 (순서 중요)
        self.run_images = [
            load_image('warrior/Run/Warrior_Run_1.png'),
            load_image('warrior/Run/Warrior_Run_2.png'),
            load_image('warrior/Run/Warrior_Run_3.png'),
            load_image('warrior/Run/Warrior_Run_4.png'),
            load_image('warrior/Run/Warrior_Run_5.png'),
            load_image('warrior/Run/Warrior_Run_6.png'),
            load_image('warrior/Run/Warrior_Run_7.png'),
            load_image('warrior/Run/Warrior_Run_8.png'),
        ]

        self.frame_count = len(self.run_images)
        self.frame = 0

        # 위치
        self.x = x
        self.y = y

        # 크기
        self.scale = scale

        # 애니메이션 타이밍
        self.frame_time = 0.0
        self.frame_interval = 0.08  # 작을수록 빨리 달림

        # 이동
        self.speed = 200  # px/sec
        self.dir = 1      # 1: 오른쪽, -1: 왼쪽

    def update(self):
        dt = game_framework.frame_time

        # ▶ 달리기 애니메이션
        self.frame_time += dt
        if self.frame_time >= self.frame_interval:
            self.frame = (self.frame + 1) % self.frame_count
            self.frame_time = 0.0

        self.x += self.speed * self.dir * dt
        if(self.x > gd.WIDTH//2 + 300):
            self.x -= 600
    def draw(self):
        img = self.run_images[self.frame]

        w = img.w * self.scale
        h = img.h * self.scale

        img.draw(self.x, self.y, w, h)


def init():
    global ground, player
    ground = load_image('images/ground.png')
    player = Player(gd.WIDTH // 2 - 150, 90, scale=2.2)

    game_world.add_object(player, 0)
def finish():
    pass

def update():
    game_world.update()

def draw():

    clear_canvas()

    ground.draw(gd.WIDTH//2, 30, 600, 90)

    game_world.render()
    update_canvas()

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            pass

def pause():
    pass

def resume():
    pass
