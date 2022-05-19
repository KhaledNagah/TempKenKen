class Coordinate:
    def __init__(self, x, y, domain):
        self.x = x
        self.y = y
        self.domain = domain
        self.domainSize = len(domain)
        self.constraints = []
        self.value = 0

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y
    
    def domain_size(self):
        return self.domainSize   

    
    def get_domain(self):
        return self.domain

    
    def set_domain(self,values):
        self.domain=values

        
    def remove_from_domain(self,value):
        self.domain.remove(value)
    
        
    def is_in_domain(self,value):
        for i in self.domain:
            if self.domain[i] == value:
                return True 
        return False

    def add_constraint(self,constraint):
        self.constraints.append(constraint)

    def get_constraint(self):
        return self.constraints    

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value    


