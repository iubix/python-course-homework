'''
配置文件
'''
import pathlib
import sys

ALL_IO = pathlib.Path(__file__).parent.parent

sys.path.append(str(pathlib.Path(__file__).parent.parent))
# 游戏窗口大小（800*640）
SCREEN_SIZE = (SCREEN_WIGHT, SCREEN_HEIGHT) = (1100, 1000)

# 游戏中的块数排列（6行*10列）
GAME_SIZE = (GAME_ROW, GAME_COL) = (6, 10)

# 位置偏移量
BIAS = 200

# 连连看的总块数（60）
MAP_TOTAL = GAME_ROW * GAME_COL

# 定义元素个数（共8种图片）
ELE_NUM = 6
BG_COLOR = (230, 230, 240, 233)
TITLE = 'Caillo ~ '

#定义初始可点击次数
BASE_CLICKED = 10

#定义基础目标分数
BASE_TARGET_SCORE = 100

IMAGE_BG = ALL_IO / 'img' /  'basic' / 'bg.png' 
END_BG = ALL_IO / 'img' /  'basic' / 'end.png'
SUCCESS_BG = ALL_IO / 'img' /  'basic' / 'success.png'

MUSIC_START = ALL_IO / 'sound' / 'mp3' / 'start.mp3'
MUSIC_CLICK = ALL_IO / 'sound' / 'mp3' / 'click.common.button.mp3' 
MUSIC_ERROR = ALL_IO / 'sound' / 'mp3' / 'click.bubble.mp3' 
MUSIC_SUCCESS = ALL_IO / 'sound' / 'mp3' / 'amazing.mp3' 
MUSIC_END = ALL_IO / 'sound' / 'mp3' / 'end.mp3' 
# win_image = './images/win.png'
# lose_image = './images/lose.png'
GRID_SIZE = 70
SCALE_SIZE = (65, 65)
POINTS = []



import pathlib

BASE_PATH = pathlib.Path(__file__).parent.parent




import logging


"""
logging配置
"""

import os

# 1、定义三种日志输出格式，日志中可能用到的格式化串如下
# %(name)s Logger的名字
# %(levelno)s 数字形式的日志级别
# %(levelname)s 文本形式的日志级别
# %(pathname)s 调用日志输出函数的模块的完整路径名，可能没有
# %(filename)s 调用日志输出函数的模块的文件名
# %(module)s 调用日志输出函数的模块名
# %(funcName)s 调用日志输出函数的函数名
# %(lineno)d 调用日志输出函数的语句所在的代码行
# %(created)f 当前时间，用UNIX标准的表示时间的浮 点数表示
# %(relativeCreated)d 输出日志信息时的，自Logger创建以 来的毫秒数
# %(asctime)s 字符串形式的当前时间。默认格式是 “2003-07-08 16:49:45,896”。逗号后面的是毫秒
# %(thread)d 线程ID。可能没有
# %(threadName)s 线程名。可能没有
# %(process)d 进程ID。可能没有
# %(message)s用户输出的消息

# 2、强调：其中的%(name)s为getlogger时指定的名字
standard_format = '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]' \
                  '[%(levelname)s][%(message)s]'

simple_format = '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'

test_format = '%(asctime)s] %(message)s'

log_path = BASE_PATH / 'log' / 'match_3.log' 
# 3、日志配置字典
LOGGING_DIC = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': standard_format
        },
        'simple': {
            'format': simple_format
        },
        'test': {
            'format': test_format
        },
    },
    'filters': {},
    'handlers': {
        #打印到终端的日志
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',  # 打印到屏幕
            'formatter': 'simple'
        },
        #打印到文件的日志,收集info及以上的日志
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件,日志轮转
            'formatter': 'standard',
            # 可以定制日志文件路径
            # BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # log文件的目录
            # LOG_PATH = os.path.join(BASE_DIR,'a1.log')
            'filename': log_path,  # 日志文件
            'maxBytes': 1024*1024*5,  # 日志大小 5M
            'backupCount': 5,
            'encoding': 'utf-8',  # 日志文件的编码，再也不用担心中文log乱码了
        },
        'other': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',  # 保存到文件
            'formatter': 'test',
            'filename': log_path,
            'encoding': 'utf-8',
        },
    },
    'loggers': {
        #logging.getLogger(__name__)拿到的logger配置
        '': {
            'handlers': ['default', 'console'],  # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到屏幕
            'level': 'DEBUG', # loggers(第一层日志级别关限制)--->handlers(第二层日志级别关卡限制)
            'propagate': False,  # 默认为True，向上（更高level的logger）传递，通常设置为False即可，否则会一份日志向上层层传递
        },
        '专门的采集': {
            'handlers': ['other',],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}