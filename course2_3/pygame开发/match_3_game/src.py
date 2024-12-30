'''
主逻辑文件
'''

import pygame
import random
import view
import threading
from pygame.locals import *
from conf import settings
import time
import sys

times_out = settings.BASE_CLICKED
score = 0
target_score = settings.BASE_TARGET_SCORE
clear_imgs = 0

#日志处理
main_logger = view.get_logger('main')
    

#获取邻居节点
def get_neighbor(num):
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
    # #排除根节点
    # if root != None:
    #     for each in root:
    #         if each in neighborlist:
    #             neighborlist.remove(each)
    return neighborlist

#判断是否是邻居
def is_neighbor(point1, point2):
    neiborlist = get_neighbor(point1.num)
    for each in neiborlist:
        if each == point2.num:
            return True
    return False

#生成新的图像
def gen_img(current, temp_btn, map_list):
    map_list[current.num] = random.randint(1, 6)
    for each in temp_btn:
        map_list[each] = random.randint(1, 6)
        # print(map_list[each])

#检查局面是否合法
def check_map(map_list):
    #横向搜索
    for i in range(settings.GAME_ROW):
        row = i * settings.GAME_COL
        for j in range(settings.GAME_COL - 2):
            if map_list[row + j] == map_list[row + j + 1] == map_list[row + j + 2]:
                return True
                
    #竖向搜索
    for i in range(settings.GAME_COL):
        for j in range(settings.GAME_ROW - 2):
            if map_list[i + j * settings.GAME_COL] == map_list[i + (j + 1) * settings.GAME_COL] == map_list[i + (j + 2) * settings.GAME_COL]:
                return True
    return False
#重新生成局面
def gen_map(map_list):
    #横向搜索
    for i in range(settings.GAME_ROW):
        row = i * settings.GAME_COL
        for j in range(settings.GAME_COL - 2):
            if map_list[row + j] == map_list[row + j + 1] == map_list[row + j + 2]:
                map_list[row + j] = random.randint(1, 6)
                map_list[row + j + 1] = random.randint(1, 6)
                map_list[row + j + 2] = random.randint(1, 6)
    #竖向搜索
    for i in range(settings.GAME_COL):
        for j in range(settings.GAME_ROW - 2):
            if map_list[i + j * settings.GAME_COL] == map_list[i + (j + 1) * settings.GAME_COL] == map_list[i + (j + 2) * settings.GAME_COL]:
                map_list[i + j * settings.GAME_COL] = random.randint(1, 6)
                map_list[i + (j + 1) * settings.GAME_COL] = random.randint(1, 6)
                map_list[i + (j + 2) * settings.GAME_COL] = random.randint(1, 6)
#搜索函数
def search(point1, point2, map_list):
    global clear_imgs
    temp_btn = []
    row = point2.num // settings.GAME_COL
    
    left = 10*row
    right = left + settings.GAME_COL - 1
    
    top = 0
    down = settings.GAME_ROW - 1
    
    
    left_times = point2.num - left
    up_times = row - top
    down_times = down - row
    right_times = right - point2.num


    #1
    for i in range(left_times):
        
        num = point2.num - (i+1)
        if map_list[num] == point1.icon_num:
            temp_btn.append(num)
        else: break
    for i in range(right_times):
        num = point2.num + (i+1)
        if map_list[num] == point1.icon_num:
            temp_btn.append(num)
        else: break
    print(temp_btn)
    if len(temp_btn) >= 2:
        #生成覆盖
        gen_img(point2, temp_btn, map_list)
        clear_imgs = len(temp_btn) + 1
        return True
    temp_btn.clear()
    
    #2
    for i in range(up_times):
        num = point2.num - (i+1)*settings.GAME_COL
        if map_list[num] == point1.icon_num:
            temp_btn.append(num)
        else: break
    for i in range(down_times):
        num = point2.num + (i+1)*settings.GAME_COL
        if map_list[num] == point1.icon_num:
            temp_btn.append(num)
        else: break
    print(temp_btn)
    if len(temp_btn) >= 2:
        #生成
        gen_img(point2, temp_btn, map_list)
        clear_imgs = len(temp_btn) + 1
        return True
    temp_btn.clear()
    
    return False

#定义清除函数
def can_clear(point1, point2, map_list):
    map_list[point1.num],map_list[point2.num] = map_list[point2.num],map_list[point1.num]

    if search(point1, point2, map_list) or search(point2, point1, map_list): return True
    map_list[point1.num],map_list[point2.num] = map_list[point2.num],map_list[point1.num]
    return False
            
#定义交换函数
def swapclear_points(points, map_list):
    point1 = points[0]; point2 = points[1]
    if is_neighbor(point1, point2):
        #一样的交换了也不能清除
        if point1.icon_num == point2.icon_num: return False

        if can_clear(point1, point2, map_list):
            
            return True
        return False
    else:
        return False


def is_over():
    return False
    # for each in varimap_list:
    #     if each > 0:
    #         return False
    # return True

#事件处理
def event_click(image_list, map_list, layout):
    global times_out, score
    for event in pygame.event.get():
        
        if event.type == QUIT:
            msg = '用户已退出'
            main_logger.info(msg)
            sys.exit()
        
        elif event.type == MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            
            for imgbtn in image_list:
                x = imgbtn.x; y = imgbtn.y
                w = settings.SCALE_SIZE[0]
                h = settings.SCALE_SIZE[1]
                
                if pos[0] > x and pos[0] < x + w and pos[1] > y and pos[1] < y + h:
                    if imgbtn.is_checkable():

                        if not imgbtn.click():
                            # 点自己是无效的
                            settings.POINTS.clear()
                            msg = f'不能和自己交换位置'
                            main_logger.warning(msg)
                            break
                        if settings.POINTS != []:
                            settings.POINTS.append(imgbtn)

                            if swapclear_points(settings.POINTS, map_list):
                                layout.display()
                                for i in layout.image_list:
                                    i.display_image()
                                time.sleep(0.1)
                                #检查局面
                                while check_map(map_list):
                                    gen_map(map_list)
                                layout.display()
                                pygame.mixer.init()
                                pygame.mixer.music.load(settings.MUSIC_CLICK)
                                pygame.mixer.music.play()
                                msg = f'完成交换清除'
                                main_logger.info(msg)
                                score += 4*clear_imgs
                                print(score)
                                times_out -= 1
                                settings.POINTS.clear()
                            else: 
                                msg = f'无法交换清除'
                                main_logger.info(msg)
                                pygame.mixer.init()
                                pygame.mixer.music.load(settings.MUSIC_ERROR)
                                pygame.mixer.music.play()
                                for imgbtn in settings.POINTS:
                                    imgbtn.reset()
                                times_out -= 1
                                settings.POINTS.clear()
                        else:
                            settings.POINTS.append(imgbtn)
                    break
                
                        
                        

        

def main():

    msg = '游戏开始'
    main_logger.info(msg)
    # pygame.init()
    layout = view.Layout()
    #构建布局
    layout.create_layout()
    
    layout.built_map()
    layout.load_digist()
    # varimap_list = map_list.copy()
    #获取图片类列表
    layout.display()

    pygame.mixer.init()
    pygame.mixer.music.load(settings.MUSIC_START)
    pygame.mixer.music.play()

    #检查布局是否合法
    gen_map(layout.map_list)
    while check_map(layout.map_list):
        gen_map(layout.map_list)
    layout.display()
    for i in layout.image_list:
        i.display_image()
    global times_out,score
    score = 0
    times_out = settings.BASE_CLICKED
    flag = True
    
    success = False
    click = True

    while True:
        layout.show_digist(times_out)
        layout.show_score(score, target_score)
        temp = times_out
        tempscore = score
        if not times_out:
            flag = False
            msg = '已到最大可交换次数，游戏结束'
            main_logger.info(msg)
        if score >= target_score:
            flag = False
            success = True
            msg = '达到目标分数，游戏胜利'
            main_logger.info(msg)
        if flag:
            if is_over():
                flag = False
            for i in layout.image_list:
                
                i.display_image()
        else:
            endlayout = view.End_layout()
            if success:
                endlayout.load_success()
                pygame.mixer.init()
                pygame.mixer.music.load(settings.MUSIC_SUCCESS)
                pygame.mixer.music.play()
                while click:
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            msg = '用户已退出'
                            main_logger.info(msg)
                            sys.exit()
                        elif event.type == MOUSEBUTTONDOWN:
                            msg = '用户已重新开始'
                            main_logger.info(msg)
                            main()

                    pygame.display.update()
            endlayout.load_end()
            pygame.mixer.init()
            pygame.mixer.music.load(settings.MUSIC_END)
            pygame.mixer.music.play()
            while click:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        msg = '用户已退出'
                        main_logger.info(msg)
                        sys.exit()
                    elif event.type == MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        x = pos[0]; y = pos[1]
                        if x > 270 and x < 635 and y > 680 and y < 770:
                            click = False
                            #退出
                            msg = '用户已退出'
                            main_logger.info(msg)
                            sys.exit()
                        if x > 270 and x < 635 and y > 570 and y < 660:
                            click = False
                            #重新开始
                            msg = '用户已重新开始'
                            main_logger.info(msg)
                            main()

                pygame.display.update()
            sys.exit(0)

        #事假点击
        event_click(layout.image_list, layout.map_list, layout)
        layout.hide_digist(times_out, temp)
        layout.hide_score(score, tempscore)
        # layout.display()
        pygame.display.update()


    
        
        
    

    
