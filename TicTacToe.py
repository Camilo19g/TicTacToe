import tkinter as tk
import math


class TicTacToe:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic Tac Toe")

        self.player_choice = None

        self.player1_button = tk.Button(
            self.master, text="Player X", command=lambda: self.choose_player("X"), width=8)
        self.player1_button.grid(row=4, column=0, padx=0, pady=0)

        self.player2_button = tk.Button(
            self.master, text="Player O", command=lambda: self.choose_player("O"), width=8)
        self.player2_button.grid(row=4, column=2, padx=0, pady=0)

        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.buttons = []
        for i in range(3):
            row = []
            for j in range(3):
                button = tk.Button(
                    self.master, text="", width=10, height=4, command=lambda i=i, j=j: self.play(i, j))
                button.grid(row=i, column=j, padx=0, pady=0)
                button.configure(state="disabled")
                row.append(button)
            self.buttons.append(row)

        self.status = tk.Label(
            self.master, text="Please choose a player", font=("Helvetica", 16))
        self.status.grid(row=3, columnspan=3)

    def choose_player(self, player):
        self.player_choice = player
        if self.player_choice == 'X':
            self.player = "X"
            self.computer = "O"
            self.computer_turn = False
        else:
            self.player = "O"
            self.computer = "X"
            self.computer_turn = True

        self.player1_button.config(state='disabled')
        self.player2_button.config(state='disabled')

        self.status.config(text="Turn: " + self.player)

        for row in self.buttons:
            for button in row:
                button.configure(state="normal")

        if self.computer_turn:
            self.computer_play()

    def play(self, i, j):
        if self.board[i][j] == " ":
            self.board[i][j] = self.player
            self.buttons[i][j].config(text=self.player)
            winner = self.check_win()
            if winner:
                self.status.config(text=winner + " wins!")
                self.disable_buttons()
            else:
                self.computer_play()
                winner = self.check_win()
                if winner:
                    self.status.config(text=winner + " wins!")
                    self.disable_buttons()
                elif all([cell != " " for row in self.board for cell in row]):
                    self.status.config(text="Tie")
                    self.disable_buttons()
                else:
                    self.status.config(text="Turn: " + self.player)

    def computer_play(self):
        i, j = self.get_best_move()
        self.board[i][j] = self.computer
        self.buttons[i][j].config(text=self.computer)

    def get_best_move(self):
        best_score = -math.inf
        best_move = None
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == " ":
                    self.board[i][j] = self.computer
                    score = self.min_max(0, False)
                    self.board[i][j] = " "
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        return best_move

    def min_max(self, depth, is_maximizing):
        winner = self.check_win()
        if winner == self.computer:
            return 1
        elif winner == self.player:
            return -1
        elif winner == "Tie":
            return 0

        if is_maximizing:
            best_score = -math.inf
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == " ":
                        self.board[i][j] = self.computer
                        score = self.min_max(depth + 1, False)
                        self.board[i][j] = " "
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = math.inf
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == " ":
                        self.board[i][j] = self.player
                        score = self.min_max(depth + 1, True)
                        self.board[i][j] = " "
                        best_score = min(score, best_score)
            return best_score

    def check_win(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != " ":
                return self.board[i][0]
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != " ":
                return self.board[0][i]
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != " ":
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != " ":
            return self.board[0][2]
        if all([cell != " " for row in self.board for cell in row]):
            return "Tie"
        return None

    def disable_buttons(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    tictactoe = TicTacToe(root)
    root.mainloop()
