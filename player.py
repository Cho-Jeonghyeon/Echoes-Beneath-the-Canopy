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

        left = self.x - half_w+5
        right = self.x + half_w-5
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

        dt = game_framework.frame_time
        self.state_machine.update()

        if self.xdir != 0 and self.state_machine.cur_state == self.IDLE:
            self.state_machine.handle_state_event(('RUN', None))

        # bbox/feet
        left, bottom, right, top = self.get_bbox()
        half_h = (self.frame_h * DRAW_SCALE) / 2
        feet_y = self.y - half_h


        # ---------------------------------
        # 1) 낭떠러지 체크 (on_ground일 때만)
        # ---------------------------------
        if self.on_ground:
            # 발 바로 아래 1px 지점이 solid가 아니면 낙하 시작
            if not self.tile_map.solid_down(self.x, feet_y - 1, vy=-1, prev_feet_y=feet_y):
                self.on_ground = False
                # 자연 낙하 시작 (vy 그대로 두거나 0으로)
                # self.vy = 0

        # ---------------------------------
        # 2) Y축 물리 + 착지 (get_ground_y 제거, solid_at으로 통합)
        # ---------------------------------
        prev_y = self.y
        prev_feet_y = prev_y - half_h

        if not self.on_ground:
            self.vy += self.gravity * dt
            self.y += self.vy * dt

            # 머리박기(진짜 땅만 천장으로 작동)
            if self.vy > 0:
                head_y = self.y + half_h
                if self.tile_map.solid_up(self.x, head_y):
                    # 머리가 들어간 타일의 바닥면으로 스냅
                    _, tile_y = self.tile_map.world_to_tile(self.x, head_y)
                    tile_bottom = tile_y * self.tile_map.tile_h
                    self.y = tile_bottom - half_h
                    self.vy = 0  # 상승 멈추고 낙하로 전환

            feet_y = self.y - half_h

            # print(
            #     f"vy={self.vy:.2f}, "
            #     f"prev_feet_y={prev_feet_y:.2f}, "
            #     f"feet_y={player_feet_y:.2f}, "
            #     f"ground_y={ground_y}"
            # )

            # 아래로 내려오는 중이고, 이번 프레임에서 solid를 "통과"했으면 착지
            if self.vy <= 0:
                # 현재 발 위치가 solid 안쪽이면(=바닥을 뚫고 들어갔으면) 착지 처리
                if self.tile_map.solid_down(self.x, feet_y, vy=self.vy, prev_feet_y=prev_feet_y):
                    # 착지 스냅: "현재 feet_y가 속한 타일의 윗면"으로 올려놓기
                    tile_x, tile_y = self.tile_map.world_to_tile(self.x, feet_y)
                    tile_top = (tile_y + 1) * self.tile_map.tile_h

                    self.y = tile_top + half_h
                    self.vy = 0
                    self.on_ground = True

                    # 공중 공격 중이면 정리
                    if self.is_attacking:
                        self.is_attacking = False
                        self.render_offset_x = 0

                    self.state_machine.handle_state_event(('STOP', None))


        # ---------------------------------
        # 3) X축 이동 + 충돌 (is_wall 제거, solid_at으로 통합)
        # ---------------------------------
        dx = self.xdir * self.speed * dt
        if dx != 0:
            left, bottom, right, top = self.get_bbox()
            check_x = right + dx if dx > 0 else left + dx

            blocked = False

            # 샘플링 3점(발/몸통/머리)
            for y in (bottom + 4, self.y, top - 4):
                if self.tile_map.solid_side(check_x, y):
                    blocked = True
                    break

            if not blocked:
                self.x += dx

        # ---------------------------------
        # 4) 공격 처리(기존 유지)
        # ---------------------------------
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

        # ---------------------------------
        # 5) Key State → xdir 계산(기존 유지)
        # ---------------------------------
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
        #self.x += self.xdir * self.speed * game_framework.frame_time

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
        draw_rectangle(*self.get_bbox())
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

