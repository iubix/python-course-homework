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
import pathlib

#记录日志
def get_logger(log_type):
    logging.config.dictConfig(settings.LOGGING_DIC)

    logger = logging.getLogger(log_type)
    
    return logger


#布局类
class Layout:

    def __init__(self) -> None:
        self.screen = None
        self.image_list = []
        self.map_list = []
        self.digist = []
        self.score = []
    
    #加载所有图片
    def display(self):
        self.image_list = []
        img_io = pathlib.Path(__file__).parent / 'img' / 'animal' / 'image'
        for i in range(0, settings.MAP_TOTAL):
            x = int(i % settings.GAME_COL) * settings.GRID_SIZE + (settings.GRID_SIZE - settings.SCALE_SIZE[0])/2
            y = int(i / settings.GAME_COL) * settings.GRID_SIZE + (settings.GRID_SIZE - settings.SCALE_SIZE[1])/2
            ele_io = str(img_io) + str(self.map_list[i]) + '.png'
            self.image_list.append(imagBtn(self.screen, ele_io, x + settings.BIAS , y + settings.BIAS, i, self.map_list[i]))
    
    #渲染窗口
    def _create_screen(self, screen_size):
        self.screen = pygame.display.set_mode(screen_size, 0,0)
        
        return self.screen

    #添加背景
    def _add_bg(self, screen, bg_io):
        bg = pygame.transform.scale(pygame.image.load(bg_io), settings.SCREEN_SIZE)
        screen.blit(bg, (0, 0))

    #构建图片布局
    def built_map(self):
        
        list_img = []
        
        for i in range(0, settings.MAP_TOTAL):
            ele = random.randint(1, 6)
            list_img.append(ele)
            # list_img.append(ele)
            # list_img.append(ele)
        random.shuffle(list_img)
        
        self.map_list = list_img
    
    #加载数字图片
    def load_digist(self):
        img_io = pathlib.Path(__file__).parent / 'img' / 'digist'
        for each in range(1,16):
        
            digist = pygame.transform.scale(pygame.image.load(str(img_io) + f'/{each}.png'), settings.SCALE_SIZE)
            self.digist.append(digist)
            
            # self.screen.blit(digist, (settings.SCREEN_SIZE[0] - settings.SCALE_SIZE[0] - 50, 30))
            
    def show_digist(self, num):
        digist = self.digist[num - 1]
        self.screen.blit(digist, (settings.SCREEN_SIZE[0] - settings.SCALE_SIZE[0] - 50, 30))

    def hide_digist(self, num, temp):
        if temp == num : return
        digist = self.digist[temp - 1]
        digist.fill([185,224,210])
        self.screen.blit(digist, (settings.SCREEN_SIZE[0] - settings.SCALE_SIZE[0] - 50, 30))
        
    #显示分数与目标分数
    def show_score(self, score, target_score):
        #设置字体
        FONT =  pygame.font.Font(None, 48)
        self.score.append(FONT.render(f'score: {score}', True, [0, 0, 0]))
        self.screen.blit(self.score[-1], (450, 40))
        self.screen.blit(FONT.render(f'target_score: {target_score}', True, [0, 0, 0]), (450, 80))
    
    #隐藏分数
    def hide_score(self,score, temp):
        FONT =  pygame.font.Font(None, 48)
        if score == temp: return
        self.score[-1].fill([53, 176, 238])
        self.screen.blit(self.score[-1], (450, 40))

    #构建布局
    def create_layout(self):
        pygame.init()
        self._create_screen(settings.SCREEN_SIZE)
        self._add_bg(self.screen, settings.IMAGE_BG)
        pygame.display.set_caption(settings.TITLE)
        # pygame.display.flip()


#结束布局类
class End_layout:
    def __init__(self) -> None:
        self.screen = None

    #渲染窗口
    def _create_screen(self, screen_size):
        self.screen = pygame.display.set_mode(screen_size, 0,0)
        
        return self.screen
    
    def _add_bg(self, screen, bg_io):
        bg = pygame.transform.scale(pygame.image.load(bg_io), (settings.SCREEN_WIGHT - 200, settings.SCREEN_HEIGHT - 200))
        screen.blit(bg, (100, 100))
    
    def _add_succ_bg(self, screen, bg_io):
        bg = pygame.transform.scale(pygame.image.load(bg_io), (settings.SCREEN_WIGHT-200, settings.SCREEN_HEIGHT))
        screen.blit(bg, (150, 0))

    #失败结束画面
    def load_end(self):
        pygame.init()
        self.screen = self._create_screen(settings.SCREEN_SIZE)
        self._add_bg(self.screen, settings.END_BG)
    
    #成功结束画面
    def load_success(self):
        pygame.init()
        self.screen = self._create_screen(settings.SCREEN_SIZE)
        self._add_succ_bg(self.screen, settings.SUCCESS_BG)


#定义图片按钮类
class imagBtn:

    _checkable = True
    _checked = False

    def __init__(self, screen, imag_io, x, y, num, icon_num) -> None:
        self.screen = screen
        self.x = x
        self.y = y
        #第几个元素(1~60)
        self.num = num
        self.vairnum = num
        #图片编号(1~6)
        self.icon_num = icon_num

        #缩放图片
        self.orginal_image = pygame.transform.scale(pygame.image.load(imag_io), settings.SCALE_SIZE)
        self.image = self.orginal_image.copy()
    
    #渲染图片和描边
    def display_image(self):
        if self._checked:
            pygame.draw.rect(self.image, [233,122,233], (0,0, settings.SCALE_SIZE[0] - 1, settings.SCALE_SIZE[1] - 1), 2)
        self.screen.blit(self.image, (self.x, self.y))

    def hide(self):
        self._checked = False
        self._checkable = False

        self.image.fill([255, 255, 255])

    def reset(self):
        self._checked = False
        self.image = self.orginal_image.copy()
        # self.screen.blit(self.image, (self.x, self.y))
    
    def click(self):
        self._checked = not self._checked
        return self._checked
    
    def is_checkable(self):
        return self._checkable