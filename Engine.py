import copy

import numpy as np
import pygame

from PreProc import *

class Move():
    '''Определяет объект перемещения фигуры, который будет заноситься в GameState MoveLog'''

    def __init__(self, startCell, endCell, board : np.ndarray):
        self.startRow = startCell[0]
        self.startCol = startCell[1]
        self.endRow = endCell[0]
        self.endCol = endCell[1]
        self.figureMoved = board[self.startCol, self.startRow]
        self.figureCaptured = board[self.endCol, self.endRow]
        self.moveID = self.startRow * 1000 + self.startCol*100 + self.endRow*10+self.endCol
        # print(f'moveID={self.moveID}')

    def __str__(self):
        return self.moveID

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def constructMove(self):
        return np.array([[self.startCol, self.startRow],
                         [self.endCol, self.endRow]])

class GameState(object):
    """Класс определяет поле, на котором происходит действие игры.
    Поле представляет собой сетку 9 на 9, логически заменяемую массивом 9 на 9 инициализируемого изначально 0(то есть все поле пустое).
    Значение ячейки: 0 - никакой фигуры, 1 - король, 2 - защитник, 3 - атакующий."""
    DEFAULT_STATE = np.array([[0,0,0,3,3,3,0,0,0],
                              [0,0,0,0,3,0,0,0,0],
                              [0,0,0,0,2,0,0,0,0],
                              [3,0,0,0,2,0,0,0,3],
                              [3,3,2,2,1,2,2,3,3],
                              [3,0,0,0,2,0,0,0,3],
                              [0,0,0,0,2,0,0,0,0],
                              [0,0,0,0,3,0,0,0,0],
                              [0,0,0,3,3,3,0,0,0]], dtype=np.int32)

    def __init__(self, board = DEFAULT_STATE):
        self.__board = board
        self.__Turn = True # Чей ход. True - защитники. False - атакующие
        self.__MoveLog = [] # Запись произошедших ходов

    def __str__(self):
        return str(self.__board)

    def get_board(self):
        return self.__board

    def set_board(self, board : np.ndarray):
        self.__board = board

    def makeMove(self, move : Move):
        self.__board[move.startCol, move.startRow] = 0
        self.__board[move.endCol, move.endRow] = move.figureMoved
        self.__MoveLog.append(move)
        self.__Turn = not self.__Turn

    def undoMove(self):
        move = self.__MoveLog.pop()
        self.__board[move.startCol, move.startRow] = move.figureMoved
        self.__board[move.endCol, move.endRow] = move.figureCaptured
        self.__Turn = not self.__Turn

    def getValidMoves(self):
        return self.getAllPossibleMoves()


    def getAllPossibleMoves(self):
        # moves = [Move((5,4),(5,5),self.__board)]
        moves = []
        for i in range(RC_NUMBER):
            for j in range(RC_NUMBER):
                figure = self.__board[i,j]
                if figure == 3:
                    self.getAttackerMoves(i,j,moves)
                if figure == 2:
                    self.getDefenderMoves(i,j,moves)
                if figure == 1:
                    self.getKingMoves(i,j,moves)


        return moves

    def getDotMoves(self,i,j,moves):
        '''Определяет все движения для простой фигуры атакющего или защищающегося'''
        # Движение по строке влево от фигуры
        for x in range(i - 1, -1, -1):
            if self.__board[x, j] == 0:
                moves.append(Move((i, j), (x, j), self.__board))
            else:
                break
        # Движение по строке вправо от фигуры
        for x in range(i + 1, RC_NUMBER, 1):
            if self.__board[x, j] == 0:
                moves.append(Move((i, j), (x, j), self.__board))
            else:
                break
        # Движение по столбцу вверх от фигуры
        for x in range(j - 1, -1, -1):
            if self.__board[i, x] == 0:
                moves.append(Move((i, j), (i, x), self.__board))
            else:
                break
        # Движение по столбцу вниз от фигуры
        for x in range(j + 1, RC_NUMBER, 1):
            if self.__board[i, x] == 0:
                moves.append(Move((i, j), (i, x), self.__board))
            else:
                break



    def getAttackerMoves(self,i,j,moves):
        if not self.__Turn:
            self.getDotMoves(i,j,moves)


    def getDefenderMoves(self,i,j,moves):
        if self.__Turn:
            self.getDotMoves(i,j,moves)


    def getKingMoves(self, i, j, moves):
        maxr = max(RC_NUMBER, i+3)
        minr = min(0, i-3)
        maxc = max(RC_NUMBER, j+3)
        minc = min(0, j-3)

        # Движение по строке влево от короля
        for x in range(i - 1, minr, -1):
            if self.__board[x, j] == 0:
                moves.append(Move((i, j), (x, j), self.__board))
            else:
                break
        # Движение по строке вправо от короля
        for x in range(i + 1, maxr, 1):
            if self.__board[x, j] == 0:
                moves.append(Move((i, j), (x, j), self.__board))
            else:
                break
        # Движение по столбцу вверх от короля
        for x in range(j - 1, minc, -1):
            if self.__board[i, x] == 0:
                moves.append(Move((i, j), (i, x), self.__board))
            else:
                break
        # Движение по столбцу вниз от короля
        for x in range(j + 1, maxc, 1):
            if self.__board[i, x] == 0:
                moves.append(Move((i, j), (i, x), self.__board))
            else:
                break



    def DrawFigures(self, screen):
        for i in range(RC_NUMBER):
            for j in range(RC_NUMBER):
                pos = [GRID_INIT_POS[0] + GRID_STEP_SIZE*j, GRID_INIT_POS[1] + GRID_STEP_SIZE*i]

                if self.__board[i,j] == 3:
                    screen.blit(IMAGES['attacker'], pygame.Rect(pos,(int(Screen_width*0.05), int(Screen_width*0.05))))
                if self.__board[i,j] == 2:
                    screen.blit(IMAGES['defender'],
                                pygame.Rect(pos, (int(Screen_width * 0.05), int(Screen_width * 0.05))))
                if self.__board[i,j] == 1:
                    screen.blit(IMAGES['king'],
                                pygame.Rect(pos, (int(Screen_width * 0.05), int(Screen_width * 0.05))))





