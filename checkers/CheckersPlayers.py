import numpy as np


class RandomPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        a = np.random.randint(self.game.getActionSize())
        valids = self.game.getValidMoves(board, 1)
        while valids[a]!=1:
            a = np.random.randint(self.game.getActionSize())
        return a


class HumanCheckersPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        # display(board)
        print(self.game.getLegalMoves(board))
        print("Enter your starting piece (row, column)")
        
        while True:
            a = input()
            y,x = [int(x) for x in a.split(' ')]
            a = 1+self.game.coordToPos(a)
            print("Enter your destination (row, column)")
            b = input()
            y,x = [int(x) for x in a.split(' ')]
            if valid[a]:
                break
            else:
                print('Invalid')
        

        return a

