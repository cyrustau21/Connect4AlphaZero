'''

'''
import numpy as np
from .game import Game

class Board():

    # list of all 8 directions on the board, as (x,y) offsets
    __directions = [(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(0,1)]

    def __init__(self,n):
        "Set up initial board configuration."

        self.n = n
        self.game = Game()
        self.pieces = np.zeros((self.n,self.n))
        self.size = int(n*n/2)
        self.board = [0]*self.size
        self.king = 2
        self.updateBoard()


    # add [][] indexer syntax to the Board
    def __getitem__(self, index): 
        return self.pieces[index]

    def executeMove(self, move):
        self.getLegalMoves()
        #print(move)
        self.game.move(move)

    def updateBoard(self):
        self.board = [0]*self.size
        player = self.game.whose_turn()
        p = self.game.whose_turn()
        if p == 2:
            p = -1
        for piece in self.game.board.pieces:
            if not piece.captured:
                if piece.king and player==1:
                    char = self.king
                elif piece.king:
                    char = -1*self.king
                elif piece.player == player:
                    char = p
                else:
                    char = -1*p
                self.board[piece.position-1] = char

    def getSize(self):
        return self.n*self.n//2

    def getWinner(self,player):
        p = player
        if p == -1:
            p = 2
        if p == 1:
            notP = 2
        else:
            notP = 1
        if not self.game.is_over():
            return 0
        elif self.game.get_winner() == p:
            return 1
        elif self.game.get_winner == notP:
            return -1
        else:
            return 1e-4

    def getBoard(self):
        self.updateBoard()
        b = np.zeros((8,8))
        for i in range(len(self.board)):
            if not self.board[i] == 0:
                coord = self.posToCoord(i)
                b[coord[0]][coord[1]] = self.board[i]
        return b
    def curPlayer(self):
        return self.game.whose_turn()
    def getLegalMoves(self):
        print(self.game.get_possible_moves())
        return self.game.get_possible_moves()

    def posToCoord(self, pos):
        r = int(pos/4)
        if r%2==0:
            c = 2*(pos%4)+1
        else:
            c = 2*(pos%4)
        return (r,c)


