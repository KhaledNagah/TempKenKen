from board import board
from coordinate import Coordinate
from constraint import Arithmetic_Constraint
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
        
        for coord in self.board.get_coordinates():
            print(coord.get_domain())
        print("################")
        if self.is_solved():
            return True

        else:
            current_coordinate = self.coordiantes[index]
            current_coordinate=self.board.get_coordinate(int(index/self.board.get_size()),index%self.board.get_size())
            #print("^^^",current_coordinate is self.board.get_coordinate(int(index/self.board.get_size()),index%self.board.get_size()) )
            for value in self.board.get_domain():
                
                #All Values of coordinates after me must be zero
                for i in range (index+1,self.board.get_size()*self.board.get_size()):
                    self.board.set_coordinate_value(int(i/self.board.get_size()),i%self.board.get_size(),0)


                current_coordinate.set_value(value)
                #print("iteration:",value," for coordinate: ",index+1)
                #If assignment is valid
                #1 R Constraint
                invalid_R=0
                for neighbour_coordinate in self.board.get_row(current_coordinate.get_x()):
                    

                    if ((current_coordinate.get_x()!=neighbour_coordinate.get_x()) or (current_coordinate.get_y()!=neighbour_coordinate.get_y())):
                        if current_coordinate.get_value()==neighbour_coordinate.get_value():
                            invalid_R=1
                            break
                if invalid_R==1:
                    continue

                #1 C Constraint
                invalid_C=0
                for neighbour_coordinate in self.board.get_colomn(current_coordinate.get_y()):
                    if ((current_coordinate.get_x()!=neighbour_coordinate.get_x()) or (current_coordinate.get_y()!=neighbour_coordinate.get_y())):
                        if current_coordinate.get_value()==neighbour_coordinate.get_value():
                            invalid_C=1
                            break
                if invalid_C==1:
                    continue
                #3 Arithmetic Constraint
                current_coordinate_constraint=current_coordinate.get_constraint()

                #sum=current_coordinate.get_value()
                #print("sum::::::::::::::::::",current_coordinate_constraint.get_sum())
                sum=0
                for neighbour_coordinate in current_coordinate_constraint.get_coordinates():
                    real_neighbour_coordinate=self.board.get_coordinate(neighbour_coordinate.get_x(),neighbour_coordinate.get_y())
                    sum+=real_neighbour_coordinate.get_value()

                if(sum<=current_coordinate_constraint.get_sum()):
                    result=self.inner_solve(index+1)
                    if result != 0:
                        return 1
                        
                        
                    

            return 0
                            

##testing
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


b=board(4)

cons1 = Arithmetic_Constraint([b.get_coordinate(0,0),b.get_coordinate(1,0)],4)
cons2 = Arithmetic_Constraint([b.get_coordinate(0,1),b.get_coordinate(0,2),b.get_coordinate(1,1)],8)
cons3 = Arithmetic_Constraint([b.get_coordinate(0,3),b.get_coordinate(1,3)],5)
cons4 = Arithmetic_Constraint([b.get_coordinate(2,0),b.get_coordinate(2,1)],7)
cons5 = Arithmetic_Constraint([b.get_coordinate(1,2),b.get_coordinate(2,2),b.get_coordinate(2,3)],6)
cons6 = Arithmetic_Constraint([b.get_coordinate(3,0),b.get_coordinate(3,1),b.get_coordinate(3,2)],7)
cons7 = Arithmetic_Constraint([b.get_coordinate(3,3)],3)


b.get_coordinate(0,0).add_constraint(cons1)
b.get_coordinate(0,1).add_constraint(cons2)
b.get_coordinate(0,2).add_constraint(cons2)
b.get_coordinate(0,3).add_constraint(cons3)
b.get_coordinate(1,0).add_constraint(cons1)
b.get_coordinate(1,1).add_constraint(cons2)
b.get_coordinate(1,2).add_constraint(cons5)
b.get_coordinate(1,3).add_constraint(cons3)
b.get_coordinate(2,0).add_constraint(cons4)
b.get_coordinate(2,1).add_constraint(cons4)
b.get_coordinate(2,2).add_constraint(cons5)
b.get_coordinate(2,3).add_constraint(cons5)
b.get_coordinate(3,0).add_constraint(cons6)
b.get_coordinate(3,1).add_constraint(cons6)
b.get_coordinate(3,2).add_constraint(cons6)
b.get_coordinate(3,3).add_constraint(cons3)

b.add_constraint(cons1)
b.add_constraint(cons2)
b.add_constraint(cons3)
b.add_constraint(cons4)
b.add_constraint(cons5)
b.add_constraint(cons6)
b.add_constraint(cons7)
    
bt=Back_Track(b)
bt.solve()
