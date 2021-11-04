import numpy as np
import pygame
from win32api import GetSystemMetrics
import os
import sys
from copy import deepcopy, copy
import tkinter
import tkinter.filedialog

# Все цвета используемые для отображения
COLORS = {'BACKGROUND':[26,5,80], 'BACK_RECT' : [63,7,98], 'LINE' : [221,7,232], 'EXIT_RECT' : [95,111,224], 'THRONE' : [153, 255, 255], 'HIGHLIGHT_YELLOW' : [248, 3, 252], 'HIGHLIGHT_BLUE' : [3,144,252]}
FPS = 30
MULTIPLIER = 1.3
# Преопределим переменные, отвечающие за размер экрана здесь
Screen_width, Screen_height = int(MULTIPLIER*GetSystemMetrics(1)), int(0.75*MULTIPLIER*GetSystemMetrics(1))

RC_NUMBER = 9
GRID_INIT_POS = (Screen_width * 0.275, Screen_width * 0.15)
GRID_STEP_SIZE = Screen_width*0.05
GRID_LENGTH = GRID_STEP_SIZE*RC_NUMBER

# Координаты углов поля
LUC_COORDS = (Screen_width * 0.275, Screen_width * 0.15)
RUC_COORDS = (Screen_width * 0.675, Screen_width * 0.15)
RLC_COORDS = (Screen_width * 0.275, Screen_width * 0.55)
LLC_COORDS = (Screen_width * 0.675, Screen_width * 0.55)
# Координаты центра
TC_COORDS = (Screen_width * 0.475, Screen_width * 0.35)


# Загрузим необходимые изображения
IMAGES = {}

def load_images():
    list = ['king', 'defender', 'attacker', 'field']
    for item in list:
        IMAGES[item] = pygame.image.load('images/'+ item + '.png')

load_images()

# Омасштабируем их
IMAGES['field'] = pygame.transform.scale(IMAGES['field'], (int(Screen_width*0.45), int(Screen_width*0.45)))
IMAGES['king'] = pygame.transform.scale(IMAGES['king'], (int(Screen_width*0.05), int(Screen_width*0.05)))
IMAGES['defender'] = pygame.transform.scale(IMAGES['defender'], (int(Screen_width*0.05), int(Screen_width*0.05)))
IMAGES['attacker'] = pygame.transform.scale(IMAGES['attacker'], (int(Screen_width*0.05), int(Screen_width*0.05)))

def pgDrawField(screen):
    '''Отрисовывает поле'''
    # Задник
    pygame.draw.rect(screen, COLORS['BACK_RECT'], pygame.Rect(Screen_width * 0.05, Screen_width * 0.075,
                                                              Screen_width * 0.9, Screen_width * 0.625))

    # Левый верхний
    pygame.draw.rect(screen, COLORS['EXIT_RECT'], pygame.Rect(LUC_COORDS[0], LUC_COORDS[1],
                                                              GRID_STEP_SIZE, GRID_STEP_SIZE))

    # Правый верхний
    pygame.draw.rect(screen, COLORS['EXIT_RECT'], pygame.Rect(RUC_COORDS[0], RUC_COORDS[1],
                                                              GRID_STEP_SIZE, GRID_STEP_SIZE))

    # Правый нижний
    pygame.draw.rect(screen, COLORS['EXIT_RECT'], pygame.Rect(RLC_COORDS[0], RLC_COORDS[1],
                                                              GRID_STEP_SIZE, GRID_STEP_SIZE))

    # Левый нижний
    pygame.draw.rect(screen, COLORS['EXIT_RECT'], pygame.Rect(LLC_COORDS[0], LLC_COORDS[1],
                                                              GRID_STEP_SIZE, GRID_STEP_SIZE))
    # Трон
    pygame.draw.rect(screen, COLORS['THRONE'], pygame.Rect(TC_COORDS[0], TC_COORDS[1],
                                                              GRID_STEP_SIZE, GRID_STEP_SIZE))

    # Линии
    for i in range(RC_NUMBER+1):
        pygame.draw.line(screen,COLORS['LINE'],(GRID_INIT_POS[0] + GRID_STEP_SIZE*i ,GRID_INIT_POS[1]),
                         (GRID_INIT_POS[0] + GRID_STEP_SIZE*i, GRID_INIT_POS[1] + GRID_LENGTH),1)
        pygame.draw.line(screen, COLORS['LINE'], (GRID_INIT_POS[0], GRID_INIT_POS[1] + GRID_STEP_SIZE * i),
                         (GRID_INIT_POS[0] + GRID_LENGTH, GRID_INIT_POS[1] + GRID_STEP_SIZE * i), 1)

def DrawFigureTest(screen):
    pos = [100,100]
    screen.blit(IMAGES['king'], pygame.Rect(pos[0], pos[1], int(Screen_width * 0.05), int(Screen_width * 0.05)))