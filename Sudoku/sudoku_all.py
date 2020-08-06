from pytictoc import TicTocGenerator, tic, toc

def find(blanks, rows, cols, blox, solution):
    if blanks == []:
        return True
    
    i, j = blanks.pop()
    domain = list(set(rows[i]).intersection(set(cols[j])).intersection(set(blox[3*(i//3)+j//3])))
    if domain == []:
        blanks.append((i,j))
        return False

    for key in domain:
        solution.append((i, j, key))
        rows[i].remove(key)
        cols[j].remove(key)
        blox[3*(i//3)+j//3].remove(key)
        if find(blanks, rows, cols, blox, solution):
            return True
        solution.pop()
        rows[i].append(key)
        cols[j].append(key)
        blox[3*(i//3)+j//3].append(key)
    
    blanks.append((i,j))
    return False


def solveSudoku(boardStr):
    board = [0]*9

    for i in range(9):
        board[i] = boardStr[i*9:i*9+9]
    
    allDigs = [i+1 for i in range(9)]    
    rows = [allDigs.copy() for i in range(9)]
    cols = [allDigs.copy() for i in range(9)]
    blox = [allDigs.copy() for i in range(9)]
    
    blanks = []
    
    for i in range(9):
        for j in range(9):
            if board[i][j] == '.':
                blanks.append((i,j))
                continue
            key = int(board[i][j])
            try:
                rows[i].remove(key)
                cols[j].remove(key)
                blox[3*(i//3)+j//3].remove(key)
            except:
                return None
                

    solution = []
    
    if not find(blanks, rows, cols, blox, solution):
        return None
    
    for (i, j, key) in solution:
        s = board[i]
        s = s[:j] + str(key) + s[j+1:]
        board[i] = s
    
    return board

#####################
    
TicToc = TicTocGenerator() 
 

with open("Sudoku.csv") as f:
    content = f.readlines()

content.pop(0)

#for line in content:
allres = []

for i in range(len(content)):
#    problem = line.split(";")
#    problem = content[i].strip().split(";")
    problem = content[i].split(";")
    
    boardStr = problem[2]
    
    tic(TicToc)
    
    result = solveSudoku(boardStr)
    problem[2] = "".join(result) if result != None else "No solution"
    problem.insert(3, str(toc(TicToc)))
    allres.append((";".join(problem)))
#    print(result)
    print("\n".join(result)) if result != None else print("No solution")
    print(f"Problem {problem[0]} elapsed time: {problem[3]}")
    
with open("result.csv", "w") as f:
    f.writelines(allres)