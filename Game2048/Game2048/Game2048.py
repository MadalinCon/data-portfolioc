import tkinter as tk
from tkinter import messagebox
import random

GRID_SIZE = 4
CELL_SIZE = 100
CELL_PADDING = 10
WINDOW_PADDING = 20
BG_COLOR = '#faf8ef'
EMPTY_COLOR = '#cdc1b4'
TEXT_DARK = '#776e65'
TEXT_LIGHT = '#f9f6f2'

COLORS = {
    0: '#cdc1b4',
    2: '#eee4da',
    4: '#ede0c8',
    8: '#f2b179',
    16: '#f59563',
    32: '#f67c5f',
    64: '#f65e3b',
    128: '#edcf72',
    256: '#edcc61',
    512: '#edc850',
    1024: '#edc53f',
    2048: '#edc22e',
}


class Game2048:
    def __init__(self, root):
        self.root = root
        self.root.title('2048 - Python')
        self.root.resizable(False, False)
        self.root.configure(bg=BG_COLOR)

        self.score = 0
        self.best = 0
        self.board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]

        self.create_ui()
        self.bind_keys()
        self.start_new_game()

    def create_ui(self):
        top_frame = tk.Frame(self.root, bg=BG_COLOR)
        top_frame.pack(pady=(15, 5))

        title = tk.Label(
            top_frame,
            text='2048',
            font=('Arial', 28, 'bold'),
            bg=BG_COLOR,
            fg=TEXT_DARK
        )
        title.grid(row=0, column=0, padx=10)

        self.score_label = tk.Label(
            top_frame,
            text='Score\n0',
            font=('Arial', 12, 'bold'),
            bg='#bbada0',
            fg='white',
            width=8,
            height=2,
            relief='flat'
        )
        self.score_label.grid(row=0, column=1, padx=5)

        self.best_label = tk.Label(
            top_frame,
            text='Best\n0',
            font=('Arial', 12, 'bold'),
            bg='#bbada0',
            fg='white',
            width=8,
            height=2,
            relief='flat'
        )
        self.best_label.grid(row=0, column=2, padx=5)

        restart_button = tk.Button(
            self.root,
            text='Restart',
            font=('Arial', 11, 'bold'),
            bg='#8f7a66',
            fg='white',
            activebackground='#9c8672',
            activeforeground='white',
            command=self.start_new_game,
            padx=20,
            pady=8,
            bd=0,
            cursor='hand2'
        )
        restart_button.pack(pady=(5, 10))

        self.board_frame = tk.Frame(self.root, bg='#bbada0', padx=5, pady=5)
        self.board_frame.pack(padx=WINDOW_PADDING, pady=(0, 20))

        self.cells = []
        for i in range(GRID_SIZE):
            row = []
            for j in range(GRID_SIZE):
                frame = tk.Frame(
                    self.board_frame,
                    width=CELL_SIZE,
                    height=CELL_SIZE,
                    bg=EMPTY_COLOR
                )
                frame.grid(row=i, column=j, padx=CELL_PADDING // 2, pady=CELL_PADDING // 2)
                frame.grid_propagate(False)

                label = tk.Label(
                    frame,
                    text='',
                    font=('Arial', 24, 'bold'),
                    bg=EMPTY_COLOR,
                    fg=TEXT_DARK
                )
                label.place(relx=0.5, rely=0.5, anchor='center')
                row.append((frame, label))
            self.cells.append(row)

        instructions = tk.Label(
            self.root,
            text='Folosește săgețile de la tastatură pentru a muta piesele.',
            font=('Arial', 10),
            bg=BG_COLOR,
            fg=TEXT_DARK
        )
        instructions.pack(pady=(0, 15))

    def bind_keys(self):
        self.root.bind('<Up>', lambda event: self.handle_move('up'))
        self.root.bind('<Down>', lambda event: self.handle_move('down'))
        self.root.bind('<Left>', lambda event: self.handle_move('left'))
        self.root.bind('<Right>', lambda event: self.handle_move('right'))

    def start_new_game(self):
        self.score = 0
        self.board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.add_random_tile()
        self.add_random_tile()
        self.update_ui()

    def add_random_tile(self):
        empty = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if self.board[i][j] == 0]
        if not empty:
            return
        i, j = random.choice(empty)
        self.board[i][j] = 4 if random.random() < 0.1 else 2

    def update_ui(self):
        self.score_label.config(text=f'Score\n{self.score}')
        self.best = max(self.best, self.score)
        self.best_label.config(text=f'Best\n{self.best}')

        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                value = self.board[i][j]
                frame, label = self.cells[i][j]
                bg = COLORS.get(value, '#3c3a32')
                fg = TEXT_DARK if value in (0, 2, 4) else TEXT_LIGHT
                text = '' if value == 0 else str(value)
                font_size = 24
                if value >= 1024:
                    font_size = 18
                elif value >= 128:
                    font_size = 20

                frame.config(bg=bg)
                label.config(text=text, bg=bg, fg=fg, font=('Arial', font_size, 'bold'))

    def compress(self, row):
        new_row = [num for num in row if num != 0]
        new_row += [0] * (GRID_SIZE - len(new_row))
        return new_row

    def merge(self, row):
        for i in range(GRID_SIZE - 1):
            if row[i] != 0 and row[i] == row[i + 1]:
                row[i] *= 2
                self.score += row[i]
                row[i + 1] = 0
        return row

    def move_row_left(self, row):
        row = self.compress(row)
        row = self.merge(row)
        row = self.compress(row)
        return row

    def reverse(self, board):
        return [list(reversed(row)) for row in board]

    def transpose(self, board):
        return [list(row) for row in zip(*board)]

    def move_left(self):
        new_board = []
        changed = False
        for row in self.board:
            new_row = self.move_row_left(row[:])
            if new_row != row:
                changed = True
            new_board.append(new_row)
        self.board = new_board
        return changed

    def move_right(self):
        self.board = self.reverse(self.board)
        changed = self.move_left()
        self.board = self.reverse(self.board)
        return changed

    def move_up(self):
        self.board = self.transpose(self.board)
        changed = self.move_left()
        self.board = self.transpose(self.board)
        return changed

    def move_down(self):
        self.board = self.transpose(self.board)
        changed = self.move_right()
        self.board = self.transpose(self.board)
        return changed

    def handle_move(self, direction):
        old_board = [row[:] for row in self.board]

        if direction == 'left':
            changed = self.move_left()
        elif direction == 'right':
            changed = self.move_right()
        elif direction == 'up':
            changed = self.move_up()
        elif direction == 'down':
            changed = self.move_down()
        else:
            changed = False

        if changed:
            self.add_random_tile()
            self.update_ui()

            if self.check_win():
                messagebox.showinfo('Felicitări!', 'Ai ajuns la 2048!')
            elif self.check_game_over():
                messagebox.showinfo('Game Over', 'Nu mai există mutări posibile!')
        else:
            self.board = old_board

    def check_win(self):
        for row in self.board:
            if 2048 in row:
                return True
        return False

    def check_game_over(self):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.board[i][j] == 0:
                    return False
                if j < GRID_SIZE - 1 and self.board[i][j] == self.board[i][j + 1]:
                    return False
                if i < GRID_SIZE - 1 and self.board[i][j] == self.board[i + 1][j]:
                    return False
        return True


if __name__ == '__main__':
    root = tk.Tk()
    game = Game2048(root)
    root.mainloop()

