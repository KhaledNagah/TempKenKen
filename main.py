from cProfile import run
from AC import *
from board import board
from coordinate import Coordinate
from constraint import Arithmetic_Constraint
from boardgeneration import *
from backtrack import Back_Track
from backtrackFC import Back_Track_FC
from gui import *


# size parametrized
global size_of_board
size_of_board = 6


# generate board
b5 = createBoard(size_of_board)
print(b5.get_size())

coordinates= b5.coordinates


### RUNNING SECTION ###
run = True
val = 0
solved = 0
while run:
    instruction()

    # Events
    for event in pygame.event.get():

		# Quit the game window
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            ## ENTER NUMBER FROM KEY BOARD TO GENERATE BOARD WITH THIS SIZE
            if event.key == pygame.K_1:
                #global size_of_board
                size_of_board = 1
                b5 = createBoard(size_of_board)
                draw_gen_board(b5)
                pygame.display.update()
                val = 0

            if event.key == pygame.K_2:
                size_of_board = 2
                b5 = createBoard(size_of_board)
                draw_gen_board(b5)
                pygame.display.update()
                val = 0

            if event.key == pygame.K_3:
                size_of_board = 3
                b5 = createBoard(size_of_board)
                draw_gen_board(b5)
                pygame.display.update()
                val = 0

            if event.key == pygame.K_4:
                size_of_board = 4
                b5 = createBoard(size_of_board)
                draw_gen_board(b5)
                pygame.display.update()
                val = 0

            if event.key == pygame.K_5:
                size_of_board = 5
                b5 = createBoard(size_of_board)
                draw_gen_board(b5)
                pygame.display.update()
                val = 0

            if event.key == pygame.K_6:
                size_of_board = 6
                b5 = createBoard(size_of_board)
                draw_gen_board(b5)
                pygame.display.update()
                val = 0

            if event.key == pygame.K_7:
                size_of_board = 7
                b5 = createBoard(size_of_board)
                draw_gen_board(b5)
                pygame.display.update()
                val = 0

            if event.key == pygame.K_8:
                size_of_board = 8
                b5 = createBoard(size_of_board)
                draw_gen_board(b5)
                pygame.display.update()
                val = 0

            if event.key == pygame.K_9:
                size_of_board = 9
                b5 = createBoard(size_of_board)
                draw_gen_board(b5)
                pygame.display.update()  
                val = 0


            # If R pressed clear the sudoku board
            if event.key == pygame.K_r:
                draw_gen_board(b5)
                pygame.display.update()
                val = 0

            # If N is pressed generate new board with same size
            if event.key == pygame.K_n:
                b5 = createBoard(size_of_board)
                draw_gen_board(b5)
                pygame.display.update()
                val = 0

            ## ENTER ALGORITHM NUMBER TO BE SOLVED A OR B OR C
            if event.key == pygame.K_a:
                val = 1 ## for backtracking

            if event.key == pygame.K_b:
                val = 2 ## for backtrackingFC
                
            if event.key == pygame.K_c:
                val = 3 ## for Arc Consistency

              
            ## PRESS ENTER TO GENERATE        
            if event.key == pygame.K_RETURN:
                draw_gen_board(b5)
                pygame.display.update()
                val = 0    


    # Draw board and update

    if(val != 0):
        if(val == 1):
            bt=Back_Track(b5)
            bt.solve()

        if(val == 2):
            bt_fc=Back_Track_FC(b5)
            bt_fc.solve()
        
        if(val == 3 and solved == 0):
            bt_ac=AC(b5)
            bt_ac.solve()
            solved = 1
            pygame.time.delay(1000)
    pygame.display.update()
    pygame.time.delay(1500)
pygame.quit()




