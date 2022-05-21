####IMPORT CONSTRAINT AND COORDINATE CLASSES##################

class board:
    def __init__(self, size):
        self.size = size
        self.domain = []
        self.coordinates = []
        self.constraints = []

        ### initialize coordinates ###
        for i in range(1,size+1):
            self.domain.append(i)

        for i in range(size):
            for j in range(size):
                p = Coordinate(i , j,self.domain )
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

    ### initialize row and colomns constraints ###
    def initialize_RCconstraint(self):
        for i in range(self.size):
            self.constraints.append(RC_Constraint(self.get_row(i)))        
            self.constraints.append(RC_Constraint(self.get_colomn(i)))        
  
