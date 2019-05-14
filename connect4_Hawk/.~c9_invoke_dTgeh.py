'''
Author: Eric P. Nichols
Date: Feb 8, 2008.
Board class.
Board data:
  1=white, -1=black, 0=empty
  first dim is column , 2nd is row:
     pieces[1][7] is the square in column 2,
     at the opposite end of the board in row 8.
Squares are stored and manipulated as (x,y) tuples.
x is the column, y is the row.
'''
import numpy as np
class Board():

    # list of all 8 directions on the board, as (x,y) offsets
    __directions = [(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(0,1)]

    def __init__(self, r, c):
        "Set up initial board configuration."

        self.r = r
        self.c = c
        self.lastMoveW = (-1,-1)
        self.lastMoveB = (-1,-1)
        # Create the empty board array.
        self.pieces = np.zeros((r,c))
        #print(self.pieces)

    # add [][] indexer syntax to the Board
    def __getitem__(self, index): 
        return self.pieces[index]

    def countDiff(self, color):
        """Counts the # pieces more of the given color
        (1 for white, -1 for black, 0 for empty spaces)"""
        count = 0
        for y in range(self.r):
            for x in range(self.c):
                if self[x][y]==color:
                    count += 1
                if self[x][y]==-color:
                    count -= 1
        return count
    
    def findFirstUnoccupied(self,x):
        #increment loop and return column value wh
        #print(self[5][6])
        for y in range(self.r-1,-1,-1):
            if self[x][y] == 0.0:
                return y
        return -1

    def get_legal_moves(self, color):
        """Returns all the legal moves for the given color.
        (1 for white, -1 for black
        """
        moves = set()  # stores the legal moves.

        # Get all the squares with pieces of the given color.
        for x in range(0,self.c-1,1):
            #print(x)
            y = self.findFirstUnoccupied(x)
            if y != -1:
                # print("returned")
                # print(x)
                # print(y)
                moves.add((y,x))
        return moves

    def has_legal_moves(self, color):
        if len(self.get_legal_moves(color)) != 0:
            return True
        else:
            return False


    def execute_move(self, move, color):
        """Perform the given move on the board; flips pieces as necessary.
        color gives the color pf the piece to play (1=white,-1=black)
        """
        
        # Add the piece to the empty square.
        print(move)
        move_y = move[0]
        move_x = move[1]
        
        self[move_y][move_x] = color
        
        if color == 1:
            lastMoveW = move
        else:
            lastMoveB = move
        
    # def isValid(self, x, y):
    #     for d in self.__directions:
    #         dx = d[0]
    #         dy = d[1]
    #         if (dx+x) < 0:
    #             return False
    #         elif dx+x >= self.c:
    #             return False
    #         if dy+y < 0:
    #             return False
    #         elif dy+y >= self.r:
    #             return False
    #     return True
    
    def isValid(self, x, y):
        if x < 0:
            return False
        elif x >= self.c:
            return False
        if y < 0:
            return False
        elif y >= self.r:
            return False
        return True
        
    def getNumInARow(self, color):
        greatest = 1
        x = self.getLastMove(color)[0]
        y = self.getLastMove(color)[1]
        for d in self.__directions:
            dx = d[0]
            dy = d[1]
            if self.isValid(dx+x,dy+y) and (self[dx+x,dy+y] == color):
                temp = self.getNumSameD(dx+x,dy+y,dx,dy,color)
                if temp > greatest:
                    greatest = temp
                    
        return greatest
                
                
    def getNumSameD(self, x, y, dx, dy, color):
        count = 2
        while self.isValid(dx+x,dy+y) and self[dx+x][dy+y] == color:
            count +=1
            x = dx+x
            y = dy+y
        return count
        
    def getLastMove(self, color):
        if color == 1:
            return self.lastMoveW
        else:
            return self.lastMoveB
            
    def getR(self):
        return self.r
    def getC(self):
        return self.c
        

    @staticmethod
    def _increment_move(move, direction, n):
        # print(move)
        """ Generator expression for incrementing moves """
        move = list(map(sum, zip(move, direction)))
        #move = (move[0]+direction[0], move[1]+direction[1])
        while all(map(lambda x: 0 <= x < n, move)): 
        #while 0<=move[0] and move[0]<n and 0<=move[1] and move[1]<n:
            yield move
            move=list(map(sum,zip(move,direction)))
            #move = (move[0]+direction[0],move[1]+direction[1])

