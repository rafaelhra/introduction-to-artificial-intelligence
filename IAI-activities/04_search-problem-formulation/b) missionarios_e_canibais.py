class MissionariesState:
    def __init__(self, left_m, left_c, boat_left):
        self.left_m = left_m
        self.left_c = left_c
        self.boat_left = boat_left
    
    def is_valid(self):
        right_m = 3 - self.left_m
        right_c = 3 - self.left_c
        return (self.left_m >= self.left_c or self.left_m == 0) and \
               (right_m >= right_c or right_m == 0)
    
    def __eq__(self, other):
        return self.left_m == other.left_m and \
               self.left_c == other.left_c and \
               self.boat_left == other.boat_left
    
    def __hash__(self):
        return hash((self.left_m, self.left_c, self.boat_left))