import tkinter as tk
import mazeGenerator as generator

CELL_SIZE = 24
class GameMenu():
    def __init__(self,root):
        self.root = root
        self.menu_frame = tk.Frame(root, bg="#222", padx=30, pady=30)
        self.menu_frame.pack(expand=True)

        title = tk.Label(self.menu_frame, text="迷宫小游戏", font=("黑体", 32), fg="#4cf", bg="#222")
        title.pack(pady=(0,20))
        author = tk.Label(self.menu_frame, text="作者：第四小组", font=("黑体", 18), fg="#ffb", bg="#222")
        author.pack(pady=(0,30))
        diff_label = tk.Label(self.menu_frame, text="选择难度（1-5）", font=("黑体", 18), bg="#222", fg="#fff")
        diff_label.pack()
        self.diff = tk.IntVar(value=2)
        tk.Scale(self.menu_frame, from_=1, to=5, orient=tk.HORIZONTAL, variable=self.diff, length=200,
                 showvalue=True, bg="#222", fg="#fff", troughcolor="#334").pack(pady=8)

        start_btn = tk.Button(self.menu_frame, text="开始游戏", font=("黑体", 18), bg="#2c6", fg="#fff",
                              width=12, height=2, command=self.start_game)
        start_btn.pack(pady=(20,0))


    def start_game(self):
        self.menu_frame.destroy()
        MazeWindow(self.root ,self.diff.get())


class MazeWindow:

    def __init__(self, master, difficulty):
        self.master = master
        self.MAZE_HEIGHT, self.MAZE_WIDTH = difficulty * 6 + 5, difficulty * 10 + 1
        self.maze, self.start, self.end = generator.generate_maze_data(self.MAZE_WIDTH, self.MAZE_HEIGHT)

        for widget in master.winfo_children():
            widget.destroy()
        
        self.canvas = tk.Canvas(self.master, width= self.MAZE_WIDTH * CELL_SIZE, height= self.MAZE_HEIGHT * CELL_SIZE, bg="black")
        self.canvas.pack()

        self.draw_maze()
        self.player = self.canvas.create_oval(
            self.start[1]*CELL_SIZE+4,
            self.start[0]*CELL_SIZE+4,
            self.start[1]*CELL_SIZE+CELL_SIZE-4,
            self.start[0]*CELL_SIZE+CELL_SIZE-4,
            fill='yellow')
        self.player_pos = list(self.start)
        self.master.bind("<KeyPress>", self.move)

        self.master.mainloop()


    def move(self, event):
        key = event.keysym.lower()
        dx, dy = 0, 0
        if key in ['up', 'w']:
            dx, dy = -1, 0
        elif key in ['down', 's']:
            dx, dy = 1, 0
        elif key in ['left', 'a']:
            dx, dy = 0, -1
        elif key in ['right', 'd']:
            dx, dy = 0, 1
        else:
            return
        
        nx, ny = self.player_pos[0]+dx, self.player_pos[1]+dy
        if (0 <= nx < self.MAZE_HEIGHT and 0 <= ny < self.MAZE_WIDTH 
            and self.maze[nx][ny] == generator.PATH):
            self.player_pos = [nx, ny]
            self.canvas.coords(
                self.player,
                ny*CELL_SIZE+4, nx*CELL_SIZE+4,
                ny*CELL_SIZE+CELL_SIZE-4, nx*CELL_SIZE+CELL_SIZE-4
            )
            if (nx, ny) == self.end:
                self.win()

    def win(self):
        self.canvas.create_text(
            self.MAZE_WIDTH*CELL_SIZE//2, self.MAZE_HEIGHT*CELL_SIZE//2,
            text="胜利！", font=("黑体", 36), fill="gold")


        
    def draw_maze(self):
        for i in range(self.MAZE_HEIGHT):
            for j in range(self.MAZE_WIDTH):
                if (i, j) == self.start:
                    color = "green"
                elif (i, j) == self.end:
                    color = "red"
                elif self.maze[i][j] == generator.PATH:
                    color = "white"
                else:
                    color = "black"
                self.canvas.create_rectangle(
                    j*CELL_SIZE, i*CELL_SIZE,
                    (j+1)*CELL_SIZE, (i+1)*CELL_SIZE,
                    fill=color, outline='gray'
                )


if __name__ == "__main__":
    root = tk.Tk()
    root.title("迷宫小游戏")
    GameMenu(root)
    root.mainloop()

