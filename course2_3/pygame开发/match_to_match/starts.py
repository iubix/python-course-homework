'''
启动文件
'''

import sys
import pathlib
import pygame
import threading

sys.path.append(pathlib.Path(__file__).parent)


if __name__ == '__main__':
    from src import main

    main()

