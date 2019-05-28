from .CheckersLogic import Board
import numpy as np
class CheckersGame():
    """
    This class specifies the base Game class. To define your own game, subclass
    this class and implement the functions below. This works when the game is
    two-player, adversarial and turn-based.

    Use 1 for player1 and -1 for player2.

    See othello/OthelloGame.py for an example implementation.
    """
    def __init__(self,n):
        self.b = Board(n)
        self.n = n
        self.startingBoard = [1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]

    def getInitBoard(self):
        """
        Returns:
            startBoard: a representation of the board (ideally this is the form
                        that will be the input to your neural network)
        """
        b = np.zeros((8,8))
        for i in range(len(self.startingBoard)):
            if not self.startingBoard[i] == 0:
                coord = self.posToCoord(i)
                #print(coord)
                b[coord[0]][coord[1]] = self.startingBoard[i]
        return b


    def getBoardSize(self):
        """
        Returns:
            (x,y): a tuple of board dimensions
        """
        return self.n

    def getActionSize(self):
        """
        Returns:
            actionSize: number of all possible actions
        """
        return 32*32

    def getNextState(self, board, player, action):
        """
        Input:
            board: current board
            player: current player (1 or -1)
            action: action taken by current player

        Returns:
            nextBoard: board after applying action
            nextPlayer: player who plays in the next turn (should be -player)
        """
        if player == -1:
            player == 2
        self.b.boardToGame(board,player)
        move = self.actionToMove(action)
        self.b.executeMove(move)
        return self.b.getBoard(),self.b.curPlayer()


    def getValidMoves(self, board, player):
        """
        Input:
            board: current board
            player: current player

        Returns:
            validMoves: a binary vector of length self.getActionSize(), 1 for
                        moves that are valid from the current board and player,
                        0 for invalid moves
        """
        #print("Current player for board is:"+str(self.curPlayer()))
        #print("Current player given is:"+str(player))
        #print(str(self.b.getBoard()))
        if player == -1:
            player = 2
        self.b.boardToGame(board,player)
        valids = [0]*self.getActionSize()
        moves = self.b.getLegalMoves()
        print(str(moves))
        for move in moves:
            #print(move)
            valids[self.moveToAction(move)] = 1

        return valids

    def getGameEnded(self, board, player):
        """
        Input:
            board: current board
            player: current player (1 or -1)

        Returns:
            r: 0 if game has not ended. 1 if player won, -1 if player lost,
               small non-zero value for draw.
               
        """
        self.b.boardToGame(board,player)
        return self.b.getWinner(player)


    def getCanonicalForm(self, board, player):
        """
        Input:
            board: current board
            player: current player (1 or -1)

        Returns:
            canonicalBoard: returns canonical form of board. The canonical form
                            should be independent of player. For e.g. in chess,
                            the canonical form can be chosen to be from the pov
                            of white. When the player is white, we can return
                            board as is. When the player is black, we can invert
                            the colors and return the board.
        """
        print(board)
        if player == -1:
            board = np.asarray(board)
            board = np.flipud(board)
            board = np.fliplr(board)
            return list(board)
        else:        
            return board





    def getSymmetries(self, board, pi):
        """
        Input:
            board: current board
            pi: policy vector of size self.getActionSize()

        Returns:
            symmForms: a list of [(board,pi)] where each tuple is a symmetrical
                       form of the board and the corresponding pi vector. This
                       is used when training the neural network from examples.
        """
        return [(board,pi)]

    def stringRepresentation(self, board):
        """
        Input:
            board: current board

        Returns:
            boardString: a quick conversion of board to a string format.
                         Required by MCTS for hashing.
        """
        return str(board)


    def moveToAction(self, move):
        return (move[0]-1)*32+(move[1]-1)
    def actionToMove(self,action):
        start = int(action/32)
        end = action - 32*(start)
        start+=1
        end+=1
        return [start,end]
    def coordToPos(self, coord):
        r = coord[0]
        c = coord[1]
        if not c==0:
            c = int(c/2)

        return r*4+c
    def posToCoord(self, pos):
        r = int(pos/4)
        if r%2==0:
            c = 2*(pos%4)+1
        else:
            c = 2*(pos%4)
        return (r,c)
    def moveToCoords(self,move):
        start = move[0]
        end = move[1]
        return (self.posToCoord(start),self.posToCoord(end))

    def curPlayer(self):
        return self.b.curPlayer()



        

def display(board):
    n = 8
    king = 2
    for y in range(n):
        print (y,"|",end="")
    print("")
    print(" -----------------------")
    for y in range(n):
        print(y, "|",end="")    # print the row #
        for x in range(n):
            piece = board[y][x]
            if piece == -1: print("R ",end="")
            elif piece == 1: print("B ",end="")
            elif piece == -1*king: print("RK",end="")
            elif piece == king: print("BK",end="")
            else:
                if x==n:
                    print("-",end="")
                else:
                    print("- ",end="")
        print("|")

    print("   -----------------------")


