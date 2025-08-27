class SudokuState:
    def __init__(self, grid):
        self.grid = grid
    
    def is_valid(self, row, col, num):
        if num in self.grid[row]:
            return False
        if num in [self.grid[i][col] for i in range(9)]:
            return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if self.grid[start_row + i][start_col + j] == num:
                    return False
        return True
    
    def is_goal(self):
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    return False
                num = self.grid[i][j]
                self.grid[i][j] = 0
                valid = self.is_valid(i, j, num)
                self.grid[i][j] = num
                if not valid:
                    return False
        return True