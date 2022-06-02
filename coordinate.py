class Coordinate:
    def __init__(self, x, y, domain):
        self.x = x
        self.y = y
        self.domain = domain
        self.domainSize = len(domain)
        self.value = 0
        #self.constraint = 0

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
        self.domainSize =self.domainSize -1
    
        
    def is_in_domain(self,value):
        for i in self.domain:
            if i == value:
                return True 
        return False

    def add_constraint(self,constraint):
       self.constraint=constraint

    def get_constraint(self):
        return self.constraint   

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value    

