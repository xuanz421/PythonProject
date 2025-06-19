import random

# 迷宫参数
WIDTH, HEIGHT = 51, 39  # 必须为奇数
WALL, PATH = 0, 1

# 初始化迷宫全为墙体
maze = [[WALL for _ in range(WIDTH)] for _ in range(HEIGHT)]

# 递归回溯法（DFS）生成迷宫
def carve(x, y):
    maze[x][y] = PATH
    dirs = [(0,2), (0,-2), (2,0), (-2,0)]
    random.shuffle(dirs)
    for dx, dy in dirs:
        nx, ny = x + dx, y + dy
        if 0 < nx < HEIGHT and 0 < ny < WIDTH and maze[nx][ny] == WALL:
            # 检查周围，防止分支直接连通已有路径
            surrounded = True
            for ddx in [-1,0,1]:
                for ddy in [-1,0,1]:
                    if (ddx, ddy) == (0,0): continue
                    tx, ty = nx+ddx, ny+ddy
                    if 0<=tx<HEIGHT and 0<=ty<WIDTH and maze[tx][ty]==PATH:
                        surrounded = False
            if surrounded:
                maze[x + dx//2][y + dy//2] = PATH
                carve(nx, ny)

# 入口点
carve(1, 1)
maze[1][0] = PATH  # 起点
maze[HEIGHT-2][WIDTH-1] = PATH  # 终点

# 打洞函数
def can_convert_wall(x, y):
    if maze[x][y] != WALL:
        return False
    orth = [(0,1), (0,-1), (1,0), (-1,0)]
    diag = [(-1,-1), (-1,1), (1,-1), (1,1)]
    orth_count = 0
    for dx, dy in orth:
        nx, ny = x+dx, y+dy
        if 0<=nx<HEIGHT and 0<=ny<WIDTH and maze[nx][ny]==PATH:
            orth_count += 1
    if orth_count < 3:
        return False
    for dx, dy in diag:
        nx, ny = x+dx, y+dy
        if 0<=nx<HEIGHT and 0<=ny<WIDTH and maze[nx][ny]==PATH:
            return False
    return True

# 随机打洞
all_walls = [(x, y) for x in range(1, HEIGHT-1) for y in range(1, WIDTH-1)]
random.shuffle(all_walls)
holes = 0
max_holes = WIDTH * HEIGHT // 10  # 控制洞的数量，可调整
for (x, y) in all_walls:
    if can_convert_wall(x, y):
        maze[x][y] = PATH
        holes += 1
        if holes >= max_holes:
            break

# 可视化
def print_maze(maze):
    for row in maze:
        print("".join('  ' if cell==PATH else '██' for cell in row))

print_maze(maze)
