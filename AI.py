from PreProc import *
from Engine import *

import random

class AI():


    # 1 - король, 2 - защитник, 3 - атакующий
    SCORES = {1 : 10000, 2 : 5, 3 : -5, 'inf' : 999999}
    DEPTH = 4

    def findRandomMove(self,validMoves):
        '''AI выбирает ход из всех доступных ходов псевдо-случайно'''
        return validMoves[random.randrange(len(validMoves)-1)]

    def evaluate(self, gs : GameState):
        '''Оценивает игровую доску'''
                # Если король находится в углу - это + к value (выгода защитников)
        # Проходимся по всем 4-м углам
        # for cell in GameState.REGIONS['CORNERS']:
        #     if gs.get_board()[cell[0],cell[1]] == 1:
        #         value += AI.SCORES[1]
        #         break

        # Если король находится в углу - это высшая оценка для защитников
        if gs.get_board()[0, 0] == 1 or gs.get_board()[0, 8] == 1 or gs.get_board()[8, 0] == 1 or gs.get_board()[8, 8] == 1:
            return AI.SCORES[1]

        # Если короля нет на доске, то это лучшая оценка для атакующих
        KingCount = np.count_nonzero(gs.get_board() == 1)
        if KingCount == 0:
            return -AI.SCORES[1]

        # Подсчитываем количество атакующих и защитников
        defenders = np.count_nonzero(gs.get_board() == 2)
        attackers = np.count_nonzero(gs.get_board() == 3)
        value = 0  # наша оценка состояния
        value += defenders*AI.SCORES[2]
        value += attackers*AI.SCORES[3]

        return value

    def NaiveMinMax(self, gs : GameState, validMoves, screen, clock):
        '''Жадный алгоритм MinMax, очень жадный, слишком жадный.
        В данной реализации он просматривает на 2 хода вперед'''
        turnMultiplier = 1 if gs.get_turn() else -1

        oppinentMinMaxValue = AI.SCORES['inf']
        bestPlayerMove = None
        # playerMove - тот кто ходит сейчас
        # opponent - тот кто не ходит сейчас
        for playerMove in validMoves:
            gs.makeMove(playerMove,screen,clock,False,False)
            opponentMoves = gs.getValidMoves()
            random.shuffle(validMoves)
            opponentMaxValue = -AI.SCORES['inf']
            for opponentMove in opponentMoves:
                gs.makeMove(opponentMove,screen,clock,False,False)
                value = -turnMultiplier * self.evaluate(gs)
                # print(f'board value={value}')
                if (value > opponentMaxValue):
                    opponentMaxValue = value
                gs.undoMove()

            if opponentMaxValue < oppinentMinMaxValue:
                oppinentMinMaxValue = opponentMaxValue
                bestPlayerMove = playerMove
            gs.undoMove()

        return bestPlayerMove

    # @timing
    def findBestMove(self,key:int, gs : GameState, validMoves,screen,clock):
        global nextMove
        nextMove = None
        if key == 1:
            # Используем нерекурсивный минимакс
            nextMove = self.NaiveMinMax(gs,validMoves, screen, clock)
        if key == 2:
            # Используем рекурсивный минимакс
            self.RecursiveMinMax(AI.DEPTH, gs.get_turn(), gs, validMoves,screen,clock)
        if key == 3:
            self.RecursiveNegaMaxAlphaBeta(AI.DEPTH, -AI.SCORES['inf'], AI.SCORES['inf'], gs.get_turn(), gs, validMoves, screen, clock)
        return nextMove


    def RecursiveMinMax(self, depth : int, turn : bool, gs : GameState, validMoves, screen, clock):
        '''Чистый рекурсивный минимакс. можно не ложить validMoves в аргументы и заменить ее gs.getValidMoves.
        Но тогда получится, что мы делаем эту операцию 2 раза в Main'''
        global nextMove
        if depth == 0:
            return self.evaluate(gs)

        if turn:
            maxValue = -AI.SCORES['inf']
            for move in validMoves:
                gs.makeMove(move,screen,clock,False,False)
                nextMoves = gs.getValidMoves()
                value = self.RecursiveMinMax(depth-1, False, gs,nextMoves,screen,clock)
                if value > maxValue:
                    maxValue = value
                    if depth == AI.DEPTH:
                        nextMove = move
                gs.undoMove()
            return maxValue
        else:
            minValue = AI.SCORES['inf']
            for move in validMoves:
                gs.makeMove(move,screen,clock,False,False)
                nextMoves = gs.getValidMoves()
                value = self.RecursiveMinMax(depth-1, True, gs,nextMoves,screen,clock)
                if value < minValue:
                    minValue = value
                    if depth == AI.DEPTH:
                        nextMove = move
                gs.undoMove()
            return minValue


    def RecursiveNegaMaxAlphaBeta(self, depth : int, alpha, beta, turn:bool, gs : GameState, validMoves, screen, clock):
        global nextMove
        if depth == 0:
            return self.evaluate(gs)

        if turn:
            maxValue = -AI.SCORES['inf']
            for move in validMoves:
                gs.makeMove(move, screen, clock, False, False)
                nextMoves = gs.getValidMoves()
                value = self.RecursiveNegaMaxAlphaBeta(depth - 1, alpha, beta, False, gs, nextMoves, screen, clock)
                if value > maxValue:
                    maxValue = value
                    if depth == AI.DEPTH:
                        nextMove = move
                gs.undoMove()
                # Отсечение
                alpha = max(alpha, value)
                if beta <= alpha:
                    break
            return maxValue
        else:
            minValue = AI.SCORES['inf']
            for move in validMoves:
                gs.makeMove(move, screen, clock, False, False)
                nextMoves = gs.getValidMoves()
                value = self.RecursiveNegaMaxAlphaBeta(depth - 1, alpha, beta, True, gs, nextMoves, screen, clock)
                if value < minValue:
                    minValue = value
                    if depth == AI.DEPTH:
                        nextMove = move
                gs.undoMove()
                # Отсечение
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return minValue

