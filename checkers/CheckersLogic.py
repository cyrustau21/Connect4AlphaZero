'''

'''
import numpy as np
from .game import Game
from .piece import Piece

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


    # add [][] indexer syntax to the Board
    def __getitem__(self, index): 
        return self.pieces[index]

    def executeMove(self, move):
        self.game.move(move)

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
            return -.5

    def getBoard(self):
        b = np.zeros((8,8))
        for piece in self.game.board.pieces:
            if not piece.captured:
                player = piece.player
                if player == 2:
                    player = -1
                if piece.king:
                    char = player*self.king
                else:
                    char = player
                coord = self.posToCoord(piece.position-1)
                b[coord[0]][coord[1]] = char
        return b

    def boardToGame(self,board,curPlayer):
        self.game = Game()
        gameBoard = self.game.board
        pieces = self.boardToPieces(board)
        #print(str(pieces))
        ps = []
        for i in range(len(pieces)):
            if not pieces[i] == 0:
                if pieces[i]<0:
                    player = 2
                else:
                    player = 1
                if abs(pieces[i])==2:
                    king = True
                else:
                    king = False
                ps.append(self.createPiece(player,i+1,gameBoard,king))
        self.game.board.pieces = ps
        if curPlayer == -1:
            curPlayer = 2
        self.game.setPlayer(curPlayer)


    def curPlayer(self):
        player = self.game.whose_turn()
        if player == 2:
            player = -1
        return player
    def getLegalMoves(self):
        #print(self.game.get_possible_moves())
        return self.game.get_possible_moves()

    def posToCoord(self, pos):
        r = int(pos/4)
        if r%2==0:
            c = 2*(pos%4)+1
        else:
            c = 2*(pos%4)
        return (r,c)

    def boardToPieces(self, board):
        pieces = [0]*32
        i = 0
        for y in range(8):
            for x in range(8):
                if y%2==0:
                    if x%2==1:
                        pieces[i] = board[y][x]
                        i+=1
                else:
                    if x%2==0:
                        pieces[i] = board[y][x]
                        i+=1
        return pieces

    def createPiece(self,player,position,gameBoard,king):
        piece = Piece()
        piece.player = player
        piece.position = position
        piece.board = gameBoard
        piece.king = king
        return piece


