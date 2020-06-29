#Sudoku Solver by Rahul.G
#This is a backtracking algorithm designed to solve sudoku puzzles
#All parts of the code were developed by me

#To input your own sudoku to be solved, scroll to the bottom of the code and input the values in the variable 'b'
#None spaces are places you need to figure out, soon I will develop a GUI version, until then hand input it by changing the code

#The Algorithm and how it works
#The center of this backtracking algorithm is a recursive function which will be shown later

#How the Algorithm functions
# 1. It will first establish a possibility board, which in essence lists every possible number a space on the board can be
# 2. To make the code more efficient, the possibility board can be cleaned, this can be done by using the static cells
#    provided in the puzzle. Using these cells, several possibilities from the cells can be removed
# 3. The algorithm then starts at the first non static cell in the playing board, and extracts all of the cells possibilities from the possibility board, this list of
#    possibilities is referred to as the cache of possibilities for that iteration or frame of that function
# 4. The algorithm will pick the first entry in the cache (index 0), and add it to the board, this limits the possibilities for the rest of the board, as such the possibility board will be updated
# 5. This new board, and the possibility board are then sent as arguments for the next iteration for this recursive function
# 6. This will keep happening until a cell in the possibility board has no values left in its possibility cachel, ie. the combinations chosen have made solving the board impossible
#    when this occours the function returns false, and returns to the previous iteration. It will then try the next value in its possibility cache, repeating the same process as above
# 7. This continues until the board is solved

from math import *

#This is the recursive function which acts as the center of the algorithm
def solve (original_board, possibility_board, truth_board, x,y):
#Due to how python handles pointers and refferences, and functions several versions of the same board are needed, each with a different purpose
#The "root" board is a copy of the one taken in as an argument when the iteration of the function started, it is necessary for it to be copied
#as otherwise, changes to it will effect the board in previous iterations of the function which will mess up the algorithm
#These root boards will NEVER change within this iteration of the function
#The "transfer" and "updated" boards for the actual playing board and the possibility board respectively and the board which will be the boards, which will be changed
#If a new value is to be added to a cell, or an update to a cell's possibilities it would be changed on these boards not the root boards
#This was done, as if a "branch" were to fail, the original starting point was needed, so that the algorithm could try a new "branch" from its given starting point

#Paramaters
#Original Board - The starting point for this iteration
#Possibility Board - The starting possibilities of all cells, as derived from the Original board
#Truth board, a board which is full of boolean values, True signifies that the cell is a given value, false indicates it is one the algorithm must fill in
#x,y the coordinates of the cell the function is currently on

    root_board = copy2dlist(original_board)
    transfer_board = copy2dlist(root_board)
    root_possibility_board = copy3dlist(possibility_board) #I made my own copy function, which uses nested for loops to copy values
    #This was done as using the copy() function returned a new pointed to the same object, which would end up changing the root boards

    #Checks if the board is solved
    if (issolved(original_board) == True):
        for i in range(9):
            print(original_board[i])  # PRINTS THE BOARD
        return True

    # Small piece of code to find the next cell in the board
    if (x > 8):
        x = 0
        y = y + 1

    # Finds the closest non static (given) point, by going left to right
    while (truth_board[y][x] == True):
        if (x >= 8):
            x = 0
            y = y + 1
        else:
            x = x + 1
    print(x,y)
    # Finds the cache of possibilities for the iteration of the function
    cache = []
    for i in range(len(root_possibility_board[y][x])):
        cache.append(root_possibility_board[y][x][i])

    #Tries the first value in the cache in the board
    transfer_board[y][x] = cache[0]

    #Makes sure this value within the context of all given points and algorithm inputted points is possible
    #and also makes sure that there are no cells which have no possible values due to its current value
    #tldr makes sure the value in the cells is acceptable and doesnt lead to a dead end (so far)
    #If the cache runs out, the function will return false as the branch has no working possibilities
    #If a cache value is false, it will keep going until it runs out or finds a possibility which could work
    valid_guess = False
    while (valid_guess != True):
        valid_guess = ispossible(transfer_board,x,y)
        if (valid_guess == False):
            if (len(cache) != 1 ):
                cache.pop(0)
                transfer_board[y][x] = cache[0]
            else:
                return False
        else:
            updated_possibility_board = update_p_board(transfer_board,root_possibility_board,x,y)
            impossible = isimpossible(updated_possibility_board,truth_board)
            if (impossible == True):
                valid_guess = False
                if (len(cache) != 1):
                    cache.pop(0)
                    transfer_board[y][x] = cache[0]
                else:
                    return False

    #Updates the possibility board based on the new value inputted into the board
    succeeded = False
    while (succeeded != True):
        updated_possibility_board = update_p_board(transfer_board, root_possibility_board, x, y)
        succeeded = solve(transfer_board,updated_possibility_board,truth_board,x+1,y) #The recursive, aspect, sends x+1 as it was to continue the branch to the next cell
        #If the cell value inputted is possible, it will continue the branch by sending that board back into the same function

        #If no more branches (cache empty) exist the function will return false
        if (succeeded == True):
           return True
        else:
            reroll = True
            transfer_board = copy2dlist(root_board) #Resetting the possibility and game board to the starting point so a new branch can be tried
            updated_possibility_board = copy3dlist(root_possibility_board)
            valid_guess = False

            while (valid_guess != True):

                if (reroll == True):
                    if (len(cache) != 1):
                        cache.pop(0)
                        transfer_board[y][x] = cache[0]
                        reroll = False
                    else:
                        return False
                valid_guess = ispossible(transfer_board, x, y)

                if (valid_guess == True):
                    updated_possibility_board = update_p_board(transfer_board, root_possibility_board, x, y)
                    impossible = isimpossible(updated_possibility_board, truth_board)
                    if (impossible == True):
                        valid_guess = False
                        reroll = True

                else:
                    reroll == True



def run(): #Change this board to what you would like to solve
    b =      [[5, 3, None, None, 7, None, None, None, None],
             [6, None, None, 1, 9, 5, None, None, None],
             [None, 9, 8, None, None, None, None, 6, None],
             [8, None, None, None, 6, None, None, None, 3],
             [4, None, None, 8, None, 3, None, None, 1],
             [7, None, None, None, 2, None, None, None, 6],
             [None, 6, None, None, None, None, 2, 8, None],
             [None, None, None, 4, 1, 9, None, None, 5],
             [None, None, None, None, 8, None, None, 7, 9]
             ]

    p, t = predboard(b)

    solve(b, p,t,0,0)


#Needed Extra Functions

#Functions which can copy and return 2d and 3d arrays
def copy2dlist (list):
    copy = []
    for y in range (len(list)):
        row = []
        for x in range (len(list[y])):
            row.append(list[y][x])
        copy.append(row)
    return copy
def copy3dlist (list):
    copy = []
    for y in range (len(list)):
        row = []
        for x in range (len(list[y])):
            cell = []
            for z in range (len(list[y][x])):
                cell.append(list[y][x][z])
            row.append(cell)
        copy.append(row)
    return copy

#Generates a  possibility board which is derived from the given points
def predboard (board):

    p_board = []

    for i in range(9):
        row = []
        for z in range (9):
            cell = []
            if (board[i][z] == None):
                cell = list(range(1,10))
            else:
                cell.append(board[i][z])
            row.append(cell)
        p_board.append(row)
    p_board, t_board = clean(board, p_board)
    return p_board, t_board

#Tells if the board inputted is impossible to be solved, by checking of cells in the possibility board have no possible values
def isimpossible(p_board,t_board):
    for y in range (9):
        for x in range (9):
            if (len(p_board[y][x]) <1 and t_board[y][x] == False):
                return True
    return False

#Is reffered to in predboard, this function acts as the cleaner, as it will take the values given in the puzzles and remove the appropriate possibilities from the possibility board
def clean(board, p_board):

    static_points = []
    t_board = []
    for y in range (9):
        for x in range (9):
            if (len(p_board[y][x]) == 1):
                static_points.append([x,y])
                p_board[y][x].clear()


    for y in range (9):
        row = []
        for x in range (9):
            if (static_points.count([x, y]) > 0):
                row.append(True)
            else:
                row.append(False)
        t_board.append(row)

    for i in range (len(static_points)):
        xcheck = static_points[i][0]
        ycheck = static_points[i][1]
        value = board[ycheck][xcheck]

        for x in range (9):
            if (len(p_board[ycheck][x]) != 1 and p_board[ycheck][x].count(value) != 0):
                index = p_board[ycheck][x].index(value)
                p_board[ycheck][x].pop(index)
        for y in range (9):
            if (len(p_board[y][xcheck]) != 1 and p_board[y][xcheck].count(value) != 0):
                index = p_board[y][xcheck].index(value)
                p_board[y][xcheck].pop(index)

        blockx = floor(xcheck / 3)
        blocky = floor(ycheck / 3)

        for column in range(3):
            for row in range(3):
                if (len(p_board[blocky * 3 + column][blockx * 3 + row]) != 1 and p_board[blocky * 3 + column][blockx * 3 + row].count(value) != 0):

                    index = p_board[blocky * 3 + column][blockx * 3 + row].index(value)
                    p_board[blocky * 3 + column][blockx * 3 + row].pop(index)


    return p_board, t_board

#Will tell if the board is solved
def issolved (board):
    for y in range (9):
        for x in range (9):
            if (board[y][x] == None):
                return False

    for x in range(9):
        cache = list(range(1, 10))
        for y in range (9):
            if (cache.index(board[y][x]) >= 0):
                cache.pop(cache.index(board[y][x]))
            else:
                return False

    for y in range(9):
        cache = list(range(1, 10))
        for x in range (9):
            if (cache.index(board[y][x]) >= 0):
                cache.pop(cache.index(board[y][x]))
            else:
                return False

    for by in range(3):
        for bx in range(3):
            cache = list(range(1, 10))
            for column in range(3):
                for row in range(3):
                    if (cache.index(board[by * 3 + column][bx * 3 + row]) >= 0):
                        cache.pop(cache.index(board[by * 3 + column][bx * 3 + row]))
                    else:
                        return False
    return True

#Tells if the value inputted is possible, only in refference to the those values around it, not if it makes the board impossible to solve
def ispossible (board,x,y):
    value = board[y][x]
    for column in range(9):
        if (column != y):
            if (board[column][x] == value):
                return False
    for row in range(9):
        if (row != x):
            if (board[y][row] == value):
                return False
    blockx = floor(x/3)
    blocky = floor(y/3)

    for column in range (3):
        for row in range (3):
            if not (blocky*3 + column == y and blockx*3 + row == x):
                if (board[blocky*3 + column][blockx*3 + row] == value):
                    return False
    return True

#Updatesthe possibility board given a new input on the playing board
def update_p_board(board, prob_board,x,y):
    value = board[y][x]
    p_board = copy3dlist(prob_board)
    for column in range(9):
        if (column != y):
            if (p_board[column][x].count(value) > 0):
                p_board[column][x].remove(value)
    for row in range(9):
        if (row != x):
            if (p_board[y][row].count(value) > 0):
                p_board[y][row].remove(value)

    blockx = floor(x/3)
    blocky = floor(y/3)

    for column in range (3):
        for row in range (3):
            if not (blocky*3 + column == y and blockx*3 + row == x):
                if (p_board[blocky*3 + column][blockx*3 + row].count(value) > 0):
                    p_board[blocky*3 + column][blockx*3 + row].remove(value)
    return p_board

#Will run the code
run()
