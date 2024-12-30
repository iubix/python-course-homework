import pygame
import sys
from pygame import *
import settings
import split_image
import pathlib

image_list = []
map_list = []

cnt_list = []
cnt = 0

class imagBtn:

    _checkable = True
    _checked = False

    def __init__(self, screen, imag_io, x, y, num, icon_num) -> None:
        self.screen = screen
        self.x = x
        self.y = y
        #第几个元素(0~35)
        self.num = num
        #图片编号(0~35)
        self.icon_num = icon_num

        #缩放图片
        self.image = pygame.transform.scale(pygame.image.load(imag_io), settings.SCALE_SIZE)

    def display_image(self):
        self.screen.blit(self.image, (self.x, self.y))
    
    def click(self):
        self._checked = not self._checked
        return self._checked

#显示点击次数
def show_digit(screen, cnt):
    #设置字体
    global cnt_list
    FONT =  pygame.font.Font(None, 48)
    
    cnt_list.append(FONT.render(str(cnt), True, (255, 255, 255)))
    screen.blit(cnt_list[-1], (500, 40))

def hide_digit(screen, temp, cnt):
    global cnt_list
    FONT =  pygame.font.Font(None, 48)
    if temp == cnt: return
    cnt_list[-1].fill((230, 230, 240, 233))
    screen.blit(cnt_list[-1], (500, 40))


#显示图片
def display(screen):
    global image_list, map_list
    image_list = []
    img_io = pathlib.Path(__file__).parent / 'splitImage' / 'icon'
    for i in range(0, settings.MAP_TOTAL):
        x = int(i % settings.GAME_COL) * settings.GRID_SIZE + (settings.GRID_SIZE - settings.SCALE_SIZE[0])/2
        y = int(i / settings.GAME_COL) * settings.GRID_SIZE + (settings.GRID_SIZE - settings.SCALE_SIZE[1])/2
        ele_io = str(img_io) + str(map_list[i]) + '.png'
        image_list.append(imagBtn(screen, ele_io, x + settings.BIAS, y + settings.BIAS, i, map_list[i]))

#判断相邻
def is_neighbour(points):
    if abs(points[0].num - points[1].num) == settings.GAME_COL or abs(points[0].num - points[1].num) == 1:
        return True
    return False

#位置交换
def isswap(points, map_list):
    if is_neighbour(points):
        map_list[points[0].num], map_list[points[1].num] = map_list[points[1].num], map_list[points[0].num]
        return True
    return False


#判断局面
def is_right():
    map_right = range(0, settings.MAP_TOTAL)
    if map_list == map_right:
        return True
    return False


#事件点击
def event_click(imgbtn, screen):
    for event in pygame.event.get():
        
        if event.type == QUIT:
    
            sys.exit()
        
        elif event.type == MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            
            for btn in imgbtn:
                x = btn.x; y = btn.y
                w = settings.SCALE_SIZE[0]
                h = settings.SCALE_SIZE[1]
                
                if pos[0] > x and pos[0] < x + w and pos[1] > y and pos[1] < y + h:
                    if btn._checkable:
                        
                        if not btn.click():
                            # 点自己是无效的
                            settings.POINTS.clear()
                            print('不能和自己交换位置')
                            break
                        #第二张图片
                        if settings.POINTS != []:
                            
                            settings.POINTS.append(btn)
                            if isswap(settings.POINTS, map_list):
                                display(screen)
                                for i in image_list:
                                    i.display_image()
                                global cnt
                                cnt += 1
                                settings.POINTS.clear()
                                print('交换成功')
                            else:
                                settings.POINTS.clear()
                                print('非相邻的图片不能交换')
                        else:
                            #第一张图片
                            settings.POINTS.append(btn)
                    

                    break


#主函数
def main():
    
    pygame.init()
    screen = pygame.display.set_mode(settings.SCREEN_SIZE, 0,0)
    screen.fill(settings.BG_COLOR)
    pygame.display.set_caption(settings.TITLE)
    

    global map_list, image_list, cnt
    map_list = split_image.built_map()
    display(screen)
    flag = True
    
    while True:
        show_digit(screen, cnt)
        temp = cnt
        if flag:
            if is_right():
                flag = False
            for i in image_list:
                i.display_image()
        else:
            sys.exit(0)

        pygame.display.update()

        #事假点击
        event_click(image_list, screen)
        hide_digit(screen, temp, cnt)
        pygame.display.update()


if __name__ == '__main__':

    # split_image.splitImage(r'Python_course\course5\111159609_p0.jpg', settings.GAME_ROW, settings.GAME_COL)
    
    main()