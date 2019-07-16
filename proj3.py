# File:    proj3.py
# Author:  Nick Sica
# Date:    12/1/2018
# Section: 30
# E-mail:  nsica1@umbc.edu
# Description:  # Play Sudoku, or solve the game board. The user
# can save the board, play, and undo their moves with or without hints.


#CONSTANTS
#user options
QUIT = "q"
PLAY = "p"
SOLVE = "s"
SAVE = "s"
UNDO = "u"
YES = "y"
NO = "n"

#board constants
BOARD_MAX = 9
BOARD_MIN = 0
BLANK = "_"
SQUARE = 3

#number constants
MIN = 1
MAX = 10

# prettyPrint() prints the board with row and column labels,
#               and spaces the board out so that it looks nice
# Input:        board;   the square 2d game board (of integers) to print
# Output:       None;    prints the board in a pretty way
def prettyPrint(board):
    # print column headings and top border
    print("\n    1 2 3 | 4 5 6 | 7 8 9 ")
    print("  +-------+-------+-------+")

    for i in range(len(board)):
        # convert "0" cells to underscores  (DEEP COPY!!!)
        boardRow = list(board[i])
        for j in range(len(boardRow)):
            if boardRow[j] == 0:
                boardRow[j] = "_"
        # fill in the row with the numbers from the board
        print( "{} | {} {} {} | {} {} {} | {} {} {} |".format(i + 1,
                boardRow[0], boardRow[1], boardRow[2],
                boardRow[3], boardRow[4], boardRow[5],
                boardRow[6], boardRow[7], boardRow[8]) )

        # the middle and last borders of the board
        if (i + 1) % 3 == 0:
            print("  +-------+-------+-------+")



# gets the board from the user input
# Input: The file name that the board is stored in
# Output: board: the board to the game
def getBoard(fileName):
    #opens the user input filename 
    ofp = open(fileName, "r")
    puzzleList = ofp.readlines()
    #new List variable so i can append the file contents
    new_List = []

    
    for i in range(len(puzzleList)):
        #strips the whitespace and splits the commas
        new_Puzzle = puzzleList[i].strip("\n")
        new_Puzzle = puzzleList[i].split(",")
        #cast the contents of the list to integers
        for j in range(len(new_Puzzle)):
            new_Puzzle[j] = int(new_Puzzle[j])
        
        #append the puzzle to a new list
        new_List.append(new_Puzzle)

       
    ofp.close()

    
    return new_List
        


# savePuzzle() writes the contents a sudoku puzzle out
#              to a file in comma separated format
# Input:       board;    the square 2d puzzle (of integers) to write to a file
#              fileName; the name of the file to use for writing to
def savePuzzle(board, fileName):
    ofp = open(fileName, "w")
    for i in range(len(board)):
        rowStr = ""
        for j in range(len(board[i])):
            rowStr += str(board[i][j]) + ","
        # don't write the last comma to the file
        ofp.write(rowStr[ : len(rowStr)-1] + "\n")
    ofp.close()


# gets valid input for strings
# Input: play_Solve , string on what the user wants to do
# Output: Valid: boolean that is either true or false based on validity
def getValidInput(choice):
    #validates the users input
    while choice != PLAY and choice != SOLVE:
        print("That is an invalid input, please try again")
        choice = input("Play (p) or Solve(s)?: ")

    return choice 


# gets valid input for strings
# Input: user_Move, string on what the user wants to do
# Output: Valid: boolean that is either true or false based on validity
def getValidMove(choice):
    #validates that the users input is valid 
    while choice != PLAY and choice != SAVE and choice != UNDO \
          and choice != QUIT:
        print("That is an invalid input, please try again")
        choice = input("play number (p), save (s), undo (u), quit (q): ")

    return choice
        

# validates the user's move for row and column values
# Input: board: takes in the game board
 #       valid_Ints = list with the user values for row and column
# Output: valid_Move : booleans that returns if the values are valid
def valid_Board(valid_Ints):
    #validates that the users input is valid 
    while valid_Ints[0] > BOARD_MAX or valid_Ints[0] < BOARD_MIN:
        print("That is an invalid number. Please try again")
        #removes the invalid number from the list 
        row = int(input("Enter a row number: "))
        valid_Ints[0] = row - 1

    while valid_Ints[1] > BOARD_MAX or valid_Ints[1] < BOARD_MIN:
        print("That is an invalid number. Please try again")
        #removes the invalid number from the list 
        column = int(input("Enter a column number: "))
        valid_Ints[1] = column - 1

    return valid_Ints

# validates that the number the user wants to place can actually be placed there,
# if there is,re prompts the user for a new row and column
# Input: the board, and valid_Ints(list of the row and column value pair)
# Output: Valid_Ints (the row/column value pair) which may be new
def valid_Cell(board,valid_Ints):
    #sets variables
    row = 0
    column = 0
    #while the user entered row and column (row = 0 and column = 1)
    #does not have a number in the board already 
    while board[valid_Ints[0]][valid_Ints[1]] != 0:
        print("That spot on the board already has a number")
        #reprompts the user for a row number
        row = int(input("Enter a row number: "))
        valid_Ints[0] = row - 1
        #makes sure it is a valid input 
        valid_Ints = valid_Board(valid_Ints)

        #preprmpts the user for a column number and validates it 
        column = int(input("Enter a column number: "))
        valid_Ints[1] = column - 1
        valid_Ints = valid_Board(valid_Ints)

    return valid_Ints


# validates the number that the user wants to place in the puzzle
# Input: board : takes in the board
#        row: the user inputted row number,
#        column: user inputted column number
#        cell: the number the user wants to place in the board
# Output: cell: the value that they want to enter into the board
def valid_Puzzle(board,row,column,cell):
    while cell < MIN and cell >= MAX:
        #if the user's number is invalid, reprompts
        print("That is an invalid entry. Try again")
        cell = int(input("Enter a number to put in a cell (" \
                         + str(row + 1) + "," + str(column + 1) + "): "))

    #checks if the move is a legal move and satisfies all rules
    while legalMove(board,row,column,cell) == False:
        #checks why it doesnt satisfies the rules and prints which rule(s) it breaks 
        if checkRow(board,row,cell) == True:
            print("The number",cell,"is already in the row")
            
            
            
        if checkColumn(board,column,cell) == True:
            print("The number",cell,"is already in the column")
            
                        
            
        if checkBoxes(board, row - row % SQUARE,column - column % SQUARE,cell) == True:
            print("The number",cell,"is already in the square")

        #gets a new number from the user 
        cell = int(input("Enter a number to put in a cell (" \
                         + str(row + 1) + "," + str(column + 1) + "): "))

    return cell

# solves the game recursively
# Input: board: the current game board
# Output:board: the solved game board
def solve_Game(board):
    #keeps track of the index 
    indexList = []
    #if there are no empty locations stop
    if checkLocations(board) == True:
        return True

    else:
        #sets the index to the location of the blank spot
        indexList = checkLocations(board)

        #sets the row number to the first index in the list
        #sets the column number to the second index in the list 
        row = indexList[0]
        column = indexList[1]

        #runs the loop for all the digits 
        for i in range(MIN,MAX):
            #if the digit can be placed in the spot 
            if legalMove(board,row,column,i) == True:
                #places the digit into the spot 
                board[row][column] = i
                #recursive call, goes through all of the recursions
                #and it returns true when done and it should be solved
                #approaches the base case as it is lowering the number
                #of blank spots
                if solve_Game(board):
                    return True

                #if it is not valid that it resets the index to 0
                #so it can backtrack succesfully hopefully
                board[row][column] = 0
        #if something goes wrong and it breaks
        return False


######RULES FUNCTIONS######

#searches the board to find the next blank
#if there is a blank, the refrence list will be set to that location
#Input: board (the board)
#Output: returns a list if there are still blanks in the board
#        returns True if there is no more blanks
def checkLocations(board):
    #chekcs if there are any empty spaces in the board 
    indexList = []
    for i in range(BOARD_MIN,BOARD_MAX):
        for j in range(BOARD_MIN,BOARD_MAX):
            if board[i][j] == 0:

                indexList = [i,j]

                return indexList
    return True


#returns a boolean which tells whether the number is in the same row
#Input: board (the board), row(the row number)
#       and num(the number trying to be placed)
#Output: boolean value true or false  
def checkRow(board,row,num):
    #runs through that user's row, to check if the num is there 
    for i in range(BOARD_MAX):
        if board[row][i] == num:
            return True

    return False

#returns a boolean value which tells whether the number is in the same column
#Input: the board, the column number and the digit trying to be placed
#Output: a boolean either true or false based on if the digit is in the board
def checkColumn(board,column,num):
    #runs through the column to check if the num is there 
    for i in range(BOARD_MAX):
        if board[i][column] == num:
            return True

    return False

#returns a boolean value that tells whether the number is in the same square
#Input: board(the board), rowStart(int) and colStart(int) 
#Output: a boolean that returns true or false if the number is in the box
def checkBoxes(board,row,column,num):
    #runs through the squares to check if the num is there 
#checks 3x3 squares
    for i in range(SQUARE):
        for j in range(SQUARE):
            if board[i + row][j + column] == num:
                return True

    return False


#returns the values for the previous three functions 
#Input: takes in the board, the row number, the column number and the digit
#trying to be placed 
#Output: returns a boolean value
def legalMove(board,row,column,num):
    #returns the previous true/false of the functions to either the solve function or main
    #this function was easier to do separately, it was easier for me to understand everything
    #and see what i needed for it all to work
    return not checkRow(board,row,num) \
        and not checkColumn(board,column,num) \
        and not checkBoxes(board, row - row % SQUARE,column - column % SQUARE,num)



# undoes the user's previous move
# Input: board: the game board
#        prev_Row: list with the previous row moves
#        prev_Col: list with the previous column moves
# Output: None: prints that the last move was undone
def undo_Move(board,prev_Row,prev_Col):

    #sets length of the list of the previous row/column pairs
    row_Length = len(prev_Row)
    col_Length = len(prev_Col)

    #if the length is greater than 0, then it undoes the last move
    if row_Length > 0 and col_Length > 0:
        last_Row = prev_Row[row_Length - 1]
        last_Move = prev_Col[col_Length - 1]
        board[last_Row][last_Move] = 0
    else:
        print("There are no moves to undo")

    



def main():
    #variables 
    win = False
    correct = False
    stop = False
    prev_Row = []
    prev_Col = []
    prev_Move = []
    #gets filename 
    ifp = input("Enter the filename of the Sudoku Puzzle: ")
    #gets the board 
    board = getBoard(ifp)

    #prints board 
    prettyPrint(board)
    #user input on if they want to play or solve 
    play_Solve = input("Play (p) or Solve(s)?: ")
    #validates the input
    play_Solve = getValidInput(play_Solve)

    #if the user chooses solve,solves then prints the board 
    if play_Solve == SOLVE:
        if solve_Game(board) == True:
            prettyPrint(board)
        else:
            print("error")

    #if the user decides to play 
    elif play_Solve == PLAY:
        correct_Check = input("Correctness Checking (y/n): ")

        #validates the input 
        while correct_Check != YES and correct_Check != NO:
            print("That is an invalid input. Please try again")
            correct_Check = input("Correctness Checking (y/n): ")

        #if the user wants to use correctness checking 
        if correct_Check == YES:
            user_Move = ""
            #gets a solved version of the board to compare to 
            solved = getBoard(ifp)
            solve_Game(solved)
            #while win is false and the user hasnt quit 
            while win == False and user_Move != QUIT:
                prettyPrint(board)

                #gets user moves and validates it 
                user_Move = input("play number (p), save (s), undo (u), quit (q): ")
                user_Move = getValidMove(user_Move)

                #if the user wants to play the game 
                if user_Move == PLAY:
                    #this list is for the rows and column 
                    valid_Ints = [0,0]
                    #gets input for the row  and validates it 
                    row = int(input("Enter a row number: "))
                    valid_Ints[0] = row - 1
                    valid_Ints = valid_Board(valid_Ints)

                    #gets the column and validates it 
                    column = int(input("Enter a column number: "))
                    valid_Ints[1] = column - 1
                    valid_Ints = valid_Board(valid_Ints)
                    #validates that the spot the user chose, a number can be put there 
                    valid_Ints = valid_Cell(board,valid_Ints)

                    #if any changes occured in validation then it updates the row and column
                    row = valid_Ints[0]
                    column = valid_Ints[1]
                    #gets user input for the choice 
                    cell_Choice = int(input("Enter a number to put in a cell (" \
                                            + str(row + 1) + "," + str(column + 1) + "): "))

                    #validates the input 
                    cell = valid_Puzzle(board,row,column,cell_Choice)
                    #if the move validates the rules of Sudoku
                    if legalMove(board,row,column,cell) == True:
                        #put the number in 
                        board[row][column] = cell

                        #compares the user's move to the solved board
                        #if it is not the same then it makes the user's move back to a 0
                        if board[row][column] != solved[row][column]:
                            board[row][column] = 0
                            print("The number " + str(cell) \
                                  + (" does not belong in the cell (") \
                                  + str(row + 1) + "," + str(column + 1) + ")")
                        #otherwise it just keeps it and adds it to the previous move lists 
                        else:
                            prev_Row.append(row)
                            prev_Col.append(column)
                            
                    #if the user's board is the same as the solved board then there is a winner 
                    if board == solved:
                        print("WINNER!!!!!")
                        win = True
                        prettyPrint(board)

                #if the user chose to undo then the it undoes the previous move 
                elif user_Move == UNDO:

                    undo_Move(board,prev_Row,prev_Col)
                    #if the length of the previous move lists are greater than 0, then it removes the last items 
                    if len(prev_Row) > 0 and len(prev_Col) > 0:
                        prev_Row = prev_Row[:-1]
                        prev_Col = prev_Col[:-1]
                        print("Removed your previous move")
                #if the user wants to save the game, then it saves the game. Thanks Neary!
                elif user_Move == SAVE:
                   user_File = input("Enter the name of the file you want to save to: ")
                   savePuzzle(board,user_File)
                   print("File saved")

                #if the user wants to quit then it quits 
                elif user_Move == QUIT:
                    prettyPrint(board)
                    print("Goodbye, here is your final board")

                    
        #if the user does not want to have correctness checking 
        elif correct_Check == NO:
            user_Move = ""
            #gets solved version of board to compare to 
            solved = getBoard(ifp)
            solve_Game(solved)
            #while the game hasnt been won and the user hasnt quit 
            while win == False and user_Move != QUIT:
                prettyPrint(board)
                #gets input and validates it 
                user_Move = input("play number (p), save (s), undo (u), quit (q): ")
                user_Move = getValidMove(user_Move)
                
                #if the user wants to play                        
                if user_Move == PLAY:
                    #list created to remeber the row and column inputs 
                    valid_Ints = [0,0]
                    #gets row and validates it 
                    row = int(input("Enter a row number: "))
                    valid_Ints[0] = row - 1
                    valid_Ints = valid_Board(valid_Ints)
                    #gets column and validates it 
                    column = int(input("Enter a column number: "))
                    valid_Ints[1] = column - 1
                    valid_Ints = valid_Board(valid_Ints)
                    #validates that the row and column pair has a 0 
                    valid_Ints = valid_Cell(board,valid_Ints)
                    #updates the row and column in case that there was a change in the validation
                    row = valid_Ints[0]
                    column = valid_Ints[1]
                    #gets choice for the cell input 
                    cell_Choice = int(input("Enter a number to put in a cell (" \
                                            + str(row + 1) + "," + str(column + 1) + "): "))
                    
                    #validation and places the number in the board if it satisfies all of the rules 
                    cell = valid_Puzzle(board,row,column,cell_Choice)
                    if legalMove(board,row,column,cell) == True:
                        board[row][column] = cell

                        #appends the move to the previous move lists for undoing 
                        prev_Row.append(row)
                        prev_Col.append(column)
                    #if game won, then print this 
                    if board == solved:
                        print("WINNER!!!!!")
                        win = True
                        prettyPrint(board)
                #if the user wants to undo the last move 
                elif user_Move == UNDO:
                    
                    undo_Move(board,prev_Row,prev_Col)
                    #removes the last items in the previous move lists if they are not empty 
                    if len(prev_Row) > 0 and len(prev_Col) > 0: 
                        prev_Row = prev_Row[:-1]
                        prev_Col = prev_Col[:-1]
                        print("Removed your previous move")
                #if the user chose to save. Thanks Neary!
                elif user_Move == SAVE:
                   user_File = input("Enter the name of the file you want to save to: ")
                   savePuzzle(board,user_File)
                   print("File saved")

                #if the user chose to quit, then it quits
                elif user_Move == QUIT:
                    prettyPrint(board)
                    print("Goodbye, here is your final board")
                   

                                        
                
        

main()

