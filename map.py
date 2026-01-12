# import json
# from pico2d import load_image
#
# TILE_SIZE = 32
#
# class TileMap:
#     def __init__(self, filename):
#         with open(filename, 'r', encoding='utf-8') as f:
#             data = json.load(f)
#
#         self.width = data['width']
#         self.height = data['height']
#         self.tilewidth = data['tilewidth']
#         self.tileheight = data['tileheight']
#
#         # 첫 번째 타일 레이어 (Terrain이라고 가정)
#         layer = data['layers'][0]
#         self.tiles = layer['data']
#
#         # 타일셋 이미지 로드
#         tileset = data['tilesets'][0]
#         self.tileset_image = load_image('images/tileset3.png')
#
#         self.columns = tileset['columns']
#
#     def draw(self, camera_x=0, camera_y=0):
#         for row in range(self.height):
#             for col in range(self.width):
#                 tile_id = self.tiles[row * self.width + col]
#                 if tile_id == 0:
#                     continue
#
#                 tile_index = tile_id - 1
#                 sx = (tile_index % self.columns) * self.tilewidth
#                 sy = (self.tileset_image.h -
#                       (tile_index // self.columns + 1) * self.tileheight)
#
#                 x = col * self.tilewidth - camera_x
#                 y = (self.height - row - 1) * self.tileheight - camera_y
#
#                 self.tileset_image.clip_draw(
#                     sx, sy,
#                     self.tilewidth, self.tileheight,
#                     x + self.tilewidth // 2,
#                     y + self.tileheight // 2
#                 )

#===============================================================
# import json
# from pico2d import load_image
#
# class TileMap:
#     def __init__(self, filename):
#         with open(filename, 'r', encoding='utf-8') as f:
#             data = json.load(f)
#
#         self.width = data['width']
#         self.height = data['height']
#         self.tilewidth = data['tilewidth']
#         self.tileheight = data['tileheight']
#
#         # 첫 번째 타일 레이어 사용 (Terrain 가정)
#         layer = data['layers'][0]
#         self.tiles = layer['data']
#
#         # ⭐ 여러 tileset 로드
#         self.tilesets = []
#         for ts in data['tilesets']:
#             tileset = {
#                 'firstgid': ts['firstgid'],
#                 'tilewidth': ts['tilewidth'],
#                 'tileheight': ts['tileheight'],
#                 'columns': ts['columns'],
#                 'image': load_image('map/' + ts['image'])
#             }
#             self.tilesets.append(tileset)
#
#     # ⭐ tile_id가 속한 tileset 찾기
#     def find_tileset(self, tile_id):
#         for ts in reversed(self.tilesets):
#             if tile_id >= ts['firstgid']:
#                 return ts
#         return None
#
#     def draw(self, camera_x=0, camera_y=0):
#         for row in range(self.height):
#             for col in range(self.width):
#                 tile_id = self.tiles[row * self.width + col]
#                 if tile_id == 0:
#                     continue
#
#                 ts = self.find_tileset(tile_id)
#                 local_id = tile_id - ts['firstgid']
#
#                 sx = (local_id % ts['columns']) * ts['tilewidth']
#                 sy = (ts['image'].h -
#                       (local_id // ts['columns'] + 1) * ts['tileheight'])
#
#                 x = col * ts['tilewidth'] - camera_x
#                 y = (self.height - row - 1) * ts['tileheight'] - camera_y
#
#                 ts['image'].clip_draw(
#                     sx, sy,
#                     ts['tilewidth'], ts['tileheight'],
#                     x + ts['tilewidth'] // 2,
#                     y + ts['tileheight'] // 2
#                 )
import json
from pico2d import load_image


class TileMap:
    def __init__(self, json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 맵 기본 정보
        self.width = data['width']
        self.height = data['height']
        self.tile_w = data['tilewidth']
        self.tile_h = data['tileheight']

        # =========================
        # 1️⃣ 타일셋 로드 (여러 개)
        # =========================
        self.tilesets = []
        for ts in data['tilesets']:
            image = load_image('map/' + ts['image'])
            tileset = {
                'firstgid': ts['firstgid'],
                'tilewidth': ts['tilewidth'],
                'tileheight': ts['tileheight'],
                'columns': ts['columns'],
                'image': image
            }
            self.tilesets.append(tileset)

        # =========================
        # 2️⃣ 레이어 로드 (이름 → data)
        # =========================
        self.layers = {}
        for layer in data['layers']:
            if layer['type'] != 'tilelayer':
                continue
            self.layers[layer['name']] = layer['data']

    # =========================
    # 내부 유틸
    # =========================
    def _find_tileset(self, tile_id):
        for ts in reversed(self.tilesets):
            if tile_id >= ts['firstgid']:
                return ts
        return None

    # =========================
    # 3️⃣ 레이어 그리기
    # =========================
    def draw(self, layer_name, camera_x=0, camera_y=0):
        if layer_name not in self.layers:
            return

        tiles = self.layers[layer_name]

        for row in range(self.height):
            for col in range(self.width):
                index = row * self.width + col
                tile_id = tiles[index]
                if tile_id == 0:
                    continue

                ts = self._find_tileset(tile_id)
                if not ts:
                    continue

                local_id = tile_id - ts['firstgid']
                tw, th = ts['tilewidth'], ts['tileheight']
                cols = ts['columns']

                sx = (local_id % cols) * tw
                sy = ts['image'].h - (local_id // cols + 1) * th

                x = col * tw - camera_x
                y = (self.height - row - 1) * th - camera_y

                ts['image'].clip_draw(
                    sx, sy, tw, th,
                    x + tw // 2, y + th // 2
                )

    # =========================
    # 4️⃣ 땅 판별 (ground 레이어)
    # =========================
    def is_ground_tile(self, tile_x, tile_y):
        ground = self.layers.get('ground')
        if not ground:
            return False

        if tile_x < 0 or tile_x >= self.width:
            return False
        if tile_y < 0 or tile_y >= self.height:
            return False

        index = tile_y * self.width + tile_x
        return ground[index] != 0

    # =========================
    # 5️⃣ 월드 좌표 기준 바닥 y 찾기
    # =========================
    def get_ground_y(self, world_x, world_y):
        tile_x = int(world_x // self.tile_w)
        tile_y = int(world_y // self.tile_h)

        # 월드 y → tiled row
        row = self.height - 1 - tile_y

        for r in range(row, self.height):
            index = r * self.width + tile_x
            if self.layers['ground'][index] != 0:
                # 타일 윗면 y 반환
                ground_tile_y = self.height - r
                return ground_tile_y * self.tile_h

        return None

    def has_ground_below(self, world_x, feet_y):
        tile_x = int(world_x // self.tile_w)
        tile_y = int(feet_y // self.tile_h) - 1  # 🔥 바로 아래 한 칸

        if tile_x < 0 or tile_x >= self.width:
            return False
        if tile_y < 0 or tile_y >= self.height:
            return False

        # tiled row 변환
        row = self.height - 1 - tile_y
        index = row * self.width + tile_x

        return self.layers['ground'][index] != 0

    def is_wall(self, world_x, world_y):
        tile_x = int(world_x // self.tile_w)
        tile_y = int(world_y // self.tile_h)

        if tile_x < 0 or tile_x >= self.width:
            return True
        if tile_y < 0 or tile_y >= self.height:
            return True

        row = self.height - 1 - tile_y
        index = row * self.width + tile_x

        return self.layers['ground'][index] !=0