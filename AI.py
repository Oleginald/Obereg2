from PreProc import *
from Engine import *

import random

class AI():


    # 1 - король, 2 - защитник, 3 - атакующий
    SCORES = {1 : 10000, 2 : 5, 3 : -5, 'inf' : 999999}

    def findRandomMove(self,validMoves):
        '''AI выбирает ход из всех доступных ходов псевдо-случайно'''
        return validMoves[random.randrange(len(validMoves)-1)]

    def evaluate(self, gs : GameState):
        '''Оценивает игровую доску'''
        value = 0 # наша оценка состояния

        # Если король находится в углу - это + к value (выгода защитников)
        # Проходимся по всем 4-м углам
        # for cell in GameState.REGIONS['CORNERS']:
        #     if gs.get_board()[cell[0],cell[1]] == 1:
        #         value += AI.SCORES[1]
        #         break

        if gs.get_board()[0, 0] == 1 or gs.get_board()[0, 8] == 1 or gs.get_board()[8, 0] == 1 or gs.get_board()[8, 8] == 1:
            value += AI.SCORES[1]

        # Если короля нет на доске, то это - к value (выгода атакующих)
        KingCount = np.count_nonzero(gs.get_board() == 1)
        value -= KingCount*AI.SCORES[1] # если короля нет, то вычитаем 0 раз, если есть, то вычитаем 1 раз

        # Подсчитываем количество атакующих и защитников
        defenders = np.count_nonzero(gs.get_board() == 2)
        attackers = np.count_nonzero(gs.get_board() == 3)
        value += defenders*AI.SCORES[2]
        value += attackers*AI.SCORES[3]

        return value

    def findBestMove(self, gs : GameState, validMoves ,screen, clock):
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
