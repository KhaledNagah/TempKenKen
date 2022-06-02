from cProfile import run
from board import board
from coordinate import Coordinate
from constraint import Arithmetic_Constraint
from boardgeneration import *
import copy

#from backtrack import Back_Track

# import pygame library
import pygame

# initialise the pygame font
pygame.font.init()



# Total window
parameter = 600
# default param = 500 and length = 600
screen = pygame.display.set_mode((parameter, 750))

# Title and Icon
pygame.display.set_caption("KENKEN SOLVER!")

# Default Kenken Board is 4.
sizeBoard = 4
dif = parameter / (sizeBoard)



# Load test fonts for future use
font1 = pygame.font.SysFont("comicsans", 40)
font2 = pygame.font.SysFont("comicsans", 20)

def get_cord(pos):
	global x
	x = pos[0]//dif
	global y
	y = pos[1]//dif

# Draw box function
def draw_box(x, y, thickness):
	for i in range(2):
		pygame.draw.line(screen, (0, 0, 0), (x * dif-3, (y + i)*dif), (x * dif + dif + 3, (y + i)*dif), thickness)
		pygame.draw.line(screen, (0, 0, 0), ( (x + i)* dif, y * dif ), ((x + i) * dif, y * dif + dif), thickness)


# Test Draw
def draw_constraint(x, y, sum, i, flag):
    # Draw colored box based on i 
    pygame.draw.rect(screen, ((40+(60 * i)) % 255, (40+(60 * i)) % 255, (40+(60 * i)) % 255), (x * dif, y * dif, dif + 1, dif + 1))
    draw_box(x,y,1)

    # Text to be written +num for the first coordinate only
    if(flag):
        text2 = font2.render("+" + str(sum), 1, (255, 0, 0))
        screen.blit(text2, (x * dif + 15, y * dif + 15))
        draw_box(x,y,1)





# Function to draw required lines for making generated default board		
def draw_gen_board(board):
    # Get size of the board
    global sizeBoard 
    sizeBoard = board.get_size()
    global dif 
    dif = parameter / (sizeBoard)

    # Draw lines horizontally and vertically to form grid		
    for i in range(sizeBoard):
        thick = 1
        pygame.draw.line(screen, (0, 0, 0), (0, i * dif), (parameter, i * dif), thick)
        pygame.draw.line(screen, (0, 0, 0), (i * dif, 0), (i * dif, parameter), thick)

    # Adding constraints to the board
    constraints = board.get_constraints()
    counter = 1 # counter used in coloring different constraints with the different color
    for i in constraints:
        coordinates = i.get_coordinates()
        flag = 1
        for j in coordinates:
            draw_constraint(j.get_x(), j.get_y(), i.get_sum(), counter, flag)
            flag = 0

        counter = counter + 1




# Function to draw the board with values		
def draw_board(board):
    # Get size of the board
    global sizeBoard 
    sizeBoard = board.get_size()
    global dif 
    dif = parameter / (sizeBoard)

    # Draw lines horizontally and vertically to form grid		
    for i in range(sizeBoard):
        thick = 1
        pygame.draw.line(screen, (0, 0, 0), (0, i * dif), (parameter, i * dif), thick)
        pygame.draw.line(screen, (0, 0, 0), (i * dif, 0), (i * dif, parameter), thick)

    # Adding constraints to the board
    constraints = board.get_constraints()
    counter = 1 # counter used in coloring different constraints with the different color
    for i in constraints:
        coordinates = i.get_coordinates()
        flag = 1
        for j in coordinates:
            draw_constraint(j.get_x(), j.get_y(), i.get_sum(), counter, flag)
            flag = 0

        counter = counter + 1

    # Draw grid of the board 
    for i in range (sizeBoard):
        for j in range (sizeBoard):
            # Fill the board with values of coordinates
            text1 = font1.render(str(board.get_coordinate(i,j).get_value()), 1, (0, 0, 255))
            screen.blit(text1, (i * dif + 60, j * dif + 15))



# Update Value
def update_value(board, x, y, value):
    # Fill the board with values of coordinates
    text1 = font1.render(str(board.set_coordinate_value(x,y).set_value(value)), 1, (0, 0, 0))
    screen.blit(text1, (x * dif + 75, y * dif + 15))

# Display instruction for the game
# def instruction():
# 	text1 = font2.render("PRESS R TO RESET, N to RE-GENERATE!", 1, (255, 0, 0))
# 	text2 = font2.render("ENTER ALGORITHM: PRESS A, B or C TO SOLVE!", 1, (255, 0, 0))
# 	screen.blit(text1, (20, 620))	
# 	screen.blit(text2, (20, 670))
    
def instruction():
    text1 = font2.render("PRESS 3,4,5,...,etc TO ENTER SIZE!", 1, (255, 0, 0))
    text2 = font2.render("PRESS R TO RESET, N to RE-GENERATE!", 1, (255, 0, 0))
    text3 = font2.render("ENTER ALGORITHM: PRESS A, B or C TO SOLVE!", 1, (255, 0, 0))
    
    screen.blit(text1, (20, 610))
    screen.blit(text2, (20, 660))
    screen.blit(text3, (20, 710))	
	
	






# Display options when solved
def result():
	text1 = font1.render("FINISHED PRESS R or D", 1, (0, 0, 0))
	screen.blit(text1, (20, 650))


"""TESTING"""

# """TEST 1"""
# b=board(3)

# cons1 = Arithmetic_Constraint([b.get_coordinate(0,0),b.get_coordinate(0,1)],3)
# cons2 = Arithmetic_Constraint([b.get_coordinate(0,2),b.get_coordinate(1,1),b.get_coordinate(1,2)],7)
# cons3 = Arithmetic_Constraint([b.get_coordinate(2,1),b.get_coordinate(2,2)],3)
# cons4 = Arithmetic_Constraint([b.get_coordinate(1,0),b.get_coordinate(2,0)],5)

# b.get_coordinate(0,0).add_constraint(cons1)
# b.get_coordinate(0,1).add_constraint(cons1)
# b.get_coordinate(0,2).add_constraint(cons2)
# b.get_coordinate(1,0).add_constraint(cons4)
# b.get_coordinate(1,1).add_constraint(cons2)
# b.get_coordinate(1,2).add_constraint(cons2)
# b.get_coordinate(2,0).add_constraint(cons4)
# b.get_coordinate(2,1).add_constraint(cons3)
# b.get_coordinate(2,2).add_constraint(cons3)


# b.add_constraint(cons1)
# b.add_constraint(cons2)
# b.add_constraint(cons3)
# b.add_constraint(cons4)



######################################
# b=board(4)

# cons1 = Arithmetic_Constraint([b.get_coordinate(0,0),b.get_coordinate(1,0)],4)
# cons2 = Arithmetic_Constraint([b.get_coordinate(0,1),b.get_coordinate(0,2),b.get_coordinate(1,1)],8)
# cons3 = Arithmetic_Constraint([b.get_coordinate(0,3),b.get_coordinate(1,3)],5)
# cons4 = Arithmetic_Constraint([b.get_coordinate(2,0),b.get_coordinate(2,1)],7)
# cons5 = Arithmetic_Constraint([b.get_coordinate(1,2),b.get_coordinate(2,2),b.get_coordinate(2,3)],6)
# cons6 = Arithmetic_Constraint([b.get_coordinate(3,0),b.get_coordinate(3,1),b.get_coordinate(3,2)],7)
# cons7 = Arithmetic_Constraint([b.get_coordinate(3,3)],3)


# b.get_coordinate(0,0).add_constraint(cons1)
# b.get_coordinate(0,1).add_constraint(cons2)
# b.get_coordinate(0,2).add_constraint(cons2)
# b.get_coordinate(0,3).add_constraint(cons3)
# b.get_coordinate(1,0).add_constraint(cons1)
# b.get_coordinate(1,1).add_constraint(cons2)
# b.get_coordinate(1,2).add_constraint(cons5)
# b.get_coordinate(1,3).add_constraint(cons3)
# b.get_coordinate(2,0).add_constraint(cons4)
# b.get_coordinate(2,1).add_constraint(cons4)
# b.get_coordinate(2,2).add_constraint(cons5)
# b.get_coordinate(2,3).add_constraint(cons5)
# b.get_coordinate(3,0).add_constraint(cons6)
# b.get_coordinate(3,1).add_constraint(cons6)
# b.get_coordinate(3,2).add_constraint(cons6)
# b.get_coordinate(3,3).add_constraint(cons3)

# b.add_constraint(cons1)
# b.add_constraint(cons2)
# b.add_constraint(cons3)
# b.add_constraint(cons4)
# b.add_constraint(cons5)
# b.add_constraint(cons6)
# b.add_constraint(cons7)

# #######################
# b1=board(4)

# cons1 = Arithmetic_Constraint([b1.get_coordinate(0,0),b1.get_coordinate(1,0)],4)
# cons2 = Arithmetic_Constraint([b1.get_coordinate(0,1),b1.get_coordinate(0,2),b1.get_coordinate(1,1)],8)
# cons3 = Arithmetic_Constraint([b1.get_coordinate(0,3),b1.get_coordinate(1,3)],5)
# cons4 = Arithmetic_Constraint([b1.get_coordinate(2,0),b1.get_coordinate(2,1)],7)
# cons5 = Arithmetic_Constraint([b1.get_coordinate(1,2),b1.get_coordinate(2,2),b1.get_coordinate(2,3)],6)
# cons6 = Arithmetic_Constraint([b1.get_coordinate(3,0),b1.get_coordinate(3,1),b1.get_coordinate(3,2)],7)
# cons7 = Arithmetic_Constraint([b1.get_coordinate(3,3)],3)


# b1.get_coordinate(0,0).add_constraint(cons1)
# b1.get_coordinate(0,1).add_constraint(cons2)
# b1.get_coordinate(0,2).add_constraint(cons2)
# b1.get_coordinate(0,3).add_constraint(cons3)
# b1.get_coordinate(1,0).add_constraint(cons1)
# b1.get_coordinate(1,1).add_constraint(cons2)
# b1.get_coordinate(1,2).add_constraint(cons5)
# b1.get_coordinate(1,3).add_constraint(cons3)
# b1.get_coordinate(2,0).add_constraint(cons4)
# b1.get_coordinate(2,1).add_constraint(cons4)
# b1.get_coordinate(2,2).add_constraint(cons5)
# b1.get_coordinate(2,3).add_constraint(cons5)
# b1.get_coordinate(3,0).add_constraint(cons6)
# b1.get_coordinate(3,1).add_constraint(cons6)
# b1.get_coordinate(3,2).add_constraint(cons6)
# b1.get_coordinate(3,3).add_constraint(cons3)

# b1.add_constraint(cons1)
# b1.add_constraint(cons2)
# b1.add_constraint(cons3)
# b1.add_constraint(cons4)
# b1.add_constraint(cons5)
# b1.add_constraint(cons6)
# b1.add_constraint(cons7)

# b1.set_coordinate_value(1,2,5)


# b5 = createBoard(7)


# ### RUNNING SECTION ###
# run = True
# Reset = 1
# flag2 = 0
# while run:
#     # Background
#     #screen.fill((255,255,255))

#     # Events
#     for event in pygame.event.get():
# 		# Quit the game window
#         if event.type == pygame.QUIT:
#             run = False

#         if event.type == pygame.KEYDOWN:
#             # If R pressed clear the sudoku board
#             if event.key == pygame.K_r:
#                 draw_gen_board(b5)
#                 pygame.display.update()
#                 val = 0

#                 Reset = 1

#             if event.key == pygame.K_n:
#                 b5 = createBoard(7)
#                 draw_gen_board(b5)
#                 pygame.display.update()

#                 Reset = 1    

#             if event.key == pygame.K_1:
#                 val = 1 ## for backtracking

#             if event.key == pygame.K_2:
#                 val = 2 ## for backtrackingFC
                
#             if event.key == pygame.K_3:
#                 val = 3 ## for third Alg
                    
#             if event.key == pygame.K_RETURN:
#                 draw_gen_board(b5)
#                 Reset = 0    


#     # Draw board and update

#     if(val != 0):
#         if(val == 1):
#             bt=Back_Track(b5)
#             bt.solve()

#         if(val == 2):
#             bt_fc=Back_Track_FC(b5)
#             bt_fc.solve()
   


#     # if(Reset == 0):
#     #     if(flag2 == 1):
#     #         draw_board(b1)
#     #         instruction()
#     #         pygame.display.update()
#     #         pygame.time.delay(300)
#     #         flag2 = 0

#     #     if(flag2 == 0):
#     #         draw_board(b)
#     #         instruction()
#     #         pygame.display.update()
#     #         pygame.time.delay(300)
#     #         flag2 = 1   
#     # else:
#     #     #draw_gen_board(b) 
#     #     instruction()
   

#     pygame.display.update()

# pygame.quit()
# #print((b.get_coordinate(0,0)).get_value())

