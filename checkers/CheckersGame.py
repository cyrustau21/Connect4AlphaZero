from .game import Game
from .CheckersLogic import Board
class CheckersGame():
    """
    This class specifies the base Game class. To define your own game, subclass
    this class and implement the functions below. This works when the game is
    two-player, adversarial and turn-based.

    Use 1 for player1 and -1 for player2.

    See othello/OthelloGame.py for an example implementation.
    """
    def __init__(self):
        self.b = Board(8)

    def getInitBoard(self):
        """
        Returns:
            startBoard: a representation of the board (ideally this is the form
                        that will be the input to your neural network)
        """
        self.b.updateBoard()
        return self.b.getBoard()


    def getBoardSize(self):
        """
        Returns:
            (x,y): a tuple of board dimensions
        """
        return self.b.getSize()

    def getActionSize(self):
        """
        Returns:
            actionSize: number of all possible actions
        """
        return 32*31

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
        move = self.actionToMove(action)
        board.executeMove(move)
        board.updateBoard()
        return board.getBoard(),board.curPlayer()

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
        valids = [0]*self.getActionSize
        moves = board.getLegalMoves()
        for move in moves:
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
        return board.getWinner(player)


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
        board.updateBoard()
        b = board.getBoard()
        if player == -1:
            for i in b:
                b[i] = -1*b[i]
        return b

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
        return board.toString()

    def display(self,board):
        #print(board.shape)
        n = board.shape[0]
        board.updateBoard()
        pieces = board.getBoard()
        print("   ",end="")
        for y in range(n):
            print (y,"|",end="")
        print("")
        print(" -----------------------")
        for y in range(n):
            print(y, "|",end="")    # print the row #
            for x in range(n):
                if y%2==0:
                    if x%2 ==1:
                        if x == n: print("-",end="")
                        elif pieces[self.coordToPos((y,x))] == -1: 
                            print("R  ",end="")
                        elif pieces[self.coordToPos((y,x))] == 1: 
                            print("B  ",end="")
                        elif pieces[self.coordToPos((y,x))] == -2:
                            print("RK  ",end="")
                        elif pieces[self.coordToPos((y,x))] == 2: 
                            print("BK  ",end="")
                        else: 
                            print("-  ",end="")
                elif x==n:
                    print("-",end="")
                else:
                    print("-  ",end="")
                if y%2==1:
                    if x%2 ==0:
                        if x == n: print("-",end="")
                        elif pieces[self.coordToPos((y,x))] == -1: 
                            print("R  ",end="")
                        elif pieces[self.coordToPos((y,x))] == 1: 
                            print("B  ",end="")
                        elif pieces[self.coordToPos((y,x))] == -2:
                            print("RK  ",end="")
                        elif pieces[self.coordToPos((y,x))] == 2: 
                            print("BK  ",end="")
                        else: 
                            print("-  ",end="")
                    elif x==n:
                        print("-",end="")
                    else:
                        print("-  ",end="")
                print("|")

        print("   -----------------------")

    def getLegalMoves(self,board):
        board.updateBoard()
        moves = board.getLegalMoves()
        coords = []
        for move in moves:
            coords.append(self.moveToCoords(move))
        return coords

    def moveToAction(self, move):
        return (move[0]-1)*32+(move[1]-1)
    def actionToMove(self,action):
        start = action%32+1
        end = action - 32*(start-1) + 1
        return (start,end)
    def coordToPos(self, coord):
        r = coord[0]
        c = coord[1]
        if c%2==1:
            c -=1
        return r*4+c
    def posToCoord(self, pos):
        r = pos%4
        c = pos - pos%4
        return (r,c)
    def moveToCoords(self,move):
        start = move[1]
        end = move[1]
        return (self.posToCoord(start),self.posToCoord(end))


