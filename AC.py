from board import board
from coordinate import Coordinate
from constraint import Arithmetic_Constraint
import copy
import pygame
from gui import draw_board, instruction

#global variable
final_coordinates = []

class AC:
    def __init__(self,board):
        self.board=board
        self.coordiantes=self.board.get_coordinates()
        self.coordinate_domain = list(range(1,self.board.size+1))
        #self.AC_queue = []
    
    #Function to generate a queue of constraints 
    def queue_of_constraints(self,coordinate,coordinates):
        x = coordinate.get_x()
        y = coordinate.get_y()
        AC_queue = []
        constraint = coordinate.get_constraint()
        for neighbour_coordinate in coordinates:
            if (neighbour_coordinate.get_x() == x) or (neighbour_coordinate.get_y() == y) or (neighbour_coordinate.get_constraint() == constraint):
                (AC_queue).append(neighbour_coordinate)
        return AC_queue       
    #function to check the 
    def check_Arithmetic_constraint(self,coordinate):
        constraint = coordinate.get_constraint()
        coordinates = constraint.get_coordinates()
        sum = 0
        for i in coordinates:
            sum += i.get_value()
        for i in coordinates:
            if(i.get_value() == 0):
                return 1
        if((sum == constraint.get_sum()) and (constraint.cells_filled() == len(coordinates))):
            return 1
        return 0            

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
        result = self.inner_solve(0)
        self.board.coordinates = final_coordinates
        draw_board(self.board)
        instruction()
        pygame.display.update()
        pygame.event.pump()
        pygame.time.delay(3000)
        return result

    def inner_solve(self,index): #index is the index of the current coordinate        
        #Always check at the beggining of this recursive function if the board is solved, hence return true
        
        # Draw generated board
        draw_board(self.board)
        instruction()
        pygame.display.update()
        pygame.event.pump()
        #pygame.time.delay(300)
    
        if self.is_solved():
            return True

        #If the board is not solved
        else:
            #Get the coordinate with the given index
            current_coordinate=self.board.get_coordinate(int(index/self.board.get_size()),index%self.board.get_size())
            #print("Coordinate : (",current_coordinate.get_x(),",",current_coordinate.get_y())
            #is_first_iteration_for_a_variable:
            #If it is 0, Save board state in case first iteration for a variable to use it in case of a backtrack
            #If it is 1, Assign the board to its first state when working with this coordinate because we backtracked
            is_first_iteration_for_a_variable=0 
            counter=0 #iterator on the domains of a variable
            temp_domain = []
            temp_domain.extend(range(1,self.board.size+1))

            #if(len(current_coordinate.get_domain())== 0):
            #    current_coordinate.set_domain(temp_domain)

            while counter<len(current_coordinate.get_domain()):
                #Get a value from the domain of the variable
                #Note that the domain can change 
                value= current_coordinate.get_domain()[counter]
                counter=counter+1
                goto_next_iteration=0 #If it is set to 1, then a constraint is not satisfied, so try another value from the domain if the variable 
                
                #Save board state in case first iteration for a variable to use it in case of a backtrack
                if(is_first_iteration_for_a_variable==0):
                    first_board_state=copy.deepcopy(self.board)
                ##Assign the board to its first state when working with this  coordinate because we backtracked
                else:
                    self.board=copy.deepcopy(first_board_state)
                
                is_first_iteration_for_a_variable=1
                #All Values of coordinates after me must be zero, this must be done because in case of backtraking
                for i in range (index+1,self.board.get_size()*self.board.get_size()):
                    self.board.set_coordinate_value(int(i/self.board.get_size()),i%self.board.get_size(),0)
                    #if Index == 1 then reset the domain     

                current_coordinate=self.board.get_coordinate(int(index/self.board.get_size()),index%self.board.get_size())
                #Assign a value to the coordinate
                current_coordinate.set_value(value)
                #print(index)

                #ARC Consistency
                #Getting Constraints
                all_coordinates = self.board.coordinates
                sum=0 
                #for i in all_coordinates:
                #    if((len(i.get_domain())== 0 )and (index == 1) or ((len(i.get_domain())== 0 )and counter > 1)):
                #        i.set_domain(temp_domain)

                if(not self.check_Arithmetic_constraint(current_coordinate)):
                    goto_next_iteration = 1

                if  goto_next_iteration==1:
                    #print("Index : ", index)
                    continue

                #Getting constraints for updating domain
                Constraint = current_coordinate.get_constraint()
                #first update queue of constraints that are related to the updates cell 
                current_queue = self.queue_of_constraints(current_coordinate,all_coordinates)

                for coordinate in current_queue:
                    sum = 0
                    if (coordinate.get_constraint() == current_coordinate.get_constraint()) and (coordinate != current_coordinate):
                        for neighbour_coordinate in Constraint.get_coordinates():
                            real_neighbour_coordinate=self.board.get_coordinate(neighbour_coordinate.get_x(),neighbour_coordinate.get_y())
                            sum+=real_neighbour_coordinate.get_value()    

                        for neighbour_coordinate in Constraint.get_coordinates():
                            if(neighbour_coordinate.get_value()==0):
                                for neighbour_domain_value in neighbour_coordinate.get_domain():
                                    if neighbour_domain_value+sum > Constraint.get_sum():
                                        if(neighbour_coordinate.is_in_domain(neighbour_domain_value)):
                                            neighbour_coordinate.remove_from_domain(neighbour_domain_value)
                            elif(neighbour_coordinate.get_value()!=0):

                                #If a neighbour has an empty domain, try another value for the current coordinate
                                if  len(neighbour_coordinate.get_domain())==0:
                                    goto_next_iteration=1

                        if  goto_next_iteration==1:
                            break                                   
                    x_coordinate = coordinate.get_x()
                    y_coordinate = coordinate.get_y()
                    row = self.board.get_row(x_coordinate)
                    col = self.board.get_colomn(y_coordinate)
                    coordinate_domain = coordinate.get_domain()
                    #Update domain of coordinates after filling the value of the current cell
                    #For Testing and debuging
                    #if(coordinate.get_value() != 0):
                        #print("Value :",coordinate.get_value(), "Coordinates : (",x_coordinate, ",",y_coordinate,")")
                        #continue
                    for i in row:
                        if(i.get_x() == x_coordinate and i.get_y() == y_coordinate) or (i.get_value() != 0):
                            continue
                        elif(i.get_x() == x_coordinate or i.get_y() == y_coordinate):
                            i_domain = i.get_domain()
                            if(coordinate.get_value() != 0):
                                if(i.is_in_domain(coordinate.get_value())):
                                    i.remove_from_domain(coordinate.get_value())
                            else:
                                for value in coordinate_domain:
                                    #variable determine if we found a value that is suitable with value
                                    Is_Found = 0
                                    for j in i_domain:
                                        if(value != j):
                                            Is_Found = 1
                                    if(Is_Found == 0):
                                        coordinate.remove_from_domain(value)
                                #If a neighbour has an empty domain, try another value for the current coordinate
                                if  len(coordinate.get_domain())==0:
                                    goto_next_iteration=1

                        if  goto_next_iteration==1:
                            break        
                    for i in col:
                        if(i.get_x() == x_coordinate and i.get_y() == y_coordinate) or (i.get_value() != 0):
                            continue
                        elif(i.get_x() == x_coordinate or i.get_y() == y_coordinate):
                            i_domain = i.get_domain()
                            if(coordinate.get_value() != 0):
                                if(i.is_in_domain(coordinate.get_value())):
                                    i.remove_from_domain(coordinate.get_value())
                            else:
                                for value in coordinate_domain:
                                    #variable determine if we found a value that is suitable with value
                                    Is_Found = 0
                                    for j in i_domain:
                                        if(value != j):
                                            Is_Found = 1
                                    if(Is_Found == 0):
                                        coordinate.remove_from_domain(value)
                                #If a neighbour has an empty domain, try another value for the current coordinate
                                if  len(coordinate.get_domain())==0:
                                    goto_next_iteration=1

                        if  goto_next_iteration==1:
                            break                        
                #next coordinate by calling the recusrive function inner_solve
                if(sum<=Constraint.get_sum()):
                    result=self.inner_solve(index+1)
                    #If result is 0, so try another value from the domain of the variable, if all domains are tried, return 0
                    if result != 0:
                        global final_coordinates
                        if(len(final_coordinates) == 0):
                            final_coordinates = all_coordinates

                        self.board.coordinates  = final_coordinates
                        return 1      
            return 0
#
#"""TESTING"""
#"""TEST 1"""
#print("HElLO")
#
#print("First test:")
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
#bt=AC(b)
#bt.solve()
#
#for i in final_coordinates:
#    print("(",i.get_x(),",",i.get_y(),")",i.get_value())
#
#del final_coordinates[:]    
#
#print("Second test:")
#"""TEST 2"""
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
#bt=AC(b)
#bt.solve()
#
#for i in final_coordinates:
#    print("(",i.get_x(),",",i.get_y(),")",i.get_value())
#
#del final_coordinates[:]    
#
#print("Third test:")
#"""TEST 3"""
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
#bt=AC(b)
#bt.solve()
#
#for i in final_coordinates:
#    print("(",i.get_x(),",",i.get_y(),")",i.get_value())
