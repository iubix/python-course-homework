'''
主逻辑文件
'''
import sys, time
import math, random
import threading
import pygame
from pygame.locals import *
from conf import settings
import disp

map_list = []
varimap_list = []
image_list = []
time_out = False

#初始化日志记录
main_logger = disp.get_logger('main_src')

#计时
def time_clock():
    global time_out
    time_lim = 90
    while time_lim > 0:
        time.sleep(1)
        time_lim -= 1
        msg = '剩余时间：' + str(time_lim)
        print(msg)
    time_out = True
    return time_out

#获取邻居节点
def get_neighbor(num, root):
    col = num % settings.GAME_COL
    row = num // settings.GAME_COL
    neighborlist = []
    if num + 1 != (row + 1) * settings.GAME_COL or num + 1 < settings.MAP_TOTAL:
        neighborlist.append(num + 1)
    if num - 1 >= 0 or num != row * settings.GAME_COL:
        neighborlist.append(num - 1)
    if num + settings.GAME_COL < settings.MAP_TOTAL:
        neighborlist.append(num + settings.GAME_COL)
    if num - settings.GAME_COL >= 0:
        neighborlist.append(num - settings.GAME_COL)
    #排除根节点
    if root != None:
        for each in root:
            if each in neighborlist:
                neighborlist.remove(each)
    return neighborlist


#bfs搜索函数
def search(points):
    point1 = points[0]; point2 = points[1]
    neighborlist = []
    root = [point1.num]
    neighborlist.extend(get_neighbor(point1.num, None))
    
    while neighborlist != []:
        #右 左 下 上
        temp_root = []
        for num in neighborlist:
            #已清除的
            if varimap_list[num] == 0:
                neighborlist.extend(get_neighbor(num, root))
                temp_root.append(num)
                neighborlist.remove(num)
                continue
            # icon_num = map_list[num]
            if num == point2.num:
                return True
            neighborlist.remove(num)
            
        if root != []:
            for each in root:
                root.remove(each)
            root.extend(temp_root)
              

#判断图片是否全部清除
def is_over():
    for each in varimap_list:
        if each > 0:
            return False
    return True

#判断图片能否被清除
def can_clear(points):
    if points[0].icon_num != points[1].icon_num:
        return False
    if search(points):
        return True
    return False


#事件点击
def event_click(imgbtn):
    for event in pygame.event.get():
        
        if event.type == QUIT:
            msg = '用户已退出'
            main_logger.info(msg)
            sys.exit()
        
        elif event.type == MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            
            for btn in imgbtn:
                x = btn.x; y = btn.y
                w = settings.SCALE_SIZE[0]
                h = settings.SCALE_SIZE[1]
                
                if pos[0] > x and pos[0] < x + w and pos[1] > y and pos[1] < y + h:
                    if btn.is_checkable():
                        
                        if not btn.click():
                            # 点自己是无效的
                            settings.POINTS.clear()
                            msg = f'不能和自己清除'
                            main_logger.warning(msg)
                            break
                        #第二张图片
                        if settings.POINTS != []:
                            
                            settings.POINTS.append(btn)
                           
                            if can_clear(settings.POINTS):
                                #能清除
                                for imgBtn in settings.POINTS:
                                    varimap_list[imgBtn.num] = 0
                                    
                                    imgBtn.hide()
                                msg = f'第{settings.POINTS[0].num}个图片和第{settings.POINTS[1].num}个图片已清除'
                                main_logger.info(msg)
                                settings.POINTS.clear()
                            else:
                                #不能清除
                                for imgBtn in settings.POINTS:
                                    imgBtn.reset()
                                msg = f'第{settings.POINTS[0].num}个图片和第{settings.POINTS[1].num}个图片不能清除'
                                main_logger.warning(msg)
                                settings.POINTS.clear()
                                
                
                        else:
                            #第一张图片
                            settings.POINTS.append(btn)
                    

                    break


#主函数
def main():
    import pathlib
    pygame.init()
    screen = disp.create_screen(settings.SCREEN_SIZE)
    screen.fill(settings.BG_COLOR)
    pygame.display.set_caption(settings.TITLE)
    
    #计时器
    t = threading.Thread(target = time_clock)
    t.start()
    
    global map_list, image_list, varimap_list
    map_list = disp.built_map()
    varimap_list = map_list.copy()
    
    img_io = pathlib.Path(__file__).parent / 'img' / 'icon'
    for i in range(0, settings.MAP_TOTAL):
        x = int(i % settings.GAME_COL) * settings.GRID_SIZE + (settings.GRID_SIZE - settings.SCALE_SIZE[0])/2
        y = int(i / settings.GAME_COL) * settings.GRID_SIZE + (settings.GRID_SIZE - settings.SCALE_SIZE[1])/2
        ele_io = str(img_io) + str(map_list[i]) + '.png'
        image_list.append(disp.imagBtn(screen, ele_io, x, y, i, map_list[i]))

    flag = True
    
    while True:
        if time_out:
            flag = False
            msg = '时间到，游戏结束'
            main_logger.info(msg)
        
        if flag:
            if is_over():
                flag = False
            for i in image_list:
                i.display_rect()
        else:
            sys.exit(0)

        pygame.display.update()

        #事假点击
        event_click(image_list)
        pygame.display.update()