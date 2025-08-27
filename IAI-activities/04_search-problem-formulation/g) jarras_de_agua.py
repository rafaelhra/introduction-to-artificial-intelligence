class JarsState:
    def __init__(self, jar12, jar8, jar3):
        self.jar12 = jar12
        self.jar8 = jar8
        self.jar3 = jar3
    
    def is_goal(self):
        return self.jar12 == 1 or self.jar8 == 1 or self.jar3 == 1
    
    def __eq__(self, other):
        return self.jar12 == other.jar12 and \
               self.jar8 == other.jar8 and \
               self.jar3 == other.jar3
    
    def __hash__(self):
        return hash((self.jar12, self.jar8, self.jar3))