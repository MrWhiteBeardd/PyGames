import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe by Karim")
        self.board = [" " for _ in range(9)]
        self.current_player = "X"
        self.buttons = []
        self.ai_enabled = False
        self.difficulty = "easy"
        self.losing_moves = set()
        self.create_menu()
        self.create_main_frame()
        self.show_options()  # Show options at the start

    def create_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)
        options_menu = tk.Menu(menu)
        menu.add_cascade(label="Options", menu=options_menu)
        options_menu.add_command(label="Show Options", command=self.show_options)

    def create_main_frame(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

    def show_options(self):
        for widget in self.main_frame.winfo_children():
            widget.pack_forget()

        options_frame = tk.Frame(self.main_frame)
        options_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(options_frame, text="Choose Game Mode:").pack(pady=10)

        tk.Button(options_frame, text="Play against Player", command=lambda: self.start_game(False, "easy")).pack(pady=5)
        tk.Button(options_frame, text="Play against AI (Easy)", command=lambda: self.start_game(True, "easy")).pack(pady=5)
        tk.Button(options_frame, text="Play against AI (Hard)", command=lambda: self.start_game(True, "hard")).pack(pady=5)

    def start_game(self, ai_enabled, difficulty):
        self.ai_enabled = ai_enabled
        self.difficulty = difficulty
        self.reset_board()
        self.show_board()

    def show_board(self):
        for widget in self.main_frame.winfo_children():
            widget.pack_forget()

        board_frame = tk.Frame(self.main_frame)
        board_frame.pack(fill=tk.BOTH, expand=True)

        for i in range(9):
            button = tk.Button(board_frame, text=" ", font=('normal', 40), width=5, height=2,
                               command=lambda i=i: self.on_button_click(i))
            button.grid(row=i//3, column=i%3)
            self.buttons.append(button)

    def on_button_click(self, index):
        if self.board[index] == " ":
            self.board[index] = self.current_player
            self.buttons[index].config(text=self.current_player)
            if self.check_winner():
                if self.current_player == "X" and self.ai_enabled:
                    self.losing_moves.add(tuple(self.board))
                messagebox.showinfo("Tic Tac Toe", f"Player {self.current_player} wins!")
                self.show_replay_options()
            elif " " not in self.board:
                messagebox.showinfo("Tic Tac Toe", "It's a tie!")
                self.show_replay_options()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                if self.ai_enabled and self.current_player == "O":
                    self.ai_move()

    def ai_move(self):
        if self.difficulty == "easy":
            available_moves = [i for i, x in enumerate(self.board) if x == " "]
            move = random.choice(available_moves)
        else:
            move = self.find_best_move()
        self.on_button_click(move)

    def find_best_move(self):
        best_score = float('-inf')
        best_move = None
        for i in range(9):
            if self.board[i] == " ":
                self.board[i] = "O"
                score = self.minimax(self.board, 0, False)
                self.board[i] = " "
                if score > best_score and tuple(self.board) not in self.losing_moves:
                    best_score = score
                    best_move = i
        return best_move

    def minimax(self, board, depth, is_maximizing):
        if self.check_winner():
            return 1 if self.current_player == "O" else -1
        elif " " not in board:
            return 0

        if is_maximizing:
            best_score = float('-inf')
            for i in range(9):
                if board[i] == " ":
                    board[i] = "O"
                    score = self.minimax(board, depth + 1, False)
                    board[i] = " "
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if board[i] == " ":
                    board[i] = "X"
                    score = self.minimax(board, depth + 1, True)
                    board[i] = " "
                    best_score = min(score, best_score)
            return best_score

    def check_winner(self):
        winning_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        ]
        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != " ":
                return True
        return False

    def reset_board(self):
        self.board = [" " for _ in range(9)]
        self.current_player = "X"
        for button in self.buttons:
            button.config(text=" ", state=tk.NORMAL)
        self.buttons.clear()

    def show_replay_options(self):
        replay = messagebox.askyesno("Tic Tac Toe", "Do you want to play again?")
        if replay:
            self.reset_board()
            self.show_board()
        else:
            self.show_options()

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()