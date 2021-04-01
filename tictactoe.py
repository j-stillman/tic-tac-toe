""" This file defines the tictactoe module """

import time
import random

""" Board: Holds a 2D array of characters, which represents a tic-tac-toe board """
class Board: 
    __size = 3
    __board = []

    """ Constructor for board """
    def __init__(self, size=3):

        # Set the size of the board. Don't let it go smaller than 3
        if size >= 3:
            self.__size = size
        else: 
            self.__size = 3

        # Build the board
        for i in range(size):               # Repeat [size] times (probably 3)

            row = []                        # Create a blank row list
            for j in range(size):           # Repeat [size] times (probably 3)
                row.append(" ")             # Append a space to that row
            
            self.__board.append(row)        # Append that row to the board itself


    """ Returns whether the spot (x, y) is empty. Note: x,y are in range [1,size], not [0,size-1] as it should be """
    def isEmpty(self, x, y):
        xx = x - 1                              # Create modified x-coordinate xx
        yy = y - 1                              # Create modified y-coordinate yy

        if ((xx >= 0 and xx < self.__size) and    
            (yy >= 0 and yy < self.__size)):    # Ensure that xx, yy is within range of size  

            val = self.__board[yy][xx]          # Retrieve the value in the board at row yy, col xx
            
            if val == " ":
                return True                     # Val is denoted by space string, therefore it is empty
            
            # Val is NOT denoted by space string, therefore it is occupied
            return False                    
        
        # xx, yy were NOT in range, so we can't run the function
        raise Exception("ERROR: isEmpty(x, y): x=" + str(x) + ", y=" + str(y) + " invalid for board size " + str(self.__size))


    """ Returns whether the entire board is empty or not """
    def boardEmpty(self):

        for i in range(self.__size):            # Repeat from i=0 to i=size-1 
            for j in range(self.__size):        # Repeat from j=0 to j=size-1
                if not self.isEmpty(i+1, j+1):       # Check the status of x = i+1, y = j+1.
                    return False                # We found an occupied spot. The board is NOT empty

        # We couldn't find an occupied spot. The board is thus empty.
        return True                

    
    """ Returns whether the entire board is full or not """
    def boardFull(self):

        for i in range(self.__size):            # Repeat from i=0 to i=size-1 
            for j in range(self.__size):        # Repeat from j=0 to j=size-1
                if self.isEmpty(i+1, j+1):           # Check the status of x = i+1, y = j+1.
                    return False                # We found an unoccupied spot. The board is NOT full

        # We couldn't find an empty spot. The board is thus full.
        return True   

            
    """ Fills a spot (x, y) with the character c. Note: x,y are in range [1,size], not [0,size-1] as it should be """
    def place(self, x, y, c):

        xx = x - 1                              # Create modified x-coordinate xx
        yy = y - 1                              # Create modified y-coordinate yy

        # Ensure first that the spot x, y is empty
        if not self.isEmpty(x, y):
            raise Exception("ERROR: place(x, y, c): x=" + str(x) + ", y=" + str(y) + ", c=\"" + str(c) + "\" invalid. This spot is taken.")

        # Ensure next that the spot x, y is in bounds
        if not ((xx >= 0 and xx < self.__size) and (yy >= 0 and yy < self.__size)): 
            raise Exception("ERROR: place(x, y, c): x=" + str(x) + ", y=" + str(y) + ", c=\"" + str(c) + "\" invalid. Position out of bounds.")
        
        self.__board[yy][xx] = c                # Assign c to row yy, col xx

    
    """ Returns whether the board has a winner (looks for 3-in-a-row or whatever size) """
    def getWinner(self):

        # Ensure that the board is not empty. If it is, don't return a character
        if self.boardEmpty(): 
            return None

        s = self.__size                             # Shorter way of saying self.__size which is gross
        b = self.__board                            # Shorter way of saying self.__board which is gross
        val = None                                  # The current value of the space as we go down a row/col/diag
        candidate = None                            # A value to compare val against when going down a row/col/diag

        # First try to go column by column
        for i in range(s):                          # Repeat from i=0 to i=size-1

            candidate = b[0][i]                     # Retrieve the top value in the column

            if candidate != " ":

                for j in range(1, s):               # Repeat from j=1 to j=size-1
                    val = b[j][i]                   # Retrieve the value down the column
                    if val != candidate: 
                        break                       # The value doesn't match the candidate, stop checking this column
                    else:
                        if j == s - 1:              # Check if we've reached the bottom of the column
                            return candidate        # If so, we can return the candidate as the winner

            else:
                continue                            # The top value in the column is empty, there CAN'T be a vertical sequence

        # Next try to go row by row
        for i in range(s):                          # Repeat from i=0 to i=size-1

            candidate = b[i][0]                     # Retrieve the first value in the row

            if candidate != " ":

                for j in range(1, s):               # Repeat from j=1 to j=size-1
                    val = b[i][j]                   # Retrieve the value across the row
                    if val != candidate: 
                        break                       # The value doesn't match the candidate, stop checking this row
                    else:
                        if j == s - 1:              # Check if we've reached the end of the row
                            return candidate        # If so, we can return the candidate as the winner

            else:
                continue                            # The top value in the column is empty, there CAN'T be a vertical sequence

        # Try to go diagonal down-right
        candidate = b[0][0]                         # Retrieve the top-left corner value

        if candidate != " ":                        # Ensure that something is actually in that corner

            for i in range(1, s):                   # Repeat from i=1 to i=size-1
                val = b[i][i]                       # Retrieve the value down the diagonal
                if val != candidate:                
                    break
                else: 
                    if i == s - 1:                  # Check if we've reached the end of the diagonal
                        return candidate            # If so, we can return the candidate as the winner

        # Try to go diagonal down-left
        candidate = b[0][s-1]                       # Retrive the top-right corner value

        if candidate != " ":                        # Ensure that something is actually in that corner

            for i in range(1, s):                   # Repeat from i=1 to i=size-1
                val = b[i][(s-1) - i]               # Retrieve the value down the diagonal
                if val != candidate:                
                    break
                else: 
                    if i == s - 1:                  # Check if we've reached the end of the diagonal
                        return candidate            # If so, we can return the candidate as the winner

        # We couldn't find a winning character (neither X nor O), so return null
        return None


    """ Returns the size of the board """
    def getSize(self):
        return self.__size


    """ Returns a string-version of the board as it currently is """
    def __str__(self):

        res = ""                                        # Result string to build up

        for i in range(self.__size):                    # Repeat from i=0 to i=size-1
            row = self.__board[i]                       # Get row i

            # DRAW THE X'S AND O'S
            for j in range(len(row)):                   # Repeat down the dow
                res = res + " " + str(row[j]) + " "     # Append the character
                if j != self.__size - 1: 
                    res = res + "|"                     # Only append a pipe character when it's NOT at the far right edge
            res = res + "\n"                            # Newline

            # DRAW THE BORDERS, BUT ONLY IF WE'RE NOT AT THE BOTTOM
            if i != self.__size - 1: 
                for j in range(len(row)):               # Repeat down the row
                    res = res + "---"                   # Append a floor chars
                    if j != self.__size - 1:
                        res = res + "+"                 # Only append a plus (corner) character when it's NOT at the far right edge
                res = res + "\n"                        # Newline

        return res


""" Player: Represents a game player, either a human or AI """
class Player:

    _winner = False                     # Whether this player is the game's winner
    _marker = " "                       # The marker that the player uses. Either X or O (at least it should be)

    """ Constructor for Player """
    def __init__(self, marker): 
        self._marker = marker


    """ Method to take a turn. Implement in the children """
    def takeTurn(self, board):
        pass


    """ Method to see if we are a winner yet """
    def isWinner(self): 
        return self._winner

    
    """ Method to return the player's marker/symbol """
    def getSymbol(self):
        return self._marker


""" HumanPlayer: Extends Player. It is a player that a user controls """
class HumanPlayer(Player): 

    __playerName = ""

    """ Constructor for HumanPlayer """
    def __init__(self, name, marker):
        super().__init__(marker)
        self.__playerName = name


    """ Method to verify that an input string is in character format """
    def isCharFormat(self, line):
        tokens = line.split()
        if len(tokens) == 1: 
            if not tokens[0].isdigit() and len(tokens[0]) == 1: 
                return True                                         # If there is one token, character and that character isn't numeric 

        # Otherwise it is false
        return False 


    """ Method to verify that an input string is in position format """
    def isPosFormat(self, line): 
        tokens = line.split()
        if len(tokens) == 2: 
            if tokens[0].isdigit() and tokens[1].isdigit(): 
                return True                                         # If there are two tokens and both tokens are numeric

        # Otherwise it is false
        return False


    """ Method to take a turn. Implemented here """
    def takeTurn(self, board):
        
        name = self.__playerName                    # Shorter variable name for self.__playerName
        symbol = self._marker                       # Shorter variable name for self._marker
        response = ""                               # String to store the input line into
        tokens = []                                 # List that stores the input as tokens


        """ Define what it means to get a valid input """
        def validMove(line):

            t = line.split()                        # Get the tokens from the line

            if self.isPosFormat(line):              # If the input is two integers and it's a valid spot
                
                bSize = board.getSize()          
                pos = (int(t[0]), int(t[1]))

                if (pos[0] >= 1 and pos[0] <= bSize) and (pos[1] >= 1 and pos[1] <= bSize): 
                    if board.isEmpty(pos[0], pos[1]):
                        return True 

            elif self.isCharFormat(line):           # If the input is a single character

                val = t[0].upper()
                if val == "Q": 
                    return True

            # If it's neither a valid position tuple nor the letter Q, then it's invalid 
            return False


        # First get the input
        response = input(str(name) + ", enter a position to place your " + str(symbol) + ", or q to quit: ")

        while not validMove(response):
            print("Invalid input, please try again.")
            response = input(str(name) + ", enter a position to place your " + str(symbol) + ", or q to quit: ")

        # Split the input into tokens
        tokens = response.split()

        if len(tokens) == 2:                            # If there are two inputs -> a position was entered 
            pos = (int(tokens[0]), int(tokens[1]))      # Construct a tuple out of that input
            board.place(pos[0], pos[1], symbol)         # Place the symbol into the board

            self._winner = board.getWinner()            # Check if we're a winner while we're at it
            return True                                 # End. Move was made successfully

        else:                                           # The input is a single character, it can only be the quit option 
            return False                                # End. Move was not made, and we're ending the game.

    """ Override string method """
    def __str__(self):
        return "I am a human player with symbol " + str(self._marker)


""" AIPlayer: Extends Player. It is a player that the program controls """
class AIPlayer(Player):

    """ Constructor for AIPlayer """
    def __init__(self, marker):
        super().__init__(marker)

    """ Method to take a turn. Implemented here """
    def takeTurn(self, board):
        
        symbol = self._marker           # Shorter variable name for self._marker
        size = board.getSize()          # Get the size of the board so we know our range
        xx = 0                          # The x-coordinate of where we will place our symbol
        yy = 0                          # The y-coordinate of where we will place our symbol

        # Generate random numbers until we get a free, valid space
        xx = random.randint(1, size)
        yy = random.randint(1, size)

        while not board.isEmpty(xx, yy): 
            xx = random.randint(1, size)
            yy = random.randint(1, size)
        
        # Place the symbol at the position we obtained
        board.place(xx, yy, symbol)

        self._winner = board.getWinner()    # Check if we're a winner from that move
        return True                         # End. Move was made successfully



    """ Override string method """
    def __str__(self):
        return "I am an AI player with symbol " + str(self._marker) 



""" TicTacToeGame: Manages the different stages of gameplay """
class TicTacToeGame:
    __p1 = None                 # Player object for p1
    __p2 = None                 # Player object for p2 
    __board = None              # The board that the game uses 

    __numHumans = 0             # The amount of human players playing [0, 2]
    __boardSize = 0             # The size of the board [3, infinity]

    __winnerName = ""           # The name of the winner when they are announced

    """ Constructor for TicTacToeGame """
    def __init__(self):
        pass

    """ Method to verify that an input string is in numeric (integer) format """
    def isIntFormat(self, line): 
        tokens = line.split()
        if len(tokens) == 1: 
            if tokens[0].isdigit(): 
                return True             # If there is only one token and that token is a digit, it's true

        # Otherwise it is false
        return False


    """ Method to verify that an input string is in character format """
    def isCharFormat(self, line):
        tokens = line.split()
        if len(tokens) == 1: 
            if not tokens[0].isdigit() and len(tokens[0]) == 1: 
                return True                                         # If there is one token, character and that character isn't numeric 

        # Otherwise it is false
        return False 


    """ Method to verify that an input string is in position format """
    def isPosFormat(self, line): 
        tokens = line.split()
        if len(tokens) == 2: 
            if tokens[0].isdigit() and tokens[1].isdigit(): 
                return True                                         # If there are two tokens and both tokens are numeric

        # Otherwise it is false
        return False


    """ Method to verify that an input is of any valid form """
    def isValidInput(self, line):
        return isCharFormat(line) or isIntFormat(line) or isPosFormat(line)


    """ Method to initialize the board and players """
    def initGame(self):

        response = ""                       # String that stores user input
        tokens = []                         # List that stores user input as tokens

        """ Define what it means to enter a valid board size """
        def validBoardSize(line): 

            if self.isIntFormat(line):      # Ensure that the format is one integer
                tokens = line.split()       # Get the tokens
                val = int(tokens[0])        # Retrieve the actual value entered as an int
                if val >= 3:                # If that value is 3 or more,
                    return True             # Then our input is valid as a board size

            # Test failed, not valid as a board size
            return False

        """ Define what it means to enter a valid number of players """
        def validNumPlayers(line):

            if self.isIntFormat(line):      # Ensure that the format is one integer
                tokens = line.split()       # Get the tokens
                val = int(tokens[0])        # Retrieve the actual value entered as an int
                if val >= 0 and val <= 2:   # If that value is in the range [0, 2],
                    return True             # Then our input is valid as a number of players

            # Test failed, not valid as a number of players
            return False


        """ Define what it means to enter a valid player symbol """
        def validPlayerSymbol(line):

            if self.isCharFormat(line):         # Ensure that the format is one character
                tokens = line.split()           # Get the tokens
                val = tokens[0].upper()         # Retrieve the actual character as upper case
                if val == "X" or val == "O":    # If that value is an X or O,
                    return True                 # Then our input is valid as a player symbol
            
            # Test failed, not valid as a player symbol
            return False


        # FIRST: GET THE SIZE OF THE BOARD ========================================================
        response = input("Enter a board size (at least 3): ")
        
        while not validBoardSize(response): 
            print("Invalid input, please try again.")
            response = input("Enter a board size (at least 3): ")

        # Turn the response into tokens and store the numerical value into __boardSize
        tokens = response.split()
        self.__boardSize = int(tokens[0])   

        self.__board = Board(self.__boardSize)

        # SECOND: GET THE NUMBER OF PLAYERS =======================================================
        response = input("Enter the number of humans playing (no more than 2): ")

        while not validNumPlayers(response):
            print("Invalid input, please try again.")
            response = input("Enter the number of humans playing (no more than 2): ")

        # Turn the response into tokens and store the numerical value into __numHumans
        tokens = response.split()
        self.__numHumans = int(tokens[0])

        # THIRD: ASSIGN SYMBOLS AND CREATE PLAYERS ================================================
        p1Symbol = ""
        p2Symbol = ""
        n = self.__numHumans

        if n >= 1: 
            # At least one player is a human. Ask p1 what they are, and p2 will be the opposite automatically
            response = input("Player 1, are you X or O? (type one): ")

            while not validPlayerSymbol(response):
                print("Invalid input, please try again.")
                response = input("Player 1, are you X or O? (type one): ")
            print()

            # Obtain the symbol itself as a string
            tokens = response.split()
            symbol = tokens[0].upper()

            if symbol == "X":                                           # If we chose X, then p1=X, p2=O
                p1Symbol = "X"
                p2Symbol = "O"
                print("Player 1 will be X, and Player 2 will be O.")
            else: 
                p1Symbol = "O"                                          # If we chose O, then p1=O, p2=X
                p2Symbol = "X"
                print("Player 1 will be O, and Player 2 will be X.")

            # Create the two players. Player 2 will be human or AI, depending on how many players we selected
            self.__p1 = HumanPlayer("Player 1", p1Symbol)
            if n > 1: 
                self.__p2 = HumanPlayer("Player 2", p2Symbol)
            else: 
                self.__p2 = AIPlayer(p2Symbol)

        else: 
            # In this case, both players are AI
            self.__p1 = AIPlayer("X")
            self.__p2 = AIPlayer("O")

        """
        print()
        print("We have now created the board and players. In sum: ")
        print("Board size is " + str(self.__boardSize) + ". Seen below:")
        print(self.__board)
        print()
        print("The number of human players is " + str(self.__numHumans) + ". P1 and P2 will greet you now:")
        print(self.__p1)
        print(self.__p2)
        print()
        """


    """ Method to see if either player has won yet """
    def winnerExists(self): 
        p1 = self.__p1          # Shorter variable name for self.__p1
        p2 = self.__p2          # Shorter variable name for self.__p2

        # Check if p1 or p2 are winners. If so, set the winner name and return true
        if p1.isWinner(): 
            self.__winnerName = "Player 1 (" + str(p1.getSymbol()) + ")"
            return True
        elif p2.isWinner(): 
            self.__winnerName = "Player 2 (" + str(p2.getSymbol()) + ")"
            return True

        # Neither players have won yet
        return False

    """ Method to run the game loop """ 
    def runGame(self):
        
        delayTime = 0.5                         # Amount of time to let the game breathe after showing the board
        board = self.__board                    # Shorter variable name for self.__board
        p1 = self.__p1                          # Shorter variable name for self.__p1
        p2 = self.__p2                          # Shorter variable name for self.__p2
        continueGame = True                     # Store this into the result of player.takeTurn()
        winner = False                          # Whether the game completed with a winner

        # First, show the board 
        print(board)
        time.sleep(delayTime)

        # Now go indefinitely until there is a winner
        while True: 
            continueGame = p1.takeTurn(board)
            if not continueGame: 
                break

            print(board)
            time.sleep(delayTime)

            if self.winnerExists(): 
                winner = True
                break 
            elif board.boardFull(): 
                break

            continueGame = p2.takeTurn(board)
            if not continueGame: 
                break 

            print(board)
            time.sleep(delayTime)

            if self.winnerExists(): 
                winner = True
                break 
            elif board.boardFull(): 
                break

        
        if continueGame:                                # If continueGame is true, then the game ended organically
            if winner:                                  # If winner is true, then the game has a winner
                print(self.__winnerName + " wins!")     # Tell the user(s) who the winner is
            else:                                       # Otherwise,
                print("Tie game!")                      # There is no winner, it's a tie
        else: 
            print("Game has been cut short.")           # If continueGame isn't true, then the game was ended with q


    """ Method to do everything, call this from your main program """
    def play(self): 

        self.initGame()
        self.runGame()

    






