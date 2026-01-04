import copy

class Puzzle:
    def __init__(self, state):
        self.state = state
        self.cols = self.getCols()
        self.squares = self.getSquares()
        self.addPossibilities()
        
    
    def getCols(self): # Puzzle -> Grid
        lst = []

        for i in range(9):
            col = []
            for j in range(9):
                col.append(self.state[j][i])
            lst.append(col)
        
        return lst
    
    def getSquares(self): # Puzzle -> Grid
        lst = []

        for i in range(3):
            s1 = []
            s2 = []
            s3 = []
            for j in range(3): 
                s1 += self.state[(i * 3) + j][0:3]
                s2 += self.state[(i * 3) + j][3:6]
                s3 += self.state[(i * 3) + j][6:9]
            lst.append(s1)
            lst.append(s2)
            lst.append(s3)
        return lst
    
    def update(self):
        self.removeSingles()
        self.cols = self.getCols()
        self.squares = self.getSquares()

    
    def isSolved(self): # Puzzle -> Bool
        nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        def isFull():
            for r in self.state:
                for cell in r:
                    if isinstance(cell, list) or cell == "?":
                        return False
            return True

        def checkRows():
            for r in self.state:
                if not all(x in r for x in nums):
                    return False
            return True

        def checkCols():
            for c in self.cols:
                if not all(x in c for x in nums):
                    return False
            return True

        def checkSquares():
            for s in self.squares:
                if not all(x in s for x in nums):
                    return False
            return True
        return isFull() and checkRows() and checkCols() and checkSquares()
    
    def isFailed(self): # Puzzle -> Bool
        for i in range(9):
            for x in range(9):
                if (self.state[i].count(x + 1) > 1) or (self.cols[i].count(x + 1) > 1) or (self.squares[i].count(x + 1) > 1) or (self.state[i][x] == []):
                    return True
        return False

    

    def addPossibilities(self):
        for r in range(9):
            for c in range(9):
                if self.state[r][c] == "?":
                    self.state[r][c] = [1, 2, 3, 4, 5, 6, 7, 8, 9]

                    if r <= 2:
                        if c <= 2:
                            s = 0
                        elif c <= 5:
                            s = 1
                        else:
                            s = 2
                    elif r <= 5:
                        if c <= 2:
                            s = 3
                        elif c <= 5:
                            s = 4
                        else:
                            s = 5
                    else:
                        if c <= 2:
                            s = 6
                        elif c <= 5:
                            s = 7
                        else:
                            s = 8
                    cell = self.state[r][c][:]
                    for i in range(9):
                        if (self.state[r][c][i] in self.state[r]) or (self.state[r][c][i] in self.cols[c]) or (self.state[r][c][i] in self.squares[s]):
                            cell.remove(self.state[r][c][i])
                    self.state[r][c] = cell

    def removeSingles(self): 
        def filterIndex(n, lst): # Num List -> List
            return [x for x in lst if x != n]
        
        def containsSingle(self): # Puzzle -> Bool
            for r in range(9):
                for c in range(9):
                    if isinstance(self.state[r][c], list) and len(self.state[r][c]) == 1:
                        return True
            return False

        while containsSingle(self):
            for r in range(9):
                for c in range(9):
                    if isinstance(self.state[r][c], list) and len(self.state[r][c]) == 1:
                        self.state[r][c] = self.state[r][c][0]
                        val = self.state[r][c]
                        for x in range(9):
                            # remove from row
                            if isinstance(self.state[r][x], list):
                                self.state[r][x] = filterIndex(val, self.state[r][x])
                            # remove from column
                            if isinstance(self.state[x][c], list):
                                self.state[x][c] = filterIndex(val, self.state[x][c])
                            # remove from square
                            srow = (r // 3) * 3
                            scol = (c // 3) * 3
                            for i in range(srow, srow + 3):
                                for j in range(scol, scol + 3):
                                    if isinstance(self.state[i][j], list):
                                        self.state[i][j] = filterIndex(val, self.state[i][j])
            # keep cols/squares consistent for the next iteration
            self.cols = self.getCols()
            self.squares = self.getSquares()
                            
    
    def neighbors(self):
        minCandidates = []
        for r in range(9):
            lsts = [x for x in self.state[r] if isinstance(x, list)]
            if lsts != []:
                m = min(lsts, key=len)
                c = self.state[r].index(m)
                minCandidates.append([r, c, m])

        if minCandidates == []:
            return []
        else:
            totalMin = min(minCandidates, key=lambda x: len(x[2]))
            lst = self.state[totalMin[0]][totalMin[1]]
            nbrs = []

            for n in lst:
                newState = copy.deepcopy(self.state)
                newState[totalMin[0]][totalMin[1]] = n
                newPzl = Puzzle(newState)
                newPzl.removeSingles()
                if newPzl.isFailed():
                    continue
                nbrs.append(newPzl)
            return nbrs

    def solve(self):
        self.update()

        if self.isSolved():
            return self
        else:
            solution = solveLst(self.neighbors())
            if (solution is not None) and (solution.isSolved()):
                return solution
            else:
                return None


def solveLst(nbrs):
        for n in nbrs:
            solution = n.solve()
            if (solution is not None) and (solution.isSolved()):
                return solution
        return None
        
                        
                