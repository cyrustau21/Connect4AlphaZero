from tkinter import *
from tkinter import font
import numpy as np
from connect4_Hawk.Connect4Game import Connect4Game
from connect4_Hawk.Connect4Logic import Board
from connect4_Hawk.NNet_Pytorch import NNetWrapper as NNet
from MCTS import MCTS
from utils import *

class Info(Frame):
    def __init__(self, master=None):
        Frame.__init__(self)
        self.configure(width=500, height=100)
        police = font.Font(self, size=20, family='Arial')
        self.t = Label(self, text="Look at console!", font=police)
        self.t.grid(sticky=NSEW, pady=20)

class Piece(object):
    def __init__(self, x, y, can, color="white", bg="red"):
        self.can = can
        self.x = x
        self.y = y
        self.color = color

        self.turn = 1
        
        self.r = 30
        self.piece = self.can.create_oval(self.x+10,self.y+10,self.x+61,self.y+61,fill=color,outline="blue")
        
        

    def changeColor(self, color):
        self.can.itemconfigure(self.piece, fill=color)
        self.color = color

class Game(Canvas):
    def __init__(self, master=None):
        Canvas.__init__(self)
        self.configure(width=500, height=400, bg="blue")
        self.game = Connect4Game(6,7)
        self.player = 1
        self.humanPlayer = 0
        while not self.humanPlayer == 1 and not self.humanPlayer == 2:
            print("Should the human go first or second? Enter 1 or 2")
            self.humanPlayer = int(input())
        if self.humanPlayer == 1:
            self.ai_player = 2
        else:
            self.ai_player = 1
        self.setPlayer()
        self.board = np.zeros((6,7))
        self.color = "yellow"
        self.p = []
        self.perm = True
        n1 = NNet(self.game)
        n1.load_checkpoint('./checkpoint','best.pth.tar')
        args1 = dotdict({'numMCTSSims': 50, 'cpuct':1.0})
        mcts1 = MCTS(self.game, n1, args1)
        self.n1p = lambda x: np.argmax(mcts1.getActionProb(x, temp=0))
        # n2 = NNet(self.game)
        # n2.load_checkpoint('./checkpoints','best.pth.tar')
        # args2 = dotdict({'numMCTSSims': 50, 'cpuct':1.0})
        # mcts2 = MCTS(self.game, n2, args2)
        # self.n2p = lambda x: np.argmax(mcts2.getActionProb(x, temp=0))
        if self.ai_player == 2:
            self.ai_ind = -1
        else:
            self.ai_ind = 1
        for i in range(0, 340, int(400/6)):
            liste_rangee = []
            for j in range(0, 440, int(500/7)):
                liste_rangee.append(Piece(j, i ,self))
                
            self.p.append(liste_rangee)
        self.bind("<Button-1>", self.detCol)

    def detCol(self, event):
        if self.perm:
            #print("Called")
            if self.player == self.humanPlayer:
                col = int(event.x/71)
                #print(col)
            else:
                #print(str(list(self.board)))
                col = self.n1p(self.game.getCanonicalForm(self.board,1 ))
            b = Board(6,7)
            b.pieces = np.copy(self.board)
            r = b.findFirstUnoccupied(col)
            if self.player == 2:
                self.player = -1
            new = self.game.getNextState(self.board,self.player,col)
            if self.player == -1:
                self.player = 2
            self.board = new[0]
            #print(str(r)+" "+str(col))
            if r == -1:
                info.t.config(text="Choose a valid column")
                return
            else:
                self.p[r][col].changeColor(self.color)

            
            
            if self.player == 1:
                self.player = 2
                self.setPlayer()
                self.color = "red"

            elif self.player == 2:
                self.player = 1
                self.setPlayer()
                self.color = "yellow"
            print(str(self.board))
            result = self.game.getGameEnded(self.board,self.humanPlayer)
            if result == 1:
                info.t.config(text="Human wins")
                self.perm = False
            elif result == -1:
                info.t.config(text="AI wins")
                self.perm = False
            elif result == -.5:
                info.t.config(text="Tie")
                self.perm = False

    def setPlayer(self):
        if self.player == self.ai_player:
            info.t.config(text="AI's turn")
        else:
           info.t.config(text="Human's turn") 
    


root = Tk()
root.geometry("550x550")
root.title("Connect 4 with Alpha4 AI -- Big AI Group")

info = Info(root)
info.grid(row=0, column=0)


t = Game(root)
t.grid(row=1, column=0)
human = 1
def rein():
    global info
    info.t.config(text="")
    
    info = Info(root)
    info.grid(row=0, column=0)
    t = Game(root)
    t.grid(row=1, column=0)

Button(root, text="Restart", command=rein).grid(row=2, column=0, pady=30)

root.mainloop()

