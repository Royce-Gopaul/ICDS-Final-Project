#Tic-Tac-Toe Game
#Susan Wang
#ICDS Project

#Note: referenced https://youtu.be/V9MbQ2Xl4CE?si=q0t2VwgGzyCiInIj

from tkinter import *

CHAT_IP = '127.0.0.1'
# CHAT_IP = socket.gethostbyname(socket.gethostname())

CHAT_PORT = 1112
SERVER = (CHAT_IP, CHAT_PORT)

class Game:

    def __init__(self):
        self._score = 0
        self._players = ["O","X"]
        self._turn = self._players[0]


        self.window = Tk()
        self.window.title("Tic-Tac-Toe")

        self._board = [[0,0,0],
                [0,0,0],
                [0,0,0]]
        
        self.label = Label(text=self._turn + " turn", font=('Times',40))
        self.label.pack(side="top")

        frame = Frame(self.window)
        frame.pack()

        for row in range(3):
            for column in range(3):
                self._board[row][column] = Button(frame, text="",font=('Times',40), width=5, height=2,
                command= lambda row=row, column=column: self.play(row,column))
                self._board[row][column].grid(row=row,column=column)

        restart = Button(text="restart", font=('Times', 20), command=self.restart)
        restart.pack(side="top")

        #score = 1,-1,0

    def evaluate(self):
        #Evaluates the board situation (if anyone won)
        #1= WIN
        #-1 = OPPONENT WIN
        #0 = NO WIN

        for player in self._players:
            # Check rows and columns
            for i in range(3):
                if (self._board[i][0]['text'] == self._board[i][1]['text'] == self._board[i][2]['text'] == player) or \
                   (self._board[0][i]['text'] == self._board[1][i]['text'] == self._board[2][i]['text'] == player):
                    return 1 if player == self._turn else -1

            # Check diagonals
            if (self._board[0][0]['text'] == self._board[1][1]['text'] == self._board[2][2]['text'] == player) or \
               (self._board[0][2]['text'] == self._board[1][1]['text'] == self._board[2][0]['text'] == player):
                return 1 if player == self._turn else -1

        # No winner found
        return 0
    

    def full(self):
        #Checks if board is full

        for x in range(3):
            for y in range(3):
                if self._board[x][y]['text'] == "":
                    return False

        return True
    
    def play(self,row,column):
        if self._board[row][column]['text'] == "" and self.evaluate() == 0:
            # Update the button text
            self._board[row][column]['text'] = self._turn

            # Check for a win
            result = self.evaluate()
            if result == 1:
                self.label.config(text=self._turn + " wins!")
            elif result == -1:
                self.label.config(text=self._players[1 - self._players.index(self._turn)] + " wins!")
            
            elif result == 0 and self.full():
                self.label.config(text="Tie!")
            else:
                # Switch turns
                self._turn = self._players[1 - self._players.index(self._turn)]
                self.label.config(text=self._turn + " turn")


    def restart(self):
        for x in range(3):
            for y in range(3):
                self._board[x][y]['text'] = ""

        for x in range(3):
            for y in range(3):
                self._board[x][y]['text'] = ""

        self._turn = self._players[0]
        self.label.config(text=self._turn + " turn")
    
    def run(self):

        self.window.mainloop()

if __name__ == "__main__":
    game = Game()
    game.run()
