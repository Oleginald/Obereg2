import sys

import pygame

from PreProc import *
from Engine import *
from AI import *

def start():
    '''Начальное окно взаимодействия с пользователем'''

    root = Tk()
    root.title("GUI на Python")
    root.geometry("300x250")

    var = IntVar()
    chk = Checkbutton(root, text='foo', variable=var)
    chk.pack(side=LEFT)
    var.get()  # unchecked
    print(f'var={var}')
    def click_button():
        mainres = main(True, True)
        if mainres == 0:
            print(f'ffff')

    btn = Button(text="Click Me", background="#555", foreground="#ccc",
                 padx="20", pady="8", font="16", command=click_button)
    btn.pack()

    root.mainloop()

def main(player1 : bool, player2 : bool):

    os.environ["SDL_VIDEO_CENTERED"] = '1'

    pygame.init()
    pygame.display.set_caption('Оберег')
    screen = pygame.display.set_mode((Screen_width, Screen_height))
    clock = pygame.time.Clock()

    pygame.display.update()

    gs = GameState()
    ai = AI()

    validMoves = gs.getValidMoves() # Список по которому будем чекать, можно ли так ходить или нет
    moveMade = False # Если игрок сделал правильный ход, то мы будем генерировать новый список validMoves, и флаг будет True.
    animate = True # Если True, то анимация включена, если False, то нет
    gameOver = False

    running = True
    cellSelected = () # Флаг - выбрана ячейка или нет. Изначально ничего не выделено
    playerClicks = [] #
    win_condition = 0


    # Инициализируем элементы GUI
    hlDefenders = Backlighter((0.215 * Screen_width, 0.65 * Screen_width), (0.02 * Screen_width, 0.02 * Screen_width), COLORS['ATTACKER'])
    hlAttackers = Backlighter((0.75 * Screen_width, 0.65 * Screen_width), (0.02 * Screen_width, 0.02 * Screen_width), COLORS['DEFENDER'])


    while running:
        screen.fill(COLORS['BACKGROUND'])
        humanTurn = (not gs.get_turn() and player1) or (gs.get_turn() and player2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if not gameOver and humanTurn:


                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    # Для того, чтобы перейти в систему отсчета связанную с представлением нашего поля, где первый индекс
                    # соответствует rows, а второй columns (в pygame my идет вдоль rows, а mx идет вдоль columns)
                    # далее поменем местами координат pygame местами
                    mFy = -GRID_INIT_POS[0] + mx # Конкретно здесь выступает как rows
                    mFx = -GRID_INIT_POS[1] + my # Конкретно здесь выступает как cols
                    Xind = int(mFx // GRID_STEP_SIZE)
                    Yind = int(mFy // GRID_STEP_SIZE)

                    # Установим ограничитель индексов. Именно индексов - не ограничиваю здесь возможность кликов. Пока что ограничу наивным образом. В дальнейшем это может работать не верно при работе мышкой за полем.
                    if Xind > 8:
                        Xind = 8
                    if Xind < 0:
                        Xind = 0
                    if Yind > 8:
                        Yind = 8
                    if Yind < 0:
                        Yind = 0

                    if cellSelected == (Xind, Yind):
                        cellSelected = ()
                        playerClicks = []
                    else:
                        cellSelected = (Xind, Yind)
                        playerClicks.append(cellSelected)
                    if len(playerClicks) == 2:
                        move = Move(playerClicks[0], playerClicks[1], gs.get_board())
                        if move in validMoves:
                            gs.makeMove(move, screen, clock, animate, True)
                            moveMade = True
                            cellSelected = () # обнуляет клики пользователя
                            playerClicks = []
                        else:
                            playerClicks = [cellSelected] # сохраняем последний клик, для того

                # Почему-то все функции перестали работать
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z: # Отменяем последний ход, нажатием на кнопку z
                        gs.undoMove()
                        validMoves = gs.getValidMoves()
                        moveMade = False


        # AI
        if not gameOver and not humanTurn:
            AIMove = ai.findBestMove(3, gs, validMoves, screen, clock)
            if AIMove is None: # Если по какой-то причине не был найден оптимальный ход, то ход рандомный
                AIMove = ai.findRandomMove(validMoves)
            gs.makeMove(AIMove,screen,clock,animate, True)
            moveMade = True

        if moveMade:
            # print(f'Move made')
            validMoves = gs.getValidMoves()
            moveMade = False


        if gs.get_win():
            gameOver = True
            if not gs.get_turn():
                drawText(screen, 'Defenders win by the King out', (0.36 * Screen_width, 0.64 * Screen_width), (0.3 * Screen_width, 0.1 * Screen_width), COLORS['FONT_LOWER'], int(0.025*Screen_width))
            else:
                drawText(screen, 'Attackers win by eating the King', (0.36 * Screen_width, 0.64 * Screen_width), (0.3 * Screen_width, 0.1 * Screen_width), COLORS['FONT_LOWER'], int(0.025*Screen_width))

        #Отображение и GUI
        pgDrawField(screen, gs.get_turn())



        gs.highlightCells(screen,validMoves,cellSelected)
        gs.DrawFigures(screen)

        pygame.display.flip()

    clock.tick(FPS)
    pygame.quit()
    return 0

if __name__ == "__main__":
    start()
    # main(True, True)