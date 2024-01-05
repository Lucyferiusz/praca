# WIN_WIDTH = 1080
# WIN_HEIGHT = 950
TILESIZE = 32
FPS = 60

PLAYER_LAYER = 4
ENEMY_LAYER = 3
BLOCK_LAYER = 1
WATER_LAYER = 1



RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
from data.map_01 import * 
map_01 = MAP_01
# map_01 = MAP_02
# Wymiary mapy
map_width = len(MAP_01[0])
map_height = len(MAP_01)
total_tiles = map_width * map_height

print(f"{map_width=} {map_height=}")
