# from pico2d import *
# import game_framework
# from state_machine import StateMachine
#
# # =========================
# # 이벤트 체크 함수 (의미 이벤트)
# # =========================
# def event_run(e):
#     return e[0] == 'RUN'
#
# def event_stop(e):
#     return e[0] == 'STOP'
#
# def space_down(e):
#     return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE
#
# def event_turn(e):
#     return e[0] == 'TURN'
#
# # =========================
# # 상태: Idle
# # =========================
# class Idle:
#     def __init__(self, player):
#         self.player = player
#
#     def enter(self, e):
#         self.player.frame = 0
#         self.player.dir = 0
#         if e[0] == 'STOP' and e[1] is not None:
#             self.player.face_dir = e[1]
#
#     def exit(self, e):
#         pass
#
#     def do(self):
#         self.player.frame = (
#             self.player.frame
#             + self.player.idle_fps * game_framework.frame_time
#         ) % self.player.idle_frames
#
#     def draw(self):
#         img = self.player.idle_images[int(self.player.frame)]
#         self.player.draw_image(img)
#
#
# # =========================
# # 상태: Run
# # =========================
# class Run:
#     def __init__(self, player):
#         self.player = player
#
#     def enter(self, e):
#         self.player.frame = 0
#         if self.player.xdir != 0:
#             self.player.face_dir = self.player.xdir
#
#     def exit(self, e):
#         pass
#
#     def do(self):
#         self.player.frame = (
#             self.player.frame
#             + self.player.run_fps * game_framework.frame_time
#         ) % self.player.run_frames
#
#         self.player.x += self.player.xdir * self.player.speed * game_framework.frame_time
#         self.player.y += self.player.ydir * self.player.speed * game_framework.frame_time
#
#     def draw(self):
#         img = self.player.run_images[int(self.player.frame)]
#         self.player.draw_image(img)
#
#
# # =========================
# # Player
# # =========================
# class Player:
#     def __init__(self):
#         # 위치
#         self.x, self.y = 200, 120
#
#         # 방향 누적 데이터
#         self.xdir, self.ydir = 0, 0
#         self.dir = 0
#         self.face_dir = 1
#
#         # 이동 속도 (pixel/sec)
#         self.speed = 200
#
#         # 애니메이션
#         self.frame = 0
#         self.idle_images = [
#             load_image(f'warrior/Idle/Warrior_Idle_{i}.png') for i in range(1, 7)
#         ]
#         self.run_images = [
#             load_image(f'warrior/Run/Warrior_Run_{i}.png') for i in range(1, 9)
#         ]
#
#         self.idle_frames = len(self.idle_images)
#         self.run_frames = len(self.run_images)
#
#         self.idle_fps = 6
#         self.run_fps = 10
#
#         # 상태 생성
#         self.IDLE = Idle(self)
#         self.RUN = Run(self)
#
#         self.state_machine = StateMachine(
#             self.IDLE,
#             {
#                 self.IDLE: { event_run: self.RUN },
#                 self.RUN:  { event_stop: self.IDLE }
#             }
#         )
#
#     # =========================
#     # 입력 처리 (교수님 핵심 구조)
#     # =========================
#     def handle_event(self, event):
#         # 방향키 처리
#         if event.key in (SDLK_LEFT, SDLK_RIGHT, SDLK_UP, SDLK_DOWN):
#             cur_xdir, cur_ydir = self.xdir, self.ydir
#
#             if event.type == SDL_KEYDOWN:
#                 if event.key == SDLK_LEFT:   self.xdir -= 1
#                 elif event.key == SDLK_RIGHT:self.xdir += 1
#                 elif event.key == SDLK_UP:   self.ydir += 1
#                 elif event.key == SDLK_DOWN: self.ydir -= 1
#
#             elif event.type == SDL_KEYUP:
#                 if event.key == SDLK_LEFT:   self.xdir += 1
#                 elif event.key == SDLK_RIGHT:self.xdir -= 1
#                 elif event.key == SDLK_UP:   self.ydir -= 1
#                 elif event.key == SDLK_DOWN: self.ydir += 1
#
#             # ⭐ 이동 상태 변화 감지
#             if cur_xdir != self.xdir or cur_ydir != self.ydir:
#                 if self.xdir == 0 and self.ydir == 0:
#                     self.state_machine.handle_state_event(
#                         ('STOP', self.face_dir)
#                     )
#                 else:
#                     self.state_machine.handle_state_event(
#                         ('RUN', None)
#                     )
#
#         # 그 외 입력은 FSM으로 전달
#         else:
#             self.state_machine.handle_state_event(('INPUT', event))
#
#     def update(self):
#         self.state_machine.update()
#
#     def draw(self):
#         self.state_machine.draw()
#
#     # =========================
#     # 공통 렌더링
#     # =========================
#     def draw_image(self, img):
#         if self.face_dir == 1:
#             img.draw(self.x, self.y,120,80)
#         else:
#             img.clip_composite_draw(
#                 0, 0, img.w, img.h,
#                 0, 'h',
#                 self.x, self.y,
#                 120, 80
#             )
from pico2d import *
import game_framework

from state_machine import StateMachine

# =====================
# 상수
# =====================
DRAW_SCALE = 4

# =====================
# 상태 이벤트 판별
# =====================
def event_run(e):   return e[0] == 'RUN'
def event_stop(e):  return e[0] == 'STOP'
def event_attack(e): return e[0] == 'ATTACK'
def event_jump(e):  return e[0] == 'JUMP'

# =====================
# 상태 클래스
# =====================
class Idle:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        self.player.frame = 0
        self.player.frame_w = 16
        self.player.frame_h = 16
    def exit(self, e):
        pass

    def do(self):
        self.player.frame = (
            self.player.frame
            + self.player.idle_fps * game_framework.frame_time
        ) % self.player.idle_frames

    def draw(self):
        self.player.draw_current_frame(self.player.idle_image)


class Run:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        self.player.frame = 0
        self.player.frame_w = 16
        self.player.frame_h = 16
    def exit(self, e):
        pass

    def do(self):
        # self.player.x += (
        #     self.player.xdir
        #     * self.player.speed
        #     * game_framework.frame_time
        # )

        self.player.frame = (
            self.player.frame
            + self.player.run_fps * game_framework.frame_time
        ) % self.player.run_frames

    def draw(self):
        self.player.draw_current_frame(self.player.run_image)


class Attack:
    def __init__(self, player):
        self.player = player

    def enter(self, e):

        self.player.frame = 0
        self.player.is_attacking = True
        self.player.frame_w = 32  # ← 중요
        self.player.frame_h = 16

        self.player.render_offset_x = 32 * self.player.face_dir

    def exit(self, e):

        self.player.is_attacking = False
        self.player.render_offset_x = 0

    def do(self):
        self.player.frame += (
            self.player.attack_fps * game_framework.frame_time
        )

        # ⭐ 애니메이션 끝나면 자동 종료 (후딜 포함)
        if self.player.frame >= self.player.attack_frames:
            self.player.state_machine.handle_state_event(('STOP', None))

    def draw(self):
        self.player.draw_current_frame(self.player.attack_image)


class Jump:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        # 점프 시작
        self.player.vy = self.player.jump_power
        self.player.on_ground = False

        self.player.frame = 0
        self.player.frame_w = 16
        self.player.frame_h = 16

    def exit(self, e):
        pass

    def do(self):
        if not self.player.is_attacking:
            self.player.frame = (
                self.player.frame
                + self.player.jump_fps * game_framework.frame_time
                ) % self.player.jump_frames
        else:
            self.player.frame = (
                self.player.frame
                + self.player.attack_fps * game_framework.frame_time
                ) % self.player.attack_frames

    def draw(self):
        if self.player.is_attacking:
            self.player.draw_current_frame(self.player.attack_image)
        else:
            self.player.draw_current_frame(self.player.jump_image)
# =====================
# Player 클래스
# =====================
class Player:
    def __init__(self, tile_map, x=400, y=222):

        self.x, self.y = x, y
        self.tile_map = tile_map

        # 점프 물리
        self.vy = 0
        self.gravity = -1800
        self.jump_power = 700
        self.on_ground = True

        self.frame_w = 16
        self.frame_h = 16

        #attack1 render offset
        self.render_offset_x = 0
        self.render_offset_y = 0

        # 방향 입력
        self.left_pressed = False
        self.right_pressed = False
        self.attack_pressed = False

        self.xdir = 0        #
        self.face_dir = 1    # 1: 오른쪽, -1: 왼쪽

        # 이동
        self.speed = 200

        # 프레임
        self.frame = 0

        # 애니메이션 설정
        self.idle_frames = 6
        self.run_frames = 8
        self.attack_frames = 7
        self.jump_frames = 3

        self.idle_fps = 6
        self.run_fps = 10
        self.attack_fps = 20
        self.jump_fps = 6

        # 이미지 로드
        self.idle_image = load_image('images/idle_right.png')
        self.run_image  = load_image('images/run_right.png')
        self.attack_image = load_image('images/attack1_right.png')
        self.jump_image = load_image('images/jump_right.png')
        self.is_attacking = False

        # 상태 객체
        self.IDLE = Idle(self)
        self.RUN  = Run(self)
        self.ATTACK = Attack(self)
        self.JUMP = Jump(self)

        # 상태 머신
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {
                    event_run: self.RUN,
                    event_attack: self.ATTACK,
                    event_jump: self.JUMP
                },
                self.RUN: {
                    event_stop: self.IDLE,
                    event_attack: self.ATTACK,
                    event_jump: self.JUMP

                },
                self.JUMP: {
                    event_stop: self.IDLE
                },
                self.ATTACK: {
                    event_stop: self.IDLE
                }
            }
        )

    def get_bbox(self):
        half_w = (self.frame_w * DRAW_SCALE) / 2
        half_h = (self.frame_h * DRAW_SCALE) / 2

        left = self.x - half_w
        right = self.x + half_w
        bottom = self.y - half_h
        top = self.y + half_h

        return left, bottom, right, top

    # =====================
    # 입력 처리
    # =====================
    def handle_event(self, event):

        # 공격 키
        if event.type == SDL_KEYDOWN and event.key == SDLK_z:
            self.attack_pressed = True
            return

        # 점프 키
        if event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            if self.on_ground and not self.is_attacking:
                self.state_machine.handle_state_event(('JUMP', None))
            return

        # 키 상태만 기록
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_LEFT:
                self.left_pressed = True
            elif event.key == SDLK_RIGHT:
                self.right_pressed = True

        elif event.type == SDL_KEYUP:
            if event.key == SDLK_LEFT:
                self.left_pressed = False
            elif event.key == SDLK_RIGHT:
                self.right_pressed = False

    # =====================
    # 업데이트 / 드로우
    # =====================
    def update(self):

        self.state_machine.update()

        if self.xdir != 0 and self.state_machine.cur_state == self.IDLE:
            self.state_machine.handle_state_event(('RUN', None))

        #낭떠러지 처리(점프안했을떄)
        left, bottom, right, top = self.get_bbox()
        player_feet_y = bottom

        if self.on_ground:
            has_ground = self.tile_map.has_ground_below(self.x, player_feet_y)
            if not has_ground:
                self.on_ground = False
                print("낭떠러지!")
                # vy는 0에서 시작 → 자연 낙하

        #점프 후 낙하 처리
        if not self.on_ground:
            prev_y = self.y

            self.vy += self.gravity * game_framework.frame_time
            self.y += self.vy * game_framework.frame_time

            player_feet_y = self.y - (self.frame_h * DRAW_SCALE) / 2
            ground_y = self.tile_map.get_ground_y(self.x, player_feet_y)
            prev_feet_y = prev_y - (self.frame_h * DRAW_SCALE) / 2

            print(
                f"vy={self.vy:.2f}, "
                f"prev_feet_y={prev_feet_y:.2f}, "
                f"feet_y={player_feet_y:.2f}, "
                f"ground_y={ground_y}"
            )
            if (
                    ground_y is not None
                    and self.vy <= 0
                    and prev_feet_y >= ground_y >= player_feet_y
            ):
                print("착지!")
                self.y = ground_y + (self.frame_h * DRAW_SCALE) / 2
                self.vy = 0
                self.on_ground = True

                # 공중 공격 중이면 정리
                if self.is_attacking:
                    self.is_attacking = False
                    self.render_offset_x = 0

                self.state_machine.handle_state_event(('STOP', None))

        # =====================
        # 1️⃣ 공격 우선 처리
        # =====================
        if self.attack_pressed and not self.is_attacking:
            if self.state_machine.cur_state == self.JUMP:
                # 🔥 공중 공격: 상태 전이 ❌
                self.is_attacking = True
                self.frame = 0
                self.frame_w = 32
                self.frame_h = 16
                self.render_offset_x = 32 * self.face_dir
            else:
                self.is_attacking = True
                self.xdir = 0
                self.state_machine.handle_state_event(('ATTACK', None))

            self.attack_pressed = False

            #self.xdir = 0  # 즉시 이동 차단

        prev_xdir = self.xdir

        # =====================
        # Key State → xdir 계산
        # =====================
        # if self.is_attacking:
        #     self.xdir = 0
        # else:
        #     if self.left_pressed and not self.right_pressed:
        #         self.xdir = -1
        #     elif self.right_pressed and not self.left_pressed:
        #         self.xdir = 1
        #     else:
        #         self.xdir = 0
        #
        #     self.x += self.xdir * self.speed * game_framework.frame_time
        # 입력으로 원하는 방향 계산
        if self.left_pressed and not self.right_pressed:
            desired_xdir = -1
        elif self.right_pressed and not self.left_pressed:
            desired_xdir = 1
        else:
            desired_xdir = 0

        # 공격 중에는 방향 "갱신"만 막음
        if not self.is_attacking:
            self.xdir = desired_xdir

        # 이동은 항상 적용
        self.x += self.xdir * self.speed * game_framework.frame_time

        # =====================
        # 상태 전이
        # =====================
        # 지상 상태에서만 이동 FSM 처리
        if self.state_machine.cur_state in (self.IDLE, self.RUN):
            if prev_xdir != self.xdir:
                if self.xdir == 0:
                    self.state_machine.handle_state_event(('STOP', None))
                else:
                    self.state_machine.handle_state_event(('RUN', None))

        # 바라보는 방향
        if self.xdir > 0:
            self.face_dir = 1
        elif self.xdir < 0:
            self.face_dir = -1



    def draw(self):
        self.state_machine.draw()

    # =====================
    # 프레임 렌더링
    # =====================
    def draw_current_frame(self, image):
        frame = int(self.frame)
        sx = frame * self.frame_w
        sy = 0
        draw_x = self.x + self.render_offset_x
        draw_y = self.y + self.render_offset_y

        if self.face_dir == 1:
            image.clip_draw(
                sx, sy,
                self.frame_w, self.frame_h,
                draw_x, draw_y,
                self.frame_w * DRAW_SCALE,
                self.frame_h * DRAW_SCALE
            )
        else:
            image.clip_composite_draw(
                sx, sy,
                self.frame_w, self.frame_h,
                0, 'h',
                draw_x, draw_y,
                self.frame_w * DRAW_SCALE,
                self.frame_h * DRAW_SCALE
            )

