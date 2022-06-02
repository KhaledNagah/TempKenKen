from coordinate import Coordinate
#from constraint import RC_Constraint
from constraint import Arithmetic_Constraint


class board:
    def __init__(self, size):
        self.size = size
        self.domain = []
        self.coordinates = []
        self.constraints = []

        ### initialize coordinates ###
        for i in range(size):
            self.domain.append(i+1)

        for z in range(size):
            for j in range(size):
                coord_domain=list(range(1,self.size+1))
                p = Coordinate(z , j,coord_domain )
                p.set_value(0)
                self.coordinates.append(p) 


    def get_colomn(self, col):
        list_coordinates = []
        for i in self.coordinates:
            if(i.get_y() == col):
                list_coordinates.append(i)

        return list_coordinates

    
    def get_row(self, row):
        list_coordinates = []
        for i in self.coordinates:
            if(i.get_x() == row):
                list_coordinates.append(i)

        return list_coordinates 


    def get_coordinates(self):
        return self.coordinates    

    def get_coordinate(self, x, y):
        for i in self.coordinates:
            if((i.get_x() == x) and (i.get_y() == y)):
                return i

    def get_size(self):
        return self.size    

    def add_constraint(self, constraint):
        self.constraints.append(constraint)

    def get_constraints(self):
        return self.constraints

    def get_domain(self):
        return self.domain
    ### initialize row and colomns constraints ###
    #def initialize_RCconstraint(self):
    #    for i in range(self.size):
    #        self.constraints.append(RC_Constraint(self.get_row(i)))        
    #        self.constraints.append(RC_Constraint(self.get_colomn(i)))        
    
    def set_coordinate_value(self,x,y,value):
        self.coordinates[(self.size)*x+y].set_value(value)

