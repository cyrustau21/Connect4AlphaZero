'''

'''
import numpy as np
from checkers import Game 

class Board():

    # list of all 8 directions on the board, as (x,y) offsets
    __directions = [(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(0,1)]

    def __init__(self,n):
        "Set up initial board configuration."

        self.n = n
        self.game = Game()
        self.pieces = np.zeros((self.n,self.n))
        self.size = n*n/2
        self.board = [0]*self.size


    # add [][] indexer syntax to the Board
    def __getitem__(self, index): 
        return self.pieces[index]

    def updateBoard(self):
        self.board = [0]*self.size
        for piece in game.board.pieces:
            board[]

