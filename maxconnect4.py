import csv #import csv package for creating the depth level file
import sys  #importing sys for accessing command line arguments
from MaxConnect4Game import MaxConnect4game     #importing maxconnect4game(which is the user defined package)    


def Play_Human(gameBoard):       # function to take input from the player i.e human
    while gameBoard.get_piece_count() != 42:  #this is to checking the board is empty or full
        print(" Human's turn") 
        print(" ------- ----")
        User_Moves = int(input("Enter a column number (1-7): "))  # taking cloumn number from the player
        if not 0 < User_Moves < 8:    # checking the column number given by the user
            print("Column invalid! Enter Again.")
            continue
        if not gameBoard.play_piece(User_Moves - 1):
            print("Column number: %d is full. Try other column." % User_Moves)
            continue
        print("Your made move: " + str(User_Moves))
        gameBoard.display_gameBoard()   # displaying the game board
        gameBoard.game_File = open("human.txt", 'w')  # writing the game board in a text file 
        gameBoard.print_gameBoard_file()
        gameBoard.game_File.close()  # closing the file
        if gameBoard.get_piece_count() == 42:     # this is to checking the board if it is full or not
            print("No more moves possible, Game Over!")
            gameBoard.score_Count()  # this is to displaying the score of the players
            print('Score: PlayerA = %d, PlayerB = %d\n' % (gameBoard.Player1Score, gameBoard.Player2Score))
            break
        else:   # if human is not the player(that is computer is the player)
            print("Computer is conputing based on next " + str(gameBoard.d) + " steps...")
            gameBoard.change_Move()  # transferring the game to other player
            gameBoard.ai_Play()  # computing the computer move by using minmax alpha beta purning
            gameBoard.display_gameBoard()   # presenting the game board
            gameBoard.game_File = open('computer.txt', 'w')  # printing output to file
            gameBoard.print_gameBoard_file()
            gameBoard.game_File.close()  # file closing
            gameBoard.score_Count()  # this is to print the score of both players
            print('Score: PlayerA = %d, PlayerB = %d\n' % (gameBoard.Player1Score, gameBoard.Player2Score))


def one_move_mode(gameBoard):     # this is the function for one move mode
    if gameBoard.piece_Count >= 42:  # if all the places in the board are filled then exit
        print('Game board is full !\n Game Over...')
        sys.exit(0)
    print ('GameBoard state before move:')
    gameBoard.display_gameBoard()   # printing the  game board
    gameBoard.ai_Play()      # Calculating  the computer move
    print ('GameBoard state after move:')
    gameBoard.display_GameBoard()   # printing the  game board
    gameBoard.score_Count()  # displaying score
    print('Score: PlayerA = %d, PlayerB = %d\n' % (gameBoard.Player1Score, gameBoard.Player2Score))
    gameBoard.print_gameBoard_file()    # printing the game board into file
    gameBoard.game_File.close()      # close file


def interactive_mode(gameBoard, next_Player):     #This Game Board in interactive mode
    print('Current Board state')
    gameBoard.display_gameBoard()   # presenting the game board
    gameBoard.score_Count()  # printing the score
    print('Score: PlayerA = %d, PlayerB = %d\n' % (gameBoard.Player1Score, gameBoard.Player2Score))
    if next_Player == 'human-next':  # checking the next player move from the command line argument
        Play_Human(gameBoard)    # human function 
    else:
        gameBoard.ai_Play()  # computing the computer move
        gameBoard.game_File = open('computer.txt', 'w')  # printing the result into the file
        gameBoard.print_gameBoard_file()
        gameBoard.game_File.close()  # closing the file
        gameBoard.display_gameBoard()   # dislaying the game board
        gameBoard.score_Count()  # displaying the score 
        print('Score: PlayerA = %d, PlayerB = %d\n' % (gameBoard.Player1Score, gameBoard.Player2Score))
        Play_Human(gameBoard)    # human turn

    if gameBoard.get_piece_count() == 42: #After game board is full, printing the final result
        if gameBoard.Player1Score > gameBoard.Player2Score:
            print("Player 1 wins")
        if gameBoard.Player1Score == gameBoard.Player2Score:
            print("The game is a Tie")
        if gameBoard.Player1Score < gameBoard.Player2Score:
            print("Player 2 wins")
        print("Game Over")



def main(argv): 
    gameBoard = MaxConnect4game()   #object of other file
    try:
        gameBoard.game_File = open(argv[2], 'r')     #this step is for reading the input file
        fileLines = gameBoard.game_File.readlines()
        gameBoard.gameBoard = [[int(char) for char in line[0:7]] for line in fileLines[0:-1]]
        gameBoard.current_Move = int(fileLines[-1][0])
        gameBoard.game_File.close()
    except:
        print('File not found, begin new game.')
        gameBoard.current_Move = 1
    gameBoard.check_piece_count()     # checking all the elements added is whether true or not
    gameBoard.d = argv[4]   # depth taken from argv
    if argv[1] == 'one-move':   #for one move mode
        try:
            gameBoard.game_File = open(argv[3], 'w')
        except:
            sys.exit('Error while opening output file.')
        one_move_mode(gameBoard)
    else:   # this step is for interactive mode
        interactive_mode(gameBoard, argv[3])


main(sys.argv)

