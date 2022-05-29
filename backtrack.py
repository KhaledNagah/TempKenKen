from board import board
from coordinate import Coordinate
from constraint import Arithmetic_Constraint
#from gui import *
import pygame
from gui import draw_board, instruction

class Back_Track:
    def __init__(self,board):
        self.board=board
        self.coordiantes=board.get_coordinates()

    #Checks if the board is solved
    def is_solved(self):
        #Checks that all Arithmetic Constraints are satisfied
        for constraint in self.board.get_constraints():
                    values = []
                    for coord in constraint.get_coordinates():
                        if (coord.get_value() == 0):  
                            return False
                        values.append(coord.get_value())
                    if (not constraint.is_constraint_satisfied(values)):
                        return False
        
        #Checks that all Row Constraints are satisfied
        for x in range(self.board.get_size()):
            row_coords=self.board.get_row(x)
            values = []
            for y in range(len(row_coords)):
                values.append(row_coords[y].get_value())
            
            if len(values) != len(set(values)):
                return False
        
        #Checks that all Column Constraints are satisified
        for x in range(self.board.get_size()):
            col_coords=self.board.get_colomn(x)
            values = []
            for y in range(len(col_coords)):
                values.append(col_coords[y].get_value())
            
            if len(values) != len(set(values)):
                return False

        return True    
    
    #Called externally to solve the board, it calls the inner_solve function that is recursive
    def solve(self):
        return self.inner_solve (0)


    def inner_solve(self,index): #index is the index of the current coordinate

        draw_board(self.board)
        instruction()
        pygame.display.update()
        pygame.event.pump()

        #pygame.time.delay(300)
        
        ##For debugging to show the values of the coordinates at each step
        # for coord in self.board.get_coordinates():
        #     print(coord.get_value())
        # print("################")
        
        #Always check at the beggining of this recursive function if the board is solved, hence return true
        if self.is_solved():
            return True

        #If the board is not solved
        else:
            #Get the coordinate with the given index
            current_coordinate=self.board.get_coordinate(int(index/self.board.get_size()),index%self.board.get_size())

            #For each value in the domain of the variable
            for value in self.board.get_domain():
                
                #All Values of coordinates after me must be zero, this must be done because in case of backtraking
                for i in range (index+1,self.board.get_size()*self.board.get_size()):
                    self.board.set_coordinate_value(int(i/self.board.get_size()),i%self.board.get_size(),0)

                #Assign a value to the coordinate
                current_coordinate.set_value(value)
            
                #Check if this assignment is valid
                
                #1 Check that the assignment satisfies the Row Constraint
                
                invalid_R=0 #If it is 1, then the row constraint is not satisfied, so try another value from the domain if the variable 
                for neighbour_coordinate in self.board.get_row(current_coordinate.get_x()):
                    if ((current_coordinate.get_x()!=neighbour_coordinate.get_x()) or (current_coordinate.get_y()!=neighbour_coordinate.get_y())):
                        if current_coordinate.get_value()==neighbour_coordinate.get_value():
                            invalid_R=1
                            break
                if invalid_R==1:
                    continue

                #2 Check that the assignment satisfies the Colomn Constraint
                invalid_C=0 #If it is 1, then the colomn constraint is not satisfied, so try another value from the domain if the variable 
                for neighbour_coordinate in self.board.get_colomn(current_coordinate.get_y()):
                    if ((current_coordinate.get_x()!=neighbour_coordinate.get_x()) or (current_coordinate.get_y()!=neighbour_coordinate.get_y())):
                        if current_coordinate.get_value()==neighbour_coordinate.get_value():
                            invalid_C=1
                            break
                if invalid_C==1:
                    continue
                #3 Check that the assignment satisfies the Arithmetic Constraint
                
                #Get the arithmetic constraint object of the coordinate
                current_coordinate_constraint=current_coordinate.get_constraint()

                #Calculate the sum of values of the coordinates in this constraint
                sum=0
                for neighbour_coordinate in current_coordinate_constraint.get_coordinates():
                    real_neighbour_coordinate=self.board.get_coordinate(neighbour_coordinate.get_x(),neighbour_coordinate.get_y())
                    sum+=real_neighbour_coordinate.get_value()

                #If the sum is smaller than or equal the required arithmetic constraint sum, then this assignment is valid, so continue to the
                #next coordinate by calling the recusrive function inner_solve
                if(sum<=current_coordinate_constraint.get_sum()):
                    result=self.inner_solve(index+1)
                    #If result is 0, so try another value from the domain of the variable, if all domains are tried, return 0
                    if result != 0:
                        return 1
                        
            return 0
                            

"""TESTING"""

"""TEST 1"""
#b=board(3)
#
#cons1 = Arithmetic_Constraint([b.get_coordinate(0,0),b.get_coordinate(0,1)],3)
#cons2 = Arithmetic_Constraint([b.get_coordinate(0,2),b.get_coordinate(1,1),b.get_coordinate(1,2)],7)
#cons3 = Arithmetic_Constraint([b.get_coordinate(2,1),b.get_coordinate(2,2)],3)
#cons4 = Arithmetic_Constraint([b.get_coordinate(1,0),b.get_coordinate(2,0)],5)
#
#b.get_coordinate(0,0).add_constraint(cons1)
#b.get_coordinate(0,1).add_constraint(cons1)
#b.get_coordinate(0,2).add_constraint(cons2)
#b.get_coordinate(1,0).add_constraint(cons4)
#b.get_coordinate(1,1).add_constraint(cons2)
#b.get_coordinate(1,2).add_constraint(cons2)
#b.get_coordinate(2,0).add_constraint(cons4)
#b.get_coordinate(2,1).add_constraint(cons3)
#b.get_coordinate(2,2).add_constraint(cons3)
#
#
#b.add_constraint(cons1)
#b.add_constraint(cons2)
#b.add_constraint(cons3)
#b.add_constraint(cons4)
#    
#bt=Back_Track(b)
#bt.solve()


"""TEST 2"""
#b=board(3)
#
#cons1 = Arithmetic_Constraint([b.get_coordinate(0,0),b.get_coordinate(0,1)],4)
#cons2 = Arithmetic_Constraint([b.get_coordinate(0,2),b.get_coordinate(1,1),b.get_coordinate(1,2)],7)
#cons3 = Arithmetic_Constraint([b.get_coordinate(2,1),b.get_coordinate(2,2)],4)
#cons4 = Arithmetic_Constraint([b.get_coordinate(1,0),b.get_coordinate(2,0)],3)
#
#b.get_coordinate(0,0).add_constraint(cons1)
#b.get_coordinate(0,1).add_constraint(cons1)
#b.get_coordinate(0,2).add_constraint(cons2)
#b.get_coordinate(1,0).add_constraint(cons4)
#b.get_coordinate(1,1).add_constraint(cons2)
#b.get_coordinate(1,2).add_constraint(cons2)
#b.get_coordinate(2,0).add_constraint(cons4)
#b.get_coordinate(2,1).add_constraint(cons3)
#b.get_coordinate(2,2).add_constraint(cons3)
#
#
#b.add_constraint(cons1)
#b.add_constraint(cons2)
#b.add_constraint(cons3)
#b.add_constraint(cons4)
#   
#bt=Back_Track(b)
#bt.solve()

"""TEST 3"""

#b=board(4)
#
#cons1 = Arithmetic_Constraint([b.get_coordinate(0,0),b.get_coordinate(1,0)],4)
#cons2 = Arithmetic_Constraint([b.get_coordinate(0,1),b.get_coordinate(0,2),b.get_coordinate(1,1)],8)
#cons3 = Arithmetic_Constraint([b.get_coordinate(0,3),b.get_coordinate(1,3)],5)
#cons4 = Arithmetic_Constraint([b.get_coordinate(2,0),b.get_coordinate(2,1)],7)
#cons5 = Arithmetic_Constraint([b.get_coordinate(1,2),b.get_coordinate(2,2),b.get_coordinate(2,3)],6)
#cons6 = Arithmetic_Constraint([b.get_coordinate(3,0),b.get_coordinate(3,1),b.get_coordinate(3,2)],7)
#cons7 = Arithmetic_Constraint([b.get_coordinate(3,3)],3)
#
#
#b.get_coordinate(0,0).add_constraint(cons1)
#b.get_coordinate(0,1).add_constraint(cons2)
#b.get_coordinate(0,2).add_constraint(cons2)
#b.get_coordinate(0,3).add_constraint(cons3)
#b.get_coordinate(1,0).add_constraint(cons1)
#b.get_coordinate(1,1).add_constraint(cons2)
#b.get_coordinate(1,2).add_constraint(cons5)
#b.get_coordinate(1,3).add_constraint(cons3)
#b.get_coordinate(2,0).add_constraint(cons4)
#b.get_coordinate(2,1).add_constraint(cons4)
#b.get_coordinate(2,2).add_constraint(cons5)
#b.get_coordinate(2,3).add_constraint(cons5)
#b.get_coordinate(3,0).add_constraint(cons6)
#b.get_coordinate(3,1).add_constraint(cons6)
#b.get_coordinate(3,2).add_constraint(cons6)
#b.get_coordinate(3,3).add_constraint(cons3)
#
#b.add_constraint(cons1)
#b.add_constraint(cons2)
#b.add_constraint(cons3)
#b.add_constraint(cons4)
#b.add_constraint(cons5)
#b.add_constraint(cons6)
#b.add_constraint(cons7)
#    
#bt=Back_Track(b)
#bt.solve()
#