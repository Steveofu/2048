from tkinter import Frame, Label, CENTER
import random
import logic
import Define as Df


def gen():
    return random.randint(0, Df.GRID_LEN - 1)


class GameGrid(Frame):
    def __init__(self):
        Frame.__init__(self)

        self.grid()  # 创建窗口
        self.master.title('2048')
        self.master.bind("<Key>", self.key_down)
        # 定义一个字典对应的命令
        self.commands = {
            Df.KEY_UP: logic.up,
            Df.KEY_DOWN: logic.down,
            Df.KEY_LEFT: logic.left,
            Df.KEY_RIGHT: logic.right,
            Df.KEY_UP_ALT1: logic.up,
            Df.KEY_DOWN_ALT1: logic.down,
            Df.KEY_LEFT_ALT1: logic.left,
            Df.KEY_RIGHT_ALT1: logic.right,
            Df.KEY_UP_ALT2: logic.up,
            Df.KEY_DOWN_ALT2: logic.down,
            Df.KEY_LEFT_ALT2: logic.left,
            Df.KEY_RIGHT_ALT2: logic.right,
        }

        self.grid_cells = []
        self.init_grid()
        self.matrix = logic.new_game(Df.GRID_LEN)
        self.history_matrix = []
        self.update_grid_cells()

        self.mainloop()

    def init_grid(self):
        background = Frame(self, bg=Df.BACKGROUND_COLOR_GAME, width=Df.SIZE, height=Df.SIZE)
        background.grid()

        for i in range(Df.GRID_LEN):
            grid_row = []
            for j in range(Df.GRID_LEN):
                cell = Frame(
                    background,
                    bg=Df.BACKGROUND_COLOR_CELL_EMPTY,
                    width=Df.SIZE / Df.GRID_LEN,
                    height=Df.SIZE / Df.GRID_LEN
                )
                cell.grid(row=i, column=j, padx=Df.GRID_PADDING, pady=Df.GRID_PADDING)
                t = Label(master=cell, text="", bg=Df.BACKGROUND_COLOR_CELL_EMPTY, justify=CENTER, font=Df.FONT,
                          width=5, height=2)
                t.grid()
                grid_row.append(t)
            self.grid_cells.append(grid_row)

    def update_grid_cells(self):
        for i in range(Df.GRID_LEN):
            for j in range(Df.GRID_LEN):
                new_number = self.matrix[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(text="", bg=Df.BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(
                        text=str(new_number),
                        bg=Df.BACKGROUND_COLOR_DICT[new_number],
                        fg=Df.CELL_COLOR_DICT[new_number]
                    )
        # tkinter 中的函数 更新作用
        self.update_idletasks()

    # 检测按键状态并作出相应的回应
    def key_down(self, event):
        key = event.keysym
        print(event)
        if key == Df.KEY_QUIT:
            exit()
        if key == Df.KEY_BACK and (len(self.history_matrix) > 1):
            self.matrix = self.history_matrix.pop()
            self.update_grid_cells()
            print('back on step total step:', len(self.history_matrix))

        elif key in self.commands:
            self.matrix, done = self.commands[key](self.matrix)
            if done:
                self.matrix = logic.add_two(self.matrix)

                self.history_matrix.append(self.matrix)
                self.update_grid_cells()
                if logic.game_state(self.matrix) == 'win':
                    self.grid_cells[1][1].configure(text="You", bg=Df.BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(text="Win!", bg=Df.BACKGROUND_COLOR_CELL_EMPTY)
                if logic.game_state(self.matrix) == 'lose':
                    self.grid_cells[1][1].configure(text="You", bg=Df.BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(text="Lose!", bg=Df.BACKGROUND_COLOR_CELL_EMPTY)

    def generate_next(self):
        index = (gen(), gen())
        while self.matrix[index[0]][index[1]] != 0:
            index = (gen(), gen())
        self.matrix[index[0]][index[1]] = 2


game_windows = GameGrid()
