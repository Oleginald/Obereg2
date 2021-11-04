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
        self.figureMoved = board[self.startRow, self.startCol]
        self.figureCaptured = board[self.endRow, self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol*100 + self.endRow*10+self.endCol
        # print(f'moveID={self.moveID}')

    def __str__(self):
        return str(self.moveID)

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

    TEST_STATE = np.array([[0,2,0,0,3,0,0,0,0],
                              [0,0,0,0,0,0,0,0,0],
                              [0,0,0,0,0,0,0,0,0],
                              [0,0,0,0,0,0,0,0,0],
                              [3,0,0,0,1,0,0,0,3],
                              [0,0,0,0,0,0,0,0,0],
                              [0,0,0,0,0,0,0,0,0],
                              [0,0,0,0,0,0,0,0,0],
                              [0,0,0,0,3,0,0,0,0]], dtype=np.int32)

    # Индексные области игрового поля
    REGIONS = {'THRONE' : [4,4],
                'NEAR_THRONE' : [[3,4],[4,5],[5,4],[4,3]],
                'CORNERS' : [[0,0], [0,8], [8,0], [8,8]],
                'NEAR_CORNERS' : [[1,0],[0,1],[0,7],[1,8],[7,8],[8,7],[7,0],[8,1]],
                'ROWS08' : [[0,2],[0,3],[0,4],[0,5],[0,6],
                            [8,2],[8,3],[8,4],[8,5],[8,6]],
                'COLS08' : [[2,0],[3,0],[4,0],[5,0],[6,0],
                            [2,8],[3,8],[4,8],[5,8],[6,8]],
                'CORE' : [[1,1],[1,2],[1,3],[1,4],[1,5],[1,6],[1,7],
                          [2,1],[2,2],[2,3],[2,4],[2,5],[2,6],[2,7],
                          [3,1],[3,2],[3,3],[3,5],[3,6],[3,7],
                          [4,1],[4,2],[4,6],[4,7],
                          [5,1],[5,2],[5,3],[5,5],[5,6],[5,7],
                          [6,1],[6,2],[6,3],[6,4],[6,5],[6,6],[6,7],
                          [7,1],[7,2],[7,3],[7,4],[7,5],[7,6],[7,7]]}

    def __init__(self, board = TEST_STATE):
        self.__board = board
        self.__Turn = False # Чей ход. True - защитники. False - атакующие. Начинают атакующие
        self.__DeleteLog = [] # запись удаленных фигур
        self.__MoveLog = [] # Запись произошедших ходов
        self.kingLocation = np.array([4,4])

    def __str__(self):
        return str(self.__board)

    def get_board(self):
        return self.__board

    def set_board(self, board : np.ndarray):
        self.__board = board

    def get_turn(self):
        return self.__Turn

    def print_gs(self):
        print(f'Turn={self.__Turn}')
        print(self.__board)

    def makeMove(self, move : Move):
        self.__board[move.startRow, move.startCol] = 0
        self.__board[move.endRow, move.endCol] = move.figureMoved
        self.__MoveLog.append(move)
        self.__Turn = not self.__Turn
        # Обновим позицию короля вперед
        if move.figureMoved == 1:
            self.kingLocation = (move.endRow, move.endCol)

    def undoMove(self):
        try:
            move = self.__MoveLog.pop()
            self.__board[move.startRow, move.startCol] = move.figureMoved
            self.__board[move.endRow, move.endCol] = move.figureCaptured
            self.__Turn = not self.__Turn
            # обновляем позицию короля назад
            if move.figureMoved == 1:
                self.kingLocation = (move.startRow, move.startCol)
        except IndexError:
            print(f'Нечего отменять')

    # def getValidMoves(self):
    #     # 1 Сначала создадим вообще все возможные ходы защищающихся
    #     moves = self.getAllPossibleMoves()
    #     # 2 Потом сделаем ход, какой хотим из всех возможных
    #     for i in range(len(moves)-1, -1, -1): # проход по листу назад позволит избежать проеба элементов
    #         self.makeMove(moves[i])
    #     # 3 Создадим все ходы атакующей стороы
    #     # 4 Среди них посмотрим, какие ходы уничтжают нашего короля
    #     # 5 Если вообще среди 4 есть такие ходы, то наш ход 3 надо запретить,
    #     # и так для всех ходов среди 1
    #
    #     return moves

    def getValidMoves(self):
        return self.getAllPossibleMoves()

    def getAllPossibleMoves(self):
        # moves = [Move((5,4),(5,5),self.__board),Move((5,5),(5,4),self.__board)]
        moves = []
        for i in range(RC_NUMBER):
            for j in range(RC_NUMBER):
                figure = self.__board[i,j]
                # print(f'fig={figure}')
                if self.__Turn == True:
                    if figure == 2:
                        self.getDefenderMoves(i, j, moves)
                    if figure == 1:
                        # print(f'i={i}')
                        # print(f'j={j}')
                        # print(f'yESSSSSS')
                        self.getKingMoves(i, j, moves)
                else:
                    if figure == 3:
                        self.getAttackerMoves(i,j,moves)
        #Печать возможных ходов
        print(f'moves:')
        counter = 0
        for move in moves:
            if counter == 11:
                print()
                counter = 0
            print(move, end=' ')
            counter += 1
        print()
        # self.print_board()

        return moves

    def DotCornerDeletable(self,adot:list,i:int,j:int):
        '''Определяет можно ли удалить фигуру, расположенную около углов'''
        if [i,j] == [1,0] and self.__board[2,0] in adot:
            return True
        if [i,j] == [0,1] and self.__board[0,2] in adot:
            return True
        if [i,j] == [0,7] and self.__board[0,6] in adot:
            return True
        if [i,j] == [1,8] and self.__board[2,8] in adot:
            return True
        if [i,j] == [7,8] and self.__board[6,8] in adot:
            return True
        if [i,j] == [8,7] and self.__board[8,6] in adot:
            return True
        if [i,j] == [8,1] and self.__board[8,2] in adot:
            return True
        if [i,j] == [7,0] and self.__board[6,0] in adot:
            return True
        return False

    def DotFieldDeletable(self,adot:list,i:int,j:int):
        # Если фигура находится не у краев карты
        # Случай: ячейка зажата по вертикали(строки) или по горизонтали(столбцы) двумя ячейками атакующих
        c1 = (self.__board[i + 1, j] in adot) and (self.__board[i - 1, j] in adot)
        c2 = (self.__board[i, j + 1] in adot) and (self.__board[i, j - 1] in adot)
        if c1 or c2:
            return True
        return False

    def DotDeletable(self, adot : list, i : int, j : int):
        '''Определяет можно ли удалить фигуру атакующего или защитника'''
        # Если фигура находится около углов карты
        if [i,j] in GameState.REGIONS['NEAR_CORNERS']:
            return self.DotCornerDeletable(adot,i,j)

        elif [i,j] in GameState.REGIONS['NEAR_THRONE']:
            # Переписал условия
            if self.__board[4,4] == 1: # если король на троне
                # Если король на троне, то работает обычный зажим с двух сторон защитника
                if [i,j] == [4,3]: # левая ячейка
                    c1 = self.__board[3,3] in adot and self.__board[5,3] in adot
                    if c1:
                        return True
                elif [i,j] == [5,4]: #нижняя ячейка
                    c1 = self.__board[5,3] in adot and self.__board[5,5] in adot
                    if c1:
                        return True
                elif [i,j] == [4,5]: #правая ячейка
                    c1 = self.__board[3,5] in adot and self.__board[5,5] in adot
                    if c1:
                        return True
                elif [i,j] == [3,4]: #верхняя ячейка
                    c1 = self.__board[3,3] in adot and self.__board[3,5] in adot
                    if c1:
                        return True
                else:
                    return False
            else: # если король не на троне, то работает вышеописанный зажим и еще зажим между королем и троном
                if [i,j] == [4,3]: # левая ячейка
                    c1 = self.__board[3,3] in adot and self.__board[5,3] in adot
                    c2 = self.__board[4,2] in adot
                    if c1 or c2:
                        return True
                elif [i,j] == [5,4]: #нижняя ячейка
                    c1 = self.__board[5,3] in adot and self.__board[5,5] in adot
                    c2 = self.__board[6,4] in adot
                    if c1 or c2:
                        return True
                elif [i,j] == [4,5]: #правая ячейка
                    c1 = self.__board[3,5] in adot and self.__board[5,5] in adot
                    c2 = self.__board[4,6] in adot
                    if c1 or c2:
                        return True
                elif [i,j] == [3,4]: #верхняя ячейка
                    c1 = self.__board[3,3] in adot and self.__board[3,5] in adot
                    c2 = self.__board[2,4] in adot
                    if c1 or c2:
                        return True
                else:
                    return True

        elif [i,j] in GameState.REGIONS['ROWS08']:
            if (self.__board[i, j + 1] in adot) and (self.__board[i, j - 1] in adot):
                return True
            else:
                return False
        elif [i,j] in GameState.REGIONS['COLS08']:
            if(self.__board[i + 1, j] in adot) and (self.__board[i - 1, j] in adot):
                return True
            else:
                return False

        elif [i,j] in GameState.REGIONS['CORE']:
            return self.DotFieldDeletable(adot,i,j)

        return False

    def DefenderDeletable(self, i : int, j : int):
        '''Определяет можно ли удалить защитника'''
        adot = [3]
        return self.DotDeletable(adot,i,j)

    def AttackerDeletable(self, i:int, j:int):
        '''Определяет можно ли удалить атакующего'''
        adot = [1,2]
        return self.DotDeletable(adot,i,j)

    def KingDeletable(self, i : int, j : int):
        '''Определяет можно ли удалить короля'''
        adot = [3]
        # Если фигура находится около углов карты
        if [i,j] in GameState.REGIONS['NEAR_CORNERS']:
            return self.DotCornerDeletable(adot,i,j)
        elif [i,j] == [4,4]:
            print('YESSSSSSS')
            print(f'[4,3]={self.__board[4,3]}')
            print(f'[3,4]={self.__board[3,4]}')
            print(f'[3,4]={self.__board[3, 4]}')
            # все 4 ячейки вокруг заняты атакующими
            c1 = self.__board[4,3] in adot
            c2 = self.__board[3,4] in adot
            c3 = self.__board[4,5] in adot
            c4 = self.__board[5,4] in adot
            if c1 and c2 and c3 and c4:
            # if int(self.__board[4,3]) in adot and int(self.__board[3,4]) in adot in int(self.__board[4,5]) in adot and int(self.__board[5,4]) in adot:
                return True
            else:
                return False
        elif [i,j] in GameState.REGIONS['NEAR_THRONE']:
            # Если князь находится около трона. Необходимо, чтобы 3 ближайшеие ячейки к князю были занятый атакующими
            if [i,j] == [3,4]:
                if self.__board[3,3] in adot and self.__board[2,4] in adot and self.__board[3,5] in adot:
                    return True
                else:
                    return False
            if [i,j] == [4,3]:
                if self.__board[4,2] in adot and self.__board[5,3] in adot and self.__board[3,3] in adot:
                    return True
                else:
                    return False
            if [i,j] == [5,4]:
                if self.__board[5,3] in adot and self.__board[5,5] in adot and self.__board[6,4] in adot:
                    return True
                else:
                    return False
            if [i,j] == [4,5]:
                if self.__board[3,5] in adot and self.__board[5,5] in adot and self.__board[4,6] in adot:
                    return True
                else:
                    return False

        elif [i,j] in GameState.REGIONS['ROWS08']:
            if (self.__board[i, j + 1] in adot) and (self.__board[i, j - 1] in adot):
                return True
            else:
                return False
        elif [i,j] in GameState.REGIONS['COLS08']:
            if(self.__board[i + 1, j] in adot) and (self.__board[i - 1, j] in adot):
                return True
            else:
                return False

        elif [i,j] in GameState.REGIONS['CORE']:
            # Фигура находится просто в поле
            return self.DotFieldDeletable(adot, i, j)

        return False

    def deleteFigures(self):
        '''Удаляет фигуры'''
        for i in range(RC_NUMBER):
            for j in range(RC_NUMBER):
                # print(f'i={i} j={j}')

                if self.__Turn:
                    if self.__board[i,j] == 1:
                        if self.KingDeletable(i,j):
                            self.__board[i,j] = 0

                    if self.__board[i,j] == 2:
                        if self.DefenderDeletable(i,j):
                            self.__board[i,j] = 0
                else:
                    if self.__board[i,j] == 3:
                        if self.AttackerDeletable(i,j):
                            self.__board[i,j] = 0

    def checkWinCondition(self):
        '''Проверка __board
        Выирыш защитников - король на поле, 0 фигур аткаующих или король в области выходов. Код 0.
        Выигрыш атакующих - короля нет на поле. Код 1
        Игра в процессе. Код 0'''
        a = np.count_nonzero(self.__board == 1) # считаем количество королей на поле
        pass


    def isFieldCell(self,i,j):
        '''Определяет ячейка не выхода и не трон'''
        if ([i,j] not in GameState.REGIONS['THRONE']) and ([i,j] not in GameState.REGIONS['CORNERS']):
            return True
        else:
            return False

    def getDotMoves(self,i,j,moves):
        '''Определяет все движения для простой фигуры атакющего или защищающегося'''
        # Определим условия попадания на края карты и на трон
        c1 = i
        # Движение по столбцу вверх(то есть движение по строкам к 0) от фигуры
        for x in range(i - 1, -1, -1):
            if self.__board[x, j] == 0:
                if self.isFieldCell(x,j):
                    moves.append(Move((i, j), (x, j), self.__board))
            else:
                break
        # Движение по столбцу виниз(то есть движение по строкам к RC_NUMBER) от фигуры
        for x in range(i + 1, RC_NUMBER, 1):
            if self.__board[x, j] == 0:
                if self.isFieldCell(x, j):
                    moves.append(Move((i, j), (x, j), self.__board))
            else:
                break
        # Движение по строке влево(то есть движение по столбцам к 0) от фигуры
        for x in range(j - 1, -1, -1):
            if self.__board[i, x] == 0:
                if self.isFieldCell(i, x):
                    moves.append(Move((i, j), (i, x), self.__board))
            else:
                break
        # Движение по строке вправо(то есть движение по столбцам к RC_NUMBER) от фигуры
        for x in range(j + 1, RC_NUMBER, 1):
            if self.__board[i, x] == 0:
                if self.isFieldCell(i, x):
                    moves.append(Move((i, j), (i, x), self.__board))
            else:
                break

    def getAttackerMoves(self,i,j,moves):

            self.getDotMoves(i,j,moves)


    def getDefenderMoves(self,i,j,moves):

            self.getDotMoves(i,j,moves)


    def getKingMoves(self, i, j, moves):
        maxr = max(RC_NUMBER, i+3)
        minr = min(0, i-3)
        maxc = max(RC_NUMBER, j+3)
        minc = min(0, j-3)

        # Движение по столбцу вверх от короля (по строкам к minr)
        for x in range(i - 1, minr, -1):
            if self.__board[x, j] == 0:
                moves.append(Move((i, j), (x, j), self.__board))
            else:
                break
        # Движение по столбцу вниз от короля (по строкам к maxr)
        for x in range(i + 1, maxr, 1):
            if self.__board[x, j] == 0:
                moves.append(Move((i, j), (x, j), self.__board))
            else:
                break
        # Движение по строке вправо от короля (по строкам к minc)
        for x in range(j - 1, minc, -1):
            if self.__board[i, x] == 0:
                moves.append(Move((i, j), (i, x), self.__board))
            else:
                break
        # Движение по строке вправо от короля (по строкам к maxc)
        for x in range(j + 1, maxc, 1):
            if self.__board[i, x] == 0:
                moves.append(Move((i, j), (i, x), self.__board))
            else:
                break

    def highlightCells(self, screen, validMoves: list, sqSelected: tuple):
        if sqSelected != ():
            i, j = sqSelected
            if self.get_board()[i, j] == (1 if self.get_turn() else 3) or self.get_board()[i, j] == (2 if self.get_turn() else 3): # проверка: выбранная нами ячейка, содержит фигуру в соответствующий ход
                s = pygame.Surface((GRID_STEP_SIZE, GRID_STEP_SIZE))
                s.set_alpha(100)  # прозрачность: если 0 то полностью прозрачный, если 255 то непрозрачный
                s.fill(COLORS['HIGHLIGHT_BLUE'])
                screen.blit(s, (GRID_INIT_POS[0] + j*GRID_STEP_SIZE, GRID_INIT_POS[1] + i*GRID_STEP_SIZE))
                # Выше мы подсветили выбранную ячейку, далее подсветим ячейки допустимые к ходу с этой ячейками
                s.fill(COLORS['HIGHLIGHT_YELLOW'])
                for move in validMoves:
                    if move.startRow == i and move.startCol == j:
                        screen.blit(s, (GRID_INIT_POS[0]+GRID_STEP_SIZE * move.endCol, GRID_INIT_POS[1]+GRID_STEP_SIZE * move.endRow))


    def DrawFigures(self, screen):
        for i in range(RC_NUMBER):
            for j in range(RC_NUMBER):
                pos = [GRID_INIT_POS[0] + GRID_STEP_SIZE*j, GRID_INIT_POS[1] + GRID_STEP_SIZE*i]

                if self.__board[i,j] == 3:
                    # pygame.gfxdraw.circle(screen,pos[0],pos[1],5,color=COLORS['THRONE'])
                    screen.blit(IMAGES['attacker'], pygame.Rect(pos,(int(Screen_width*0.05), int(Screen_width*0.05))))
                if self.__board[i,j] == 2:
                    screen.blit(IMAGES['defender'],
                                pygame.Rect(pos, (int(Screen_width * 0.05), int(Screen_width * 0.05))))
                if self.__board[i,j] == 1:
                    screen.blit(IMAGES['king'],
                                pygame.Rect(pos, (int(Screen_width * 0.05), int(Screen_width * 0.05))))

# def highlightCells(screen, gs : GameState, validMoves : list, sqSelected : tuple):
#     if sqSelected != ():
#         i,j = sqSelected
#         if gs.get_board()[i,j] == (1 or 2 if gs.get_turn() else 3): #проверка: выбранная нами ячейка, содержит фигуру в соответствующий ход
#             s = pygame.Surface((GRID_STEP_SIZE,GRID_STEP_SIZE))
#             s.set_alpha(100) #прозрачность: если 0 то полностью прозрачный, если 255 то непрозрачный
#             s.fill(COLORS['HIGHLIGHT'])
#             screen.blit(s, (i*GRID_STEP_SIZE, j*GRID_STEP_SIZE))
#             #Выше мы подсветили выбранную ячейку, далее подсветим ячейки допустимые к ходу с этой ячейками
#             s.fill(COLORS['HIGHLIGHT'])
#             for move in validMoves:
#                 if move.startRow == i and move.startCol == j:
#                     screen.blit(s,(GRID_STEP_SIZE*move.endRow, GRID_STEP_SIZE*move.endCol))


