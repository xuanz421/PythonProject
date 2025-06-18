import tkinter as tk

class mazeWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Maze")

        self.canvas = tk.Canvas(self.window, width=800, height=800, bg="white")
        self.canvas.pack()

        # 创建一个小方块（起始坐标100,100, 宽高40x40）
        self.rect = self.canvas.create_rectangle(100, 100, 140, 140, fill="blue")

        # 单位每次移动的步长
        self.step = 50

        # 绑定键盘事件
        self.window.bind("<KeyPress>", self.move)

        self.window.mainloop()


    def move(self, event):
        if event.keysym == 'Up':
            self.canvas.move(self.rect, 0, -self.step)
        elif event.keysym == 'w':
            self.canvas.move(self.rect, 0, -self.step)
        elif event.keysym == 'Down':
            self.canvas.move(self.rect, 0, self.step)
        elif event.keysym == 'Left':
            self.canvas.move(self.rect, -self.step, 0)
        elif event.keysym == 'Right':
            self.canvas.move(self.rect, self.step, 0)
        

mazeWindow()