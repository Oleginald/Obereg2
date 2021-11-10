from PreProc import *
from Engine import *
from AI import *

def start():
    '''Начальное окно взаимодействия с пользователем'''
    try:
        root = Tk()
        root.title("Obereg launcher")
        root.geometry("300x120")

        global player1
        global player2
        player1 = True
        player2 = True

        def isChecked1():

            global player1
            if var1.get() == True:
                player1 = False
            else:
                player1 = True

        def isChecked2():

            global player2
            if var2.get() == True:
                player2 = False
            else:
                player2 = True


        var1 = BooleanVar()
        chk1 = Checkbutton(root, text='Выберите, если за 1-го игрока играет ИИ', variable=var1, onvalue=True, offvalue=False, command=isChecked1)
        chk1.deselect()
        chk1.pack()

        var2 = BooleanVar()
        chk2 = Checkbutton(root, text='Выберите, если за 2-го игрока играет ИИ', variable=var2, onvalue=True, offvalue=False, command=isChecked2)
        chk2.deselect()
        chk2.pack()


        def click_button():

            mainres = main(player1, player2, False)
            if mainres == 0:
                sys.exit()
                print(f'Программа завершено успешно.')

        btn = Button(text="Начать игру",
                     padx="20", pady="8", font="16", command=click_button)
        btn.pack()

        root.mainloop()
    except BaseException:
        print(f'')

def main(player1 : bool, player2 : bool, reset : bool):

    os.environ["SDL_VIDEO_CENTERED"] = '1'

    pygame.init()
    pygame.display.set_caption('Оберег')
    screen = pygame.display.set_mode((Screen_width, Screen_height))
    clock = pygame.time.Clock()

    pygame.display.set_icon(IMAGES['king'])
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

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:  # Отменяем последний ход, нажатием на кнопку z
                    gs.set_win(False)
                    gameOver = False
                    gs.undoMove()
                    validMoves = gs.getValidMoves()
                    moveMade = False
                if event.key == pygame.K_r:  # Ресетим игру, нажатием на кнопку r
                    gs.set_win(False)
                    gameOver = False
                    gs.reset()
                    validMoves = gs.getValidMoves()
                    moveMade = False
                    humanTurn = (not gs.get_turn() and player1) or (gs.get_turn() and player2)
                    playerClicks = []
                    cellSelected = ()
                if event.key == pygame.K_F1: # смена типа игрока1
                    player1 = not player1
                if event.key == pygame.K_F2: # смена типа игрока2
                    player2 = not player2

        # AI
        if not gameOver and not humanTurn:
            AIMove = ai.findBestMove(3, gs, validMoves, screen, clock)
            if AIMove is None:  # Если по какой-то причине не был найден оптимальный ход, то ход рандомный
                AIMove = ai.findRandomMove(validMoves)
            gs.makeMove(AIMove, screen, clock, animate, True)
            moveMade = True


        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False




        #Отображение и GUI
        pgDrawField(screen, gs.get_turn())



        gs.highlightCells(screen,validMoves,cellSelected)
        gs.DrawFigures(screen)

        if gs.get_win():
            gameOver = True

            if not gs.get_turn():

                drawText(screen, 'Defenders win by the King out', (0.36 * Screen_width, 0.64 * Screen_width), (0.3 * Screen_width, 0.1 * Screen_width), COLORS['FONT_LOWER'], int(0.025*Screen_width))
            else:

                drawText(screen, 'Attackers win by eating the King', (0.36 * Screen_width, 0.64 * Screen_width), (0.3 * Screen_width, 0.1 * Screen_width), COLORS['FONT_LOWER'], int(0.025*Screen_width))
                pygame.draw

        pygame.display.flip()

    clock.tick(FPS)
    pygame.quit()
    return 0

if __name__ == "__main__":
    start()
    # main(True, False, False)