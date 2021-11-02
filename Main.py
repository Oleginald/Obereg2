import pygame

from PreProc import *
from Engine import *


def main():

    os.environ["SDL_VIDEO_CENTERED"] = '1'

    pygame.init()
    pygame.display.set_caption('Geometry test')
    screen = pygame.display.set_mode((Screen_width, Screen_height))
    clock = pygame.time.Clock()

    pygame.display.update()

    gs = GameState()

    validMoves = gs.getValidMoves() # Список по которому будем чекать, можно ли так ходить или нет
    moveMade = False # Если игрок сделал правильный ход, то мы будем генерировать новый список validMoves, и флаг будет True.

    running = True
    cellSelected = () # Флаг - выбрана ячейка или нет. Изначально ничего не выделено
    playerClicks = [] #
    while running:
        screen.fill(COLORS['BACKGROUND'])
        # print(buttonExit.get_flag())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                mFx = -GRID_INIT_POS[0] + mx # Конкретно здесь выступает как rows
                mFy = -GRID_INIT_POS[1] + my # Конкретно здесь выступает как cols
                Xind = int(mFx // GRID_STEP_SIZE)
                Yind = int(mFy // GRID_STEP_SIZE)

                # print([Xind, Yind])
                if cellSelected == (Xind, Yind):
                    cellSelected = ()
                    playerClicks = []
                else:
                    cellSelected = (Xind, Yind)
                    playerClicks.append(cellSelected)
                if len(playerClicks) == 2:
                    # print(playerClicks)
                    move = Move(playerClicks[0], playerClicks[1], gs.get_board())
                    print(move.constructMove())
                    if move in validMoves:
                        print(validMoves)
                        gs.makeMove(move)
                        moveMade = True


                    cellSelected = ()
                    playerClicks = []

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z: # Отменяем последний ход, нажатием на кнопку K_z
                    gs.undoMove()
                    gs.getValidMoves()

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        pgDrawField(screen)
        gs.DrawFigures(screen)

        pygame.display.flip()

    clock.tick(FPS)
    pygame.quit()


if __name__ == "__main__":
    main()