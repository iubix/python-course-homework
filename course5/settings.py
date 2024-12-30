'''
配置文件
'''
import pathlib
import sys
sys.path.append(str(pathlib.Path(__file__).parent.parent))


SCREEN_SIZE = (SCREEN_WIGHT, SCREEN_HEIGHT) = (1000, 1000)


GAME_SIZE = (GAME_ROW, GAME_COL) = (6, 6)

# 位置偏移量
BIAS = 200

# 总块数（36）
MAP_TOTAL = GAME_ROW * GAME_COL


BG_COLOR = (230, 230, 240, 233)
TITLE = 'Caillo ~ '

GRID_SIZE = 100
SCALE_SIZE = (96, 96)
POINTS = []