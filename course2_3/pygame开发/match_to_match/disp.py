'''
视图文件
'''

from conf import settings
import sys, time
import math, random
import threading
import pygame
from pygame.locals import *
import logging.config, logging

#记录日志
def get_logger(log_type):
    logging.config.dictConfig(settings.LOGGING_DIC)

    logger = logging.getLogger(log_type)
    
    return logger

#渲染窗口
def create_screen(screen_size):
    screen = pygame.display.set_mode(screen_size, 0,0)
    
    return screen


#构建图片布局
def built_map():
    
    list_img = []
    
    for i in range(0, settings.MAP_TOTAL, 2):
        ele = random.randint(1, 8)
        list_img.append(ele)
        list_img.append(ele)
    random.shuffle(list_img)
    
    return list_img


#定义图片按钮类
class imagBtn:

    _checkable = True
    _checked = False

    def __init__(self, screen, imag_io, x, y, num, icon_num) -> None:
        self.screen = screen
        self.x = x
        self.y = y
        #第几个元素(1~80)
        self.num = num
        self.vairnum = num
        #图片编号(1~8)
        self.icon_num = icon_num

        #缩放图片
        self.image = pygame.transform.scale(pygame.image.load(imag_io), settings.SCALE_SIZE)
    #描边
    def display_rect(self):
        
        if self._checked:
            pygame.draw.rect(self.image, [0,233,233], (0,0, settings.SCALE_SIZE[0] - 1, settings.SCALE_SIZE[1] - 1), 2)
        self.screen.blit(self.image, (self.x, self.y))

    def hide(self):
        self._checked = False
        self._checkable = False

        self.image.fill([255, 255, 255])

    def reset(self):
        self._checked = False
        # self.screen.blit(self.image, (self.x, self.y))
    
    def click(self):
        self._checked = not self._checked
        return self._checked
    
    def is_checkable(self):
        return self._checkable