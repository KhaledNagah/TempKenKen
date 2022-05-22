from board import board
from coordinate import Coordinate
from constraint import Arithmetic_Constraint
import copy
class Back_Track:
    def __init__(self,board):
        self.board=board
        self.coordiantes=board.get_coordinates()

    def is_solved(self):
        #Arithmetic Constraint
        for constraint in self.board.get_constraints():
                    values = []
                    for coord in constraint.get_coordinates():
                        if (coord.get_value() == 0):  
                            return False
                        values.append(coord.get_value())
                    if (not constraint.is_constraint_satisfied(values)):
                        return False
        
        #Row Constraint
        for x in range(self.board.get_size()):
            row_coords=self.board.get_row(x)
            values = []
            for y in range(len(row_coords)):
                values.append(row_coords[y].get_value())
            
            if len(values) != len(set(values)):
                return False
        
        #Column Constraint
        for x in range(self.board.get_size()):
            col_coords=self.board.get_colomn(x)
            values = []
            for y in range(len(col_coords)):
                values.append(col_coords[y].get_value())
            
            if len(values) != len(set(values)):
                return False

        return True    
    
    def solve(self):
        return self.inner_solve (0)

    def inner_solve(self,index):
        
        if self.is_solved():
            return True

        else:
            current_coordinate = self.coordiantes[index]
            current_coordinate=self.board.get_coordinate(int(index/self.board.get_size()),index%self.board.get_size())
            #print("^^^",current_coordinate is self.board.get_coordinate(int(index/self.board.get_size()),index%self.board.get_size()) )
            state_count=0
            counter=0
            while counter<len(current_coordinate.get_domain()):
                value= current_coordinate.get_domain()[counter]
                counter=counter+1
                goto_next_iteration=0
                
                #save board state in case first iteration
                if(state_count==0):
                    first_board_state=copy.deepcopy(self.board)
                else:
                    self.board=copy.deepcopy(first_board_state)
                
                state_count=1
                #All Values of coordinates after me must be zero
                for i in range (index+1,self.board.get_size()*self.board.get_size()):
                    self.board.set_coordinate_value(int(i/self.board.get_size()),i%self.board.get_size(),0)

                #print("index: ",index, "domains: ",current_coordinate.get_domain()," value: ",value)
                current_coordinate = self.coordiantes[index]
                current_coordinate=self.board.get_coordinate(int(index/self.board.get_size()),index%self.board.get_size())
                current_coordinate.set_value(value)
                print("index: ",index)
                for coord in self.board.get_coordinates():
                    print("domain ",coord.get_domain(),"value ",coord.get_value())
                print("################")
                #Forward Checking
                #For row neighbours
                for neighbour_coordinate in self.board.get_row(current_coordinate.get_x()):
                    real_neighbour_coordinate=self.board.get_coordinate(neighbour_coordinate.get_x(),neighbour_coordinate.get_y())
                    if ((current_coordinate.get_x()!=real_neighbour_coordinate.get_x()) or (current_coordinate.get_y()!=real_neighbour_coordinate.get_y())):
                        #remove the assigned value from all row neighbours if it exist
                        if(real_neighbour_coordinate.is_in_domain(current_coordinate.get_value())):                            
                            real_neighbour_coordinate.remove_from_domain(current_coordinate.get_value())
                           # print(real_neighbour_coordinate.get_x()," ",real_neighbour_coordinate.get_y()," :",real_neighbour_coordinate.get_domain())
                            if  len(real_neighbour_coordinate.get_domain())==0:
                                goto_next_iteration=1

               # print(" ")
 
                if goto_next_iteration==1:
                    continue
                #For column neighbours
                for neighbour_coordinate in self.board.get_colomn(current_coordinate.get_y()):
                    real_neighbour_coordinate=self.board.get_coordinate(neighbour_coordinate.get_x(),neighbour_coordinate.get_y())
                    if ((current_coordinate.get_x()!=real_neighbour_coordinate.get_x()) or (current_coordinate.get_y()!=real_neighbour_coordinate.get_y())):
                        #remove the assigned value from all row neighbours if it exist                           
                        if(real_neighbour_coordinate.is_in_domain(current_coordinate.get_value())):
                            real_neighbour_coordinate.remove_from_domain(current_coordinate.get_value())
                           # print(real_neighbour_coordinate.get_x()," ",real_neighbour_coordinate.get_y()," :",real_neighbour_coordinate.get_domain())
                            if  len(real_neighbour_coordinate.get_domain())==0:
                                goto_next_iteration=1
               # print("#####################################################3")
                if goto_next_iteration==1:
                    continue

                #For arithmetic neighbours
                sum=0
                current_coordinate_constraint=current_coordinate.get_constraint()
                for neighbour_coordinate in current_coordinate_constraint.get_coordinates():
                    real_neighbour_coordinate=self.board.get_coordinate(neighbour_coordinate.get_x(),neighbour_coordinate.get_y())
                    sum+=real_neighbour_coordinate.get_value()
                
                for neighbour_coordinate in current_coordinate_constraint.get_coordinates():
                    real_neighbour_coordinate=self.board.get_coordinate(neighbour_coordinate.get_x(),neighbour_coordinate.get_y())
                    #Do this if the neighbour is not assigned a value
                    if(real_neighbour_coordinate.get_value()==0):
                        for neighbour_domain_value in real_neighbour_coordinate.get_domain():
                            if neighbour_domain_value+sum > current_coordinate_constraint.get_sum():
                                real_neighbour_coordinate.remove_from_domain(neighbour_domain_value)
                            if  len(real_neighbour_coordinate.get_domain())==0:
                                 goto_next_iteration=1
                if  goto_next_iteration==1:
                    continue
                #Check that if all coordinates in a constraint are given a value, their sum must be 
                #equal to the constraint sum 
                flag=0
                for neighbour_coordinate in current_coordinate_constraint.get_coordinates():
                    real_neighbour_coordinate=self.board.get_coordinate(neighbour_coordinate.get_x(),neighbour_coordinate.get_y())
                    if(real_neighbour_coordinate.get_value()==0):
                       flag=1  
                
                if flag==1:
                    result=self.inner_solve(index+1)
                    if result != 0:
                        return 1
                    self.board=copy.deepcopy(first_board_state)
                    current_coordinate=self.board.get_coordinate(int(index/self.board.get_size()),index%self.board.get_size())
                    current_coordinate.remove_from_domain(value)
                    first_board_state=self.board
                    counter=0

                    print("result: ",result, " index ", index)
                    print("domains: ",current_coordinate.get_domain())

                else:
                    
                    sum=0
                    for neighbour_coordinate in current_coordinate_constraint.get_coordinates():
                        real_neighbour_coordinate=self.board.get_coordinate(neighbour_coordinate.get_x(),neighbour_coordinate.get_y())
                        sum+=real_neighbour_coordinate.get_value()

                    if(sum!=current_coordinate_constraint.get_sum()):
                       continue
                    else:
                        result=self.inner_solve(index+1)
                        if result != 0:
                            return 1
                        self.board=copy.deepcopy(first_board_state)
                        current_coordinate=self.board.get_coordinate(int(index/self.board.get_size()),index%self.board.get_size())
                        current_coordinate.remove_from_domain(value)
                        first_board_state=self.board
                        counter=0
                        print("domains: ",current_coordinate.get_domain())

                        print("result: ",result, " index ", index)
    
            return 0
                            

##testing
#test1
b=board(3)

cons1 = Arithmetic_Constraint([b.get_coordinate(0,0),b.get_coordinate(0,1)],3)
cons2 = Arithmetic_Constraint([b.get_coordinate(0,2),b.get_coordinate(1,1),b.get_coordinate(1,2)],7)
cons3 = Arithmetic_Constraint([b.get_coordinate(2,1),b.get_coordinate(2,2)],3)
cons4 = Arithmetic_Constraint([b.get_coordinate(1,0),b.get_coordinate(2,0)],5)

b.get_coordinate(0,0).add_constraint(cons1)
b.get_coordinate(0,1).add_constraint(cons1)
b.get_coordinate(0,2).add_constraint(cons2)
b.get_coordinate(1,0).add_constraint(cons4)
b.get_coordinate(1,1).add_constraint(cons2)
b.get_coordinate(1,2).add_constraint(cons2)
b.get_coordinate(2,0).add_constraint(cons4)
b.get_coordinate(2,1).add_constraint(cons3)
b.get_coordinate(2,2).add_constraint(cons3)


b.add_constraint(cons1)
b.add_constraint(cons2)
b.add_constraint(cons3)
b.add_constraint(cons4)
    
bt=Back_Track(b)
bt.solve()


#test2
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
#
#test3


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
    
#bt=Back_Track(b)
#bt.solve()