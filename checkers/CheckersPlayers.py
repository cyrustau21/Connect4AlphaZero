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
        valids = self.game.getValidMoves(board,self.game.curPlayer())
        while True:
            print("Enter your starting piece (row, column)")
            a = input()
            y,x = [int(x) for x in a.split(' ')]
            start = 1+self.game.coordToPos((y,x))
            print("Enter your destination (row, column)")
            b = input()
            y,x = [int(x) for x in b.split(' ')]
            end = 1+self.game.coordToPos((y,x))
            action = self.game.moveToAction((start,end))
            if valids[action]:
                break
            else:
                print('Invalid')
        

        return action

