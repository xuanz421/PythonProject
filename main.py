import tkinter as tk
from tkinter import messagebox
import mazeGenerator as generator
import random
from datetime import datetime

CELL_SIZE = 24
class GameMenu:
    def __init__(self,root):
        self.root = root
        self.root.title("Maze Explorer")
        self.root.geometry("600x500")
        self.root.configure(bg="black")

        self.green = "green"
        self.orange = "orange"
        self.white = "white"
        self.dark_gray = "gray20"
        self.medium_gray = "gray30"
        self.light_gray = "gray40"

        self.create_widgets()
        self.draw_maze()

        self.root.mainloop()

    def create_widgets(self):
        self.main_frame1 = tk.Frame(root, bg="black")
        self.main_frame1.pack(expand=True, fill="both", padx=50, pady=50)

        title = tk.Label(self.main_frame1, text="MAZE EXPLORER", font=("Courier", 36), fg=self.green, bg="black")
        title.pack(padx=(15, 0))

        subtitle = tk.Label(
            self.main_frame1,
            text="Discover the Unknown Maze World",
            font=("Arial", 12),
            fg=self.white,
            bg="black"
        )
        subtitle.pack(pady=(0, 40))

        start_button = tk.Button(
            self.main_frame1,
            text="Start Game",
            font=("Arial", 14),
            bg=self.green,
            fg="white",
            width=15,
            height=2,
            command=self.start_game
        )
        start_button.pack(pady=10)

        difficulty_frame = tk.Frame(self.main_frame1, bg="black")
        difficulty_frame.pack(pady=20)

        tk.Label(
            difficulty_frame,
            text="Difficulty:",
            font=("Arial", 12),
            fg=self.white,
            bg="black"
        ).pack(side="left", padx=(0, 10))

        self.difficulty = tk.StringVar(value="3")
        options = ["1-Easy", "2-Medium", "3-Hard", "4-Extreme"]
        tk.OptionMenu(
            difficulty_frame,
            self.difficulty,
            *options
        ).pack(side="left")

        self.canvas = tk.Canvas(
            self.main_frame1,
            width=200,
            height=200,
            bg=self.dark_gray,
            highlightthickness=0
        )

    def draw_maze(self):
        cell_size = 20
        rows = 10
        cols = 10

        for i in range(rows):
            for j in range(cols):
                x1 = j * cell_size
                y1 = i * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size

                if random.random() < 0.3:  # 30% chance to be a wall
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2,
                        fill=self.medium_gray,
                        outline=self.light_gray
                    )
                else:
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2,
                        fill=self.dark_gray,
                        outline=self.light_gray
                    )

        self.canvas.create_oval(0, 0, cell_size, cell_size, fill=self.green)
        self.canvas.pack(pady=(50, 0))

    def start_game(self):
        self.main_frame1.destroy()
        level = int(self.difficulty.get().split("-")[0])
        messagebox.showinfo(
            "Game Start",
            f"Maze adventure begins!\nDifficulty level: {level}"
        )
        MazeWindow(self.root, level)


class MazeWindow:

    def __init__(self, master, difficulty):
        self.master = master
        self.difficulty =difficulty
        if difficulty == 1:
            self.MAZE_HEIGHT, self.MAZE_WIDTH = 11, 11
        elif difficulty == 2:
            self.MAZE_HEIGHT, self.MAZE_WIDTH = 17, 21
        elif difficulty == 3:
            self.MAZE_HEIGHT, self.MAZE_WIDTH = 21, 33
        elif difficulty == 4:
            self.MAZE_HEIGHT, self.MAZE_WIDTH = 27, 41

        self.maze, self.start, self.end = generator.generate_maze_data(self.MAZE_WIDTH, self.MAZE_HEIGHT)

        for widget in master.winfo_children():
            widget.destroy()

        self.display()
        self.timer = Timer(self.frame)
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


    def display(self):
        self.frame = tk.Frame(root, bg="black")
        self.canvas = tk.Canvas(self.frame, width=self.MAZE_WIDTH * CELL_SIZE, height=self.MAZE_HEIGHT * CELL_SIZE,
                                bg="black")
        title = tk.Label(self.frame, text=f"MAZE EXPLORER Level: {self.difficulty}", font=("Courier", 36), fg="gold", bg="black")
        menu_btn = tk.Button(self.frame, text="Menu", font=("Courier", 20), bg="green", fg="white",
                              width=12, height=2, command=self.menu)

        title.pack(padx=(50, 50))
        menu_btn.pack(side = tk.LEFT, padx=(20, 0))
        self.canvas.pack(expand=True, padx=(20, 70))
        self.frame.pack(expand=True, fill="both", padx=20, pady=20)

    def menu(self):
        self.window = tk.Tk()
        self.window.geometry("600x500")
        self.window.configure(bg="black")

        self.menu_frame = tk.Frame(self.window, bg="black")
        title = tk.Label(self.menu_frame, text="MAZE EXPLORER", font=("Courier", 36), fg="gold", bg="black")
        back_btn = tk.Button(self.menu_frame, text="Back to the Game", font=("Courier", 20), bg="green", fg="white",
                              width=22, height=2, command = self.back)
        restart_btn = tk.Button(self.menu_frame, text="Back to the Main Menu", font=("Courier", 20), bg="green",
                                fg="white",width=22, height=2, command = self.restart)
        game_rule_btn = tk.Button(self.menu_frame, text="Game rule", font=("Courier", 20), bg="green", fg="white",
                              width=22, height=2, command = self.game_rule)
        exit_btn = tk.Button(self.menu_frame, text="EXIT", font=("Courier", 20), bg="green", fg="white",
                              width=22, height=2, command = self.exit)

        self.menu_frame.pack()
        title.pack(padx=(20, 0))
        back_btn.pack(padx=(20, 0))
        restart_btn.pack(padx=(20, 0))
        game_rule_btn.pack(padx=(20, 0))
        exit_btn.pack(padx=(20,0))

    def restart(self):
        self.frame.destroy()
        self.window.destroy()
        GameMenu(root)

    def exit(self):
        EXIT()
        self.window.destroy()

    def game_rule(self):
        self.menu_frame.destroy()
        self.gamerule_frame = tk.Frame(self.window, bg="black")
        game_rule_1 = tk.Label(self.gamerule_frame, text ="The yellow oval is you!!!",font=("Courier", 20),
                               fg="gold", bg="#222")
        game_rule_2 = tk.Label(self.gamerule_frame,text="Start from the green box, the end is the red box!!!",
                               font=("Courier", 20), fg="gold", bg="#222")
        game_rule_3 = tk.Label(self.gamerule_frame,text="Find a way out!!!",font=("Courier", 20), fg="gold", bg="#222")
        control_up = tk.Label(self.gamerule_frame, text="Use the keyboard of up arrow to shift up",
                              font=("Courier", 20), fg="#4cf", bg="#222")
        control_down = tk.Label(self.gamerule_frame, text="Use the keyboard of down arrow to shift down",
                                font=("Courier", 20), fg="#4cf", bg="#222")
        control_right = tk.Label(self.gamerule_frame, text="Use the keyboard of right arrow to shift right",
                                 font=("Courier", 20), fg="#4cf", bg="#222")
        control_left = tk.Label(self.gamerule_frame, text="Use the keyboard of left arrow to shift left",
                                font=("Courier", 20), fg="#4cf", bg="#222")
        back_to_menu_btn = tk.Button(self.gamerule_frame, text="Back to the menu", font=("Courier", 20),
                                     bg="green", fg="white",width=20, height=2, command = self.back_menu)

        self.gamerule_frame.pack(padx=(15, 0))
        game_rule_1.pack(padx=(15, 0))
        game_rule_2.pack(padx=(15, 0))
        game_rule_3.pack(padx=(15, 0))
        control_up.pack(padx=(15, 0))
        control_down.pack(padx=(15, 0))
        control_right.pack(padx=(15, 0))
        control_left.pack(padx=(15, 0))
        back_to_menu_btn.pack(padx=(15, 0))

    def back_menu(self):
        self.window.destroy()
        self.menu()

    def back(self):
        self.window.destroy()

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
        complete_time = str(datetime.now() - self.timer.start_time).split('.')[0]
        self.frame.destroy()
        End(root, complete_time, self.difficulty)
        
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

class End:
    def __init__(self, root, complete_time, difficulty):
        self.root = root
        self.complete_time = complete_time
        self.root.title("GAME END")
        self.root.geometry("600x500")
        self.root.configure(bg="black")
        self.gold = "gold"
        self.green = "green"
        self.orange = "orange"
        self.white = "white"

        hours, minutes, seconds = map(int, complete_time.split(':'))
        final_time = hours * 3600 + minutes * 60 + seconds
        self.rating = self.get_rating(final_time, difficulty)

        self.display()

    def display(self):
        self.end_frame = tk.Frame(root, bg="black")
        self.end_frame.pack(expand=True, fill="both", padx=50, pady=50)

        title = tk.Label(self.end_frame, text="CONGRATULATIONS!!!", font=("Courier", 48), fg=self.gold, bg="black")
        again_btn = tk.Button(self.end_frame, text="PLAY AGAIN", font=("Courier", 36), bg=self.green, fg=self.white,
                              width=12, height=2, command=self.start_again)
        exit_btn = tk.Button(self.end_frame, text="EXIT", font=("Courier", 36), bg=self.green, fg=self.white,
                              width=12, height=2, command=self.exit)
        time = tk.Label(self.end_frame,text=f"END TIME: {self.complete_time}",font=("Courier", 24),
                              fg=self.gold,bg="black")
        grade = tk.Label(self.end_frame,text=f"Grade: {self.rating}",font=("Courier", 24),
                              fg=self.gold,bg="black")


        title.pack(padx=(15, 0))
        again_btn.pack(pady=(20, 0))
        exit_btn.pack(pady=(20, 0))
        time.pack(pady=(10, 0))
        grade.pack(pady=(10, 0))

    def get_rating(self, final_time, difficulty):
        if final_time <= 15 * difficulty:
            return "S (ABSOLUTELY PERFECT)"
        elif final_time <= 30 * difficulty:
            return "A (YOU ARE EXCELLENT)"
        elif final_time <= 45 * difficulty:
            return "B (YOU ARE SO CLOSE)"
        elif final_time <= 60 * difficulty:
            return "C (YOU ARE GETTING BETTER)"
        elif final_time <= 90 * difficulty:
            return "D (YOU ARE IN THE GAME)"
        else:
            return "Fail (PRACTISE MORE)"

    def start_again(self):
        self.end_frame.destroy()
        GameMenu(root)

    def exit(self):
        EXIT()


class Timer:
    def __init__(self, root):
        self.root = root
        self.run = True
        self.start_time = datetime.now()

        self.label = tk.Label(root, text="00:00", font=("Courier", 24))
        self.label.pack()

        self.start()

    def start(self):
        if self.run:
            running = datetime.now() - self.start_time
            self.label.config(text=str(running).split(".")[0])
        self.root.after(200, self.start)


def EXIT():
    root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    GameMenu(root)
    root.mainloop()

