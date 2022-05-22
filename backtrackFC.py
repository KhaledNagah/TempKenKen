from board import board
from coordinate import Coordinate
from constraint import Arithmetic_Constraint
import copy
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
        
        #For debugging to show the values of the coordinates at each step
        for coord in self.board.get_coordinates():
            print(coord.get_value())
        print("################")

        #Always check at the beggining of this recursive function if the board is solved, hence return true
        if self.is_solved():
            return True

        #If the board is not solved
        else:
            #Get the coordinate with the given index
            current_coordinate=self.board.get_coordinate(int(index/self.board.get_size()),index%self.board.get_size())

            #is_first_iteration_for_a_variable:
            #If it is 0, Save board state in case first iteration for a variable to use it in case of a backtrack
            #If it is 1, Assign the board to its first state when working with this coordinate because we backtracked
            is_first_iteration_for_a_variable=0 
            counter=0 #iterator on the domains of a variable

            while counter<len(current_coordinate.get_domain()):
                #Get a value from the domain of the variable
                #Note that the domain can change 
                value= current_coordinate.get_domain()[counter]
                counter=counter+1
                goto_next_iteration=0 #If it is set to 1, then a constraint is not satisfied, so try another value from the domain if the variable 
                
                #Save board state in case first iteration for a variable to use it in case of a backtrack
                if(is_first_iteration_for_a_variable==0):
                    first_board_state=copy.deepcopy(self.board)
                #Assign the board to its first state when working with this  coordinate because we backtracked
                else:
                    self.board=copy.deepcopy(first_board_state)
                
                is_first_iteration_for_a_variable=1
                
                #All Values of coordinates after me must be zero, this must be done because in case of backtraking
                for i in range (index+1,self.board.get_size()*self.board.get_size()):
                    self.board.set_coordinate_value(int(i/self.board.get_size()),i%self.board.get_size(),0)

                current_coordinate=self.board.get_coordinate(int(index/self.board.get_size()),index%self.board.get_size())
                
                #Assign a value to the coordinate
                current_coordinate.set_value(value)
                
                #Forward Checking
                #1 Forward Checking for row neighbours
                for neighbour_coordinate in self.board.get_row(current_coordinate.get_x()):
                    real_neighbour_coordinate=self.board.get_coordinate(neighbour_coordinate.get_x(),neighbour_coordinate.get_y())
                    if ((current_coordinate.get_x()!=real_neighbour_coordinate.get_x()) or (current_coordinate.get_y()!=real_neighbour_coordinate.get_y())):
                        #remove the assigned value from all row neighbours if it exist
                        if(real_neighbour_coordinate.is_in_domain(current_coordinate.get_value())):                            
                            real_neighbour_coordinate.remove_from_domain(current_coordinate.get_value())
                            #If a neighbour has an empty domain, try another value for the current coordinate
                            if  len(real_neighbour_coordinate.get_domain())==0:
                                goto_next_iteration=1

                if goto_next_iteration==1:
                    continue
                
                #2 Forward Checking for colomn neighbours
                for neighbour_coordinate in self.board.get_colomn(current_coordinate.get_y()):
                    real_neighbour_coordinate=self.board.get_coordinate(neighbour_coordinate.get_x(),neighbour_coordinate.get_y())
                    if ((current_coordinate.get_x()!=real_neighbour_coordinate.get_x()) or (current_coordinate.get_y()!=real_neighbour_coordinate.get_y())):
                        #remove the assigned value from all row neighbours if it exist                           
                        if(real_neighbour_coordinate.is_in_domain(current_coordinate.get_value())):
                            real_neighbour_coordinate.remove_from_domain(current_coordinate.get_value())
                            #If a neighbour has an empty domain, try another value for the current coordinate
                            if  len(real_neighbour_coordinate.get_domain())==0:
                                goto_next_iteration=1
                if goto_next_iteration==1:
                    continue

                #3 Forward Checking for arithmetic neighbours
                
                #Get the arithmetic constraint object of the coordinate
                current_coordinate_constraint=current_coordinate.get_constraint()
                #Calculate the sum of values of the coordinates in this constraint
                sum=0
                for neighbour_coordinate in current_coordinate_constraint.get_coordinates():
                    real_neighbour_coordinate=self.board.get_coordinate(neighbour_coordinate.get_x(),neighbour_coordinate.get_y())
                    sum+=real_neighbour_coordinate.get_value()
                
                for neighbour_coordinate in current_coordinate_constraint.get_coordinates():
                    real_neighbour_coordinate=self.board.get_coordinate(neighbour_coordinate.get_x(),neighbour_coordinate.get_y())
                    #If the neighbour is not assigned a value, remove values from its domain that makes the sum greater than the required sum
                    if(real_neighbour_coordinate.get_value()==0):
                        for neighbour_domain_value in real_neighbour_coordinate.get_domain():
                            if neighbour_domain_value+sum > current_coordinate_constraint.get_sum():
                                real_neighbour_coordinate.remove_from_domain(neighbour_domain_value)
                            
                            #If a neighbour has an empty domain, try another value for the current coordinate
                            if  len(real_neighbour_coordinate.get_domain())==0:
                                 goto_next_iteration=1
                if  goto_next_iteration==1:
                    continue
                
                #Check that if all coordinates in a constraint are given a value, their sum must be equal to the constraint sum 

                #Check that if all coordinates in a constraint are given a value 
                neighbour_not_given_a_value=0
                for neighbour_coordinate in current_coordinate_constraint.get_coordinates():
                    real_neighbour_coordinate=self.board.get_coordinate(neighbour_coordinate.get_x(),neighbour_coordinate.get_y())
                    if(real_neighbour_coordinate.get_value()==0):
                       neighbour_not_given_a_value=1  
                
                #If not given a value,
                if neighbour_not_given_a_value==1:
                    result=self.inner_solve(index+1)
                    #If result is not 0, return 1
                    if result != 0:
                        return 1
                     #If result is 0, so try another value from the domain of the variable, if all domains are tried, return 0
                    else:
                        #return first to the first board state when working on the coordinate
                        self.board=copy.deepcopy(first_board_state)
                        current_coordinate=self.board.get_coordinate(int(index/self.board.get_size()),index%self.board.get_size())
                        #remove thr tried value from the board state
                        current_coordinate.remove_from_domain(value)
                        first_board_state=self.board
                        #make the iterator on the domains begin with zero as the domains changed
                        counter=0

                #If given a value
                else:
                    #Get their sum
                    sum=0
                    for neighbour_coordinate in current_coordinate_constraint.get_coordinates():
                        real_neighbour_coordinate=self.board.get_coordinate(neighbour_coordinate.get_x(),neighbour_coordinate.get_y())
                        sum+=real_neighbour_coordinate.get_value()

                    #If the sum is not equal the required arithmetic constraint sum, try another value from the domain of the variable
                    if(sum!=current_coordinate_constraint.get_sum()):
                       continue
                    #If the sum is equal to the required arithmetic constraint sum, then this assignment is valid, so continue to the
                    #next coordinate by calling the recusrive function inner_solve
                    else:
                        result=self.inner_solve(index+1)
                         #If result is not 0, return 1
                        if result != 0:
                            return 1
                        #If result is 0, so try another value from the domain of the variable, if all domains are tried, return 0
                        else: 
                            #return first to the first board state when working on the coordinate
                            self.board=copy.deepcopy(first_board_state)
                            current_coordinate=self.board.get_coordinate(int(index/self.board.get_size()),index%self.board.get_size())
                            #remove thr tried value from the board state
                            current_coordinate.remove_from_domain(value)
                            #make the iterator on the domains begin with zero as the domains changed
                            first_board_state=self.board
                            counter=0
    
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