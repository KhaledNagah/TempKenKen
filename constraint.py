from coordinate import Coordinate



class Arithmetic_Constraint:
    def __init__(self, coordinates, sum):
        self.coordinates=coordinates
        self.sum=sum

    def get_coordinates (self):
        return self.coordinates

    def includes_coordinate(self, coordinate):
        for currentCoordinate in self.coordinates:
            if currentCoordinate==coordinate:
                return True 
        return False   

    def is_constraint_satisfied(self,values):
        if len(values)!=len(self.coordinates):
            return False

        currentSum=0
        for value in values:
            currentSum+=value

        if currentSum==self.sum:   
            return True
        else:
            return False
    def get_sum(self):
        return self.sum

#class RC_Constraint:
#    def __init__(self, coordinates):
#        self.coordinates=coordinates
#        
#    def get_coordinates (self):
#        return self.coordinates
#
#    def includes_coordinate(self, coordinate):
#        for currentCoordinate in self.coordinates:
#            if currentCoordinate==coordinate:
#                return True 
#        return False   
#
#    def is_constraint_satisfied(self,values):
#        if len(values)!=len(self.coordinates):
#            return False
#
#        if len(values) == len(set(values)):
#            return True
#        else:
#            return False


"""
Testing RC_Constraint Class
"""         

#c1 = Coordinate(0,0,[1,2,3,4])
#c2 = Coordinate(0,1,[2,3,4])
#c3 = Coordinate(0,2,[3,4])
#c4 = Coordinate(0,3,[4])
#
#c1.set_value(1)
#c2.set_value(2)
#c3.set_value(3)
#c4.set_value(4)
#
#coordinates = [c1,c2,c3,c4]
#
#cons1 = RC_Constraint(coordinates)
#
#arr = cons1.get_coordinates()
#
#print(arr[1].get_x(),arr[1].get_y())
#
#values = [1,2,2,4]
#
#print(cons1.is_constraint_satisfied(values))
#
#
#c5 = Coordinate(1,1,[1,2,3])
#print(cons1.includes_coordinate(c4))

"""
Testing Arithmetic_Constraint Class
"""  
#c1 = Coordinate(0,0,[1,2,3,4])
#c2 = Coordinate(0,1,[2,3,4])
#c3 = Coordinate(0,2,[3,4])
#c4 = Coordinate(0,3,[4])
#
#c1.set_value(1)
#c2.set_value(2)
#c3.set_value(3)
#c4.set_value(4)
#
#coordinates = [c1,c2,c3,c4]
#
#cons1 = Arithmetic_Constraint(coordinates,8)
#
#arr = cons1.get_coordinates()
#
#print(arr[1].get_x(),arr[1].get_y())
#
#values = [1,1,2,4]
#
#print(cons1.is_constraint_satisfied(values))
#
#
#c5 = Coordinate(1,1,[1,2,3])
#print(cons1.includes_coordinate(c5))