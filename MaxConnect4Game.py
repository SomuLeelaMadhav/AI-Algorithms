'''Name: Somu LeelaMadhav
ID: 1002028333
Programming language used : Python
File name: MaxConnect4Game.py'''


'''
MaxConnect4Game.py file has minmax , alpha beta, beta alpha and other functions such as displaying the game board and printing the score'''


import copy #copying the items done by deepcopy
import random   #importing for using random variables 
import sys

val_utility = {}     # storing the utility value of the function
infinity = float('inf')     # defining a infinite value

class MaxConnect4game:  
    def __init__(self): 
        self.gameBoard = [[0 for i in range(7)] for j in range(6)]
        self.current_Move = 0
        self.pieceCount = 0
        self.Player1Score = 0
        self.Player2Score = 0
        self.game_File = None
        self.computer_Column = None
        self.d = 1

    
    def get_piece_count(self):    # returning the total piece count of the game board
        return sum(1 for row in self.gameBoard for piece in row if piece)
    
    def check_piece_count(self):  # is player already played or not
        self.pieceCount = sum(1 for row in self.gameBoard for p in row if p)

    
    def print_gameBoard_file(self): #defining a funtion for printing the game board
        for row in self.gameBoard:
            self.game_File.write(''.join(str(col) for col in row) + '\r')
        self.game_File.write('%s\r' % str(self.current_Move))

    def play_piece(self, column):    # function for Letting the current pllayer move in the board 
        if not self.gameBoard[0][column]:
            for i in range(5, -1, -1):
                if not self.gameBoard[i][column]:
                    self.gameBoard[i][column] = self.current_Move
                    self.pieceCount += 1
                    return 1
    def display_gameBoard(self):    #This is the function to display the gameboard
        print(' -----------------')
        for i in range(6):
            print(' |',end="")
            for j in range(7):
                print('%d' % int(self.gameBoard[i][j]),end="")
            print('| ')
        print(' -----------------')
                

    def check_Piece(self, c, o): #validity of the piece can be checked by this function
        if not self.gameBoard[0][c]:
            for i in range(5, -1, -1):
                if not self.gameBoard[i][c]:
                    self.gameBoard[i][c] = o
                    self.pieceCount += 1
                    return 1

    def maxVal(self, Current_Node):  # function for restoring the state of the minmax value. 
        node = copy.deepcopy(Current_Node)#copy the board can be done by deep copy
        Child_Node = []
        for i in range(7):
            Current_State = self.play_piece(i)
            if Current_State != None:
                Child_Node.append(self.gameBoard)
                self.gameBoard = copy.deepcopy(node)
        return Child_Node

    def minVal(self, currentNode):  #returning the state for the minimun value is done by this funtion
        node = copy.deepcopy(currentNode)
        if self.current_Move == 1:
            opponent = 2
        elif self.current_Move == 2:
            opponent = 1
        Child_Node = []
        for i in range(7):#for this in range
            currentState = self.check_Piece(i, opponent)
            if currentState != None:
                Child_Node.append(self.gameBoard)
                self.gameBoard = copy.deepcopy(node)
        return Child_Node
    
    def betaAlpha(self,currentNode, alpha, beta, depth):    # function for beta alpha puring (min val)
        value = infinity#set value to infinity
        child_node = self.minVal(currentNode)
        if child_node == [] or depth == 0:
            self.score_Count()
            return self.eval_Calc(self.gameBoard)
        else:
            for node in child_node:
                self.gameBoard = copy.deepcopy(node)
                value = min(value, self.alphaBeta(node, alpha, beta, depth - 1)) #value is minimum
                if value <= alpha:#if value is less than alpha, then return value
                    return value
                beta = min(beta, value)#beta  is the minimum of beta, value
        return value#return value
    

    def alphaBeta(self, current_Node, a, b, d):   # function for alpha beta puring (max val)
        value = -infinity#defining value to be minus inifinty
        childNode = self.maxVal(current_Node)
        if childNode == [] or d == 0:
            self.score_Count()
            return self.eval_Calc(self.gameBoard)
        else:
            for node in childNode:
                self.gameBoard = copy.deepcopy(node)
                value = max(value, self.betaAlpha(node, a, b, d - 1))
                if value >= b:
                    return value
                a = max(a, value)
            return value

    
    def minMax(self, depth):    # plain min max algorithm for game board 
        current_State = copy.deepcopy(self.gameBoard)
        for i in range(7):
            if self.play_piece(i) != None:
                if self.pieceCount == 42 or self.d == 0:
                    self.gameBoard = copy.deepcopy(current_State)
                    return i
                else:
                    val = self.betaAlpha(self.gameBoard, -infinity, infinity, depth - 1)
                    val_utility[i] = val
                    self.gameBoard = copy.deepcopy(current_State)
        max_Utility_Val = max([i for i in val_utility.values()])
        for i in range(7):
            if i in val_utility:
                if val_utility[i] == max_Utility_Val:
                    val_utility.clear()
                    return i

    def verticalCheck(self, row, column, state, streak):    # checking for the vertical piece in a row
        consecutiveCount = 0
        for i in range(row, 6):
            if state[i][column] == state[row][column]:
                consecutiveCount += 1
            else:
                break
        if consecutiveCount >= streak:
            return 1
        else:
            return 0
    
    def streakCalc(self, state, color, streak):     # function for checking which type of connectfour goes
        count = 0
        for i in range(6):
            for j in range(7):
                if state[i][j] == color:
                    count += self.verticalCheck(i, j, state, streak)
                    count += self.horizontalCheck(i, j, state, streak)
                    count += self.diagonalCheck(i, j, state, streak)
        return count
            

    def horizontalCheck(self, row, column, state, streak):  # checking for the horizontal piece in the column
        count = 0
        for j in range(column, 7):
            if state[row][j] == state[row][column]:
                count += 1
            else:
                break
        if count >= streak:
            return 1
        else:
            return 0

    def diagonalCheck(self, row, column, state, streak):    # checking for the diagonal check in the borad
        total = 0
        count = 0
        j = column
        for i in range(row, 6):
            if j > 6:
                break
            elif state[i][j] == state[row][column]:
                count += 1
            else:
                break
            j += 1
        if count >= streak:
            total += 1
        count = 0
        j = column
        for i in range(row, -1, -1):
            if j > 6:
                break
            elif state[i][j] == state[row][column]:
                count += 1
            else:
                break
            j += 1
        if count >= streak:
            total += 1
        return total

    
    def change_Move(self):   # function for changing the move to the next player 
        if self.current_Move == 1:
            self.current_Move = 2
        elif self.current_Move == 2:
            self.current_Move = 1

    
    def eval_function(self): # function for one move color and what the next color is 
        if self.current_Move == 1:
            one_move_color = 2
        elif self.current_Move == 2:
            one_move_color = 1
        return one_move_color

    def comp_Eval_Calc(self, state):  # calculating the evalution function of computer player
        one_move_color = self.eval_function()
        comp_fours = self.streakCalc(state, one_move_color, 4)
        comp_threes = self.streakCalc(state, one_move_color, 3)
        comps_twos = self.streakCalc(state, one_move_color, 2)
        return (comp_fours * 37044 + comp_threes * 882 + comps_twos * 21)

    def eval_Calc(self, state):  #function for calucating the difference in the steak of computer vs non computer
        return self.playerEvalCalc(state) - self.comp_Eval_Calc(state)

    
    def ai_Play(self):   # function for computing the computer move
        random_col = self.minMax(int(self.d))
        result = self.play_piece(random_col)
        if not result:
            print('No Result')
        else:
            print('Player: %d, Column: %d\n' % (self.current_Move, random_col + 1))
            self.change_Move()
    
    def playerEvalCalc(self, state):    # calculating the streak for the non computer player
        player_fours = self.streakCalc(state, self.current_Move, 4)
        player_threes = self.streakCalc(state, self.current_Move, 3)
        player_twos = self.streakCalc(state, self.current_Move, 2)
        return (player_fours * 37044 + player_threes * 882 + player_twos * 21) # numbers are the permutation for each fours in a row, threes in a row and twos in a row
        

    def score_Count(self):   # function for returning the score count i.e. fours in a row
        self.Player1Score = 0;
        self.Player2Score = 0;
        # Checking the board horizontally
        for row in self.gameBoard:
            # Checking the game board for player 1
            if row[0:4] == [1] * 4:
                self.Player1Score += 1
            if row[1:5] == [1] * 4:
                self.Player1Score += 1
            if row[2:6] == [1] * 4:
                self.Player1Score += 1
            if row[3:7] == [1] * 4:
                self.Player1Score += 1
            # Checking  the game board for player 2
            if row[0:4] == [2] * 4:
                self.Player2Score += 1
            if row[1:5] == [2] * 4:
                self.Player2Score += 1
            if row[2:6] == [2] * 4:
                self.Player2Score += 1
            if row[3:7] == [2] * 4:
                self.Player2Score += 1
        # diagonally checking the game board 
        # checking the gameboard for player 2
        if (self.gameBoard[2][0] == 2 and self.gameBoard[3][1] == 2 and
                self.gameBoard[4][2] == 2 and self.gameBoard[5][3] == 2):
            self.Player2Score += 1
        if (self.gameBoard[1][0] == 2 and self.gameBoard[2][1] == 2 and
                self.gameBoard[3][2] == 2 and self.gameBoard[4][3] == 2):
            self.Player2Score += 1
        if (self.gameBoard[2][1] == 2 and self.gameBoard[3][2] == 2 and
                self.gameBoard[4][3] == 2 and self.gameBoard[5][4] == 2):
            self.Player2Score += 1
        if (self.gameBoard[0][0] == 2 and self.gameBoard[1][1] == 2 and
                self.gameBoard[2][2] == 2 and self.gameBoard[3][3] == 2):
            self.Player2Score += 1
        if (self.gameBoard[1][1] == 2 and self.gameBoard[2][2] == 2 and
                self.gameBoard[3][3] == 2 and self.gameBoard[4][4] == 2):
            self.Player2Score += 1
        if (self.gameBoard[2][2] == 2 and self.gameBoard[3][3] == 2 and
                self.gameBoard[4][4] == 2 and self.gameBoard[5][5] == 2):
            self.Player2Score += 1
        if (self.gameBoard[0][1] == 2 and self.gameBoard[1][2] == 2 and
                self.gameBoard[2][3] == 2 and self.gameBoard[3][4] == 2):
            self.Player2Score += 1
        if (self.gameBoard[1][2] == 2 and self.gameBoard[2][3] == 2 and
                self.gameBoard[3][4] == 2 and self.gameBoard[4][5] == 2):
            self.Player2Score += 1
        if (self.gameBoard[2][3] == 2 and self.gameBoard[3][4] == 2 and
                self.gameBoard[4][5] == 2 and self.gameBoard[5][6] == 2):
            self.Player2Score += 1
        if (self.gameBoard[0][2] == 2 and self.gameBoard[1][3] == 2 and
                self.gameBoard[2][4] == 2 and self.gameBoard[3][5] == 2):
            self.Player2Score += 1
        if (self.gameBoard[1][3] == 2 and self.gameBoard[2][4] == 2 and
                self.gameBoard[3][5] == 2 and self.gameBoard[4][6] == 2):
            self.Player2Score += 1
        if (self.gameBoard[0][3] == 2 and self.gameBoard[1][4] == 2 and
                self.gameBoard[2][5] == 2 and self.gameBoard[3][6] == 2):
            self.Player2Score += 1
        if (self.gameBoard[0][3] == 2 and self.gameBoard[1][2] == 2 and
                self.gameBoard[2][1] == 2 and self.gameBoard[3][0] == 2):
            self.Player2Score += 1
        if (self.gameBoard[0][4] == 2 and self.gameBoard[1][3] == 2 and
                self.gameBoard[2][2] == 2 and self.gameBoard[3][1] == 2):
            self.Player2Score += 1
        if (self.gameBoard[1][3] == 2 and self.gameBoard[2][2] == 2 and
                self.gameBoard[3][1] == 2 and self.gameBoard[4][0] == 2):
            self.Player2Score += 1
        if (self.gameBoard[0][5] == 2 and self.gameBoard[1][4] == 2 and
                self.gameBoard[2][3] == 2 and self.gameBoard[3][2] == 2):
            self.Player2Score += 1
        if (self.gameBoard[1][4] == 2 and self.gameBoard[2][3] == 2 and
                self.gameBoard[3][2] == 2 and self.gameBoard[4][1] == 2):
            self.Player2Score += 1
        if (self.gameBoard[2][3] == 2 and self.gameBoard[3][2] == 2 and
                self.gameBoard[4][1] == 2 and self.gameBoard[5][0] == 2):
            self.Player2Score += 1
        if (self.gameBoard[0][6] == 2 and self.gameBoard[1][5] == 2 and
                self.gameBoard[2][4] == 2 and self.gameBoard[3][3] == 2):
            self.Player2Score += 1
        if (self.gameBoard[1][5] == 2 and self.gameBoard[2][4] == 2 and
                self.gameBoard[3][3] == 2 and self.gameBoard[4][2] == 2):
            self.Player2Score += 1
        if (self.gameBoard[2][4] == 2 and self.gameBoard[3][3] == 2 and
                self.gameBoard[4][2] == 2 and self.gameBoard[5][1] == 2):
            self.Player2Score += 1
        if (self.gameBoard[1][6] == 2 and self.gameBoard[2][5] == 2 and
                self.gameBoard[3][4] == 2 and self.gameBoard[4][3] == 2):
            self.Player2Score += 1
        if (self.gameBoard[2][5] == 2 and self.gameBoard[3][4] == 2 and
                self.gameBoard[4][3] == 2 and self.gameBoard[5][2] == 2):
            self.Player2Score += 1
        if (self.gameBoard[2][6] == 2 and self.gameBoard[3][5] == 2 and
                self.gameBoard[4][4] == 2 and self.gameBoard[5][3] == 2):
            self.Player2Score += 1 
        # Diagnolly checking the gameboard for player 1
        if (self.gameBoard[2][0] == 1 and self.gameBoard[3][1] == 1 and
                self.gameBoard[4][2] == 1 and self.gameBoard[5][3] == 1):
            self.Player1Score += 1
        if (self.gameBoard[1][0] == 1 and self.gameBoard[2][1] == 1 and
                self.gameBoard[3][2] == 1 and self.gameBoard[4][3] == 1):
            self.Player1Score += 1
        if (self.gameBoard[2][1] == 1 and self.gameBoard[3][2] == 1 and
                self.gameBoard[4][3] == 1 and self.gameBoard[5][4] == 1):
            self.Player1Score += 1
        if (self.gameBoard[0][0] == 1 and self.gameBoard[1][1] == 1 and
                self.gameBoard[2][2] == 1 and self.gameBoard[3][3] == 1):
            self.Player1Score += 1
        if (self.gameBoard[1][1] == 1 and self.gameBoard[2][2] == 1 and
                self.gameBoard[3][3] == 1 and self.gameBoard[4][4] == 1):
            self.Player1Score += 1
        if (self.gameBoard[2][2] == 1 and self.gameBoard[3][3] == 1 and
                self.gameBoard[4][4] == 1 and self.gameBoard[5][5] == 1):
            self.Player1Score += 1
        if (self.gameBoard[0][1] == 1 and self.gameBoard[1][2] == 1 and
                self.gameBoard[2][3] == 1 and self.gameBoard[3][4] == 1):
            self.Player1Score += 1
        if (self.gameBoard[1][2] == 1 and self.gameBoard[2][3] == 1 and
                self.gameBoard[3][4] == 1 and self.gameBoard[4][5] == 1):
            self.Player1Score += 1
        if (self.gameBoard[2][3] == 1 and self.gameBoard[3][4] == 1 and
                self.gameBoard[4][5] == 1 and self.gameBoard[5][6] == 1):
            self.Player1Score += 1
        if (self.gameBoard[0][2] == 1 and self.gameBoard[1][3] == 1 and
                self.gameBoard[2][4] == 1 and self.gameBoard[3][5] == 1):
            self.Player1Score += 1
        if (self.gameBoard[1][3] == 1 and self.gameBoard[2][4] == 1 and
                self.gameBoard[3][5] == 1 and self.gameBoard[4][6] == 1):
            self.Player1Score += 1
        if (self.gameBoard[0][3] == 1 and self.gameBoard[1][4] == 1 and
                self.gameBoard[2][5] == 1 and self.gameBoard[3][6] == 1):
            self.Player1Score += 1
        if (self.gameBoard[0][3] == 1 and self.gameBoard[1][2] == 1 and
                self.gameBoard[2][1] == 1 and self.gameBoard[3][0] == 1):
            self.Player1Score += 1
        if (self.gameBoard[0][4] == 1 and self.gameBoard[1][3] == 1 and
                self.gameBoard[2][2] == 1 and self.gameBoard[3][1] == 1):
            self.Player1Score += 1
        if (self.gameBoard[1][3] == 1 and self.gameBoard[2][2] == 1 and
                self.gameBoard[3][1] == 1 and self.gameBoard[4][0] == 1):
            self.Player1Score += 1
        if (self.gameBoard[0][5] == 1 and self.gameBoard[1][4] == 1 and
                self.gameBoard[2][3] == 1 and self.gameBoard[3][2] == 1):
            self.Player1Score += 1
        if (self.gameBoard[1][4] == 1 and self.gameBoard[2][3] == 1 and
                self.gameBoard[3][2] == 1 and self.gameBoard[4][1] == 1):
            self.Player1Score += 1
        if (self.gameBoard[2][3] == 1 and self.gameBoard[3][2] == 1 and
                self.gameBoard[4][1] == 1 and self.gameBoard[5][0] == 1):
            self.Player1Score += 1
        if (self.gameBoard[0][6] == 1 and self.gameBoard[1][5] == 1 and
                self.gameBoard[2][4] == 1 and self.gameBoard[3][3] == 1):
            self.Player1Score += 1
        if (self.gameBoard[1][5] == 1 and self.gameBoard[2][4] == 1 and
                self.gameBoard[3][3] == 1 and self.gameBoard[4][2] == 1):
            self.Player1Score += 1
        if (self.gameBoard[2][4] == 1 and self.gameBoard[3][3] == 1 and
                self.gameBoard[4][2] == 1 and self.gameBoard[5][1] == 1):
            self.Player1Score += 1
        if (self.gameBoard[1][6] == 1 and self.gameBoard[2][5] == 1 and
                self.gameBoard[3][4] == 1 and self.gameBoard[4][3] == 1):
            self.Player1Score += 1
        if (self.gameBoard[2][5] == 1 and self.gameBoard[3][4] == 1 and
                self.gameBoard[4][3] == 1 and self.gameBoard[5][2] == 1):
            self.Player1Score += 1
        if (self.gameBoard[2][6] == 1 and self.gameBoard[3][5] == 1 and
                self.gameBoard[4][4] == 1 and self.gameBoard[5][3] == 1):
            self.Player1Score += 1
      # Checking the game board vertically
        for j in range(7):
            # player 1's game board is being checked here
            if (self.gameBoard[0][j] == 1 and self.gameBoard[1][j] == 1 and
                    self.gameBoard[2][j] == 1 and self.gameBoard[3][j] == 1):
                self.Player1Score += 1
            if (self.gameBoard[1][j] == 1 and self.gameBoard[2][j] == 1 and
                    self.gameBoard[3][j] == 1 and self.gameBoard[4][j] == 1):
                self.Player1Score += 1
            if (self.gameBoard[2][j] == 1 and self.gameBoard[3][j] == 1 and
                    self.gameBoard[4][j] == 1 and self.gameBoard[5][j] == 1):
                self.Player1Score += 1
            # vertically checking the game of player 2
            if (self.gameBoard[0][j] == 2 and self.gameBoard[1][j] == 2 and
                    self.gameBoard[2][j] == 2 and self.gameBoard[3][j] == 2):
                self.Player2Score += 1
            if (self.gameBoard[1][j] == 2 and self.gameBoard[2][j] == 2 and
                    self.gameBoard[3][j] == 2 and self.gameBoard[4][j] == 2):
                self.Player2Score += 1
            if (self.gameBoard[2][j] == 2 and self.gameBoard[3][j] == 2 and
                    self.gameBoard[4][j] == 2 and self.gameBoard[5][j] == 2):
                self.Player2Score += 1
              
        