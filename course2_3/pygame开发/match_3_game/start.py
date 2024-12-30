'''
启动文件
'''

import pygame
import sys
import pathlib
sys.path.append(pathlib.Path(__file__).parent.parent)

if __name__ == "__main__":
    from src import main
    
    main()