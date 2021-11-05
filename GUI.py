from PreProc import *

class Backlighter():

    def __init__(self, pos : np.ndarray, size : np.ndarray, color : list):
        self.__pos = pos
        self.__size = size
        self.__color = color

    def backlight(self,screen, backlight = False):
        if backlight:
            pygame.draw.rect(screen, COLORS['HIGHLIGHTER'],  pygame.Rect(int(self.__pos[0] - 0.125*self.__size[0]), int(self.__pos[1] - 0.125*self.__size[1]), int(1.25*self.__size[0]), int(1.25*self.__size[1])))

    def pgDraw(self,screen):
        pygame.draw.rect(screen, self.__color, pygame.Rect(int(self.__pos[0]), int(self.__pos[1]), int(self.__size[0]), int(self.__size[1])))


