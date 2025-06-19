import random
from collections import deque

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
randomx = random.randrange(int(HEIGHT - (HEIGHT / 3 * 2)), int(HEIGHT - (HEIGHT / 3)), 2)
randomy = random.randrange(int(WIDTH - (WIDTH / 3 * 2)), int(WIDTH - (WIDTH / 3)), 2)

carve(randomx, randomy)
"""maze[1][0] = PATH  # 起点"""
"""maze[HEIGHT-2][WIDTH-1] = PATH"""  # 终点

# 打洞函数
def can_convert_wall(x, y):
    if maze[x][y] != WALL:
        return False
    
    # 检查正交方向
    orth_dirs = [(0,1), (0,-1), (1,0), (-1,0)]
    orth_paths = []
    for dx, dy in orth_dirs:
        nx, ny = x+dx, y+dy
        if 0 <= nx < HEIGHT and 0 <= ny < WIDTH:
            if maze[nx][ny] == PATH:
                orth_paths.append((nx, ny))
    
    # 必须恰好有两个正交路径才可打洞
    if len(orth_paths) != 2:
        return False
    
    # 检查两个路径点的相对位置
    p1, p2 = orth_paths
    # 如果两个路径点在同一行或同一列，则安全
    if p1[0] == p2[0] or p1[1] == p2[1]:
        return True
    
    # 检查对角方向是否有路径
    diag_dirs = [(1,1), (1,-1), (-1,1), (-1,-1)]
    for dx, dy in diag_dirs:
        nx, ny = x+dx, y+dy
        if 0 <= nx < HEIGHT and 0 <= ny < WIDTH:
            if maze[nx][ny] == PATH:
                return False
    
    return True

all_walls = [(x, y) for x in range(1, HEIGHT-1) for y in range(1, WIDTH-1)]
random.shuffle(all_walls)
holes = 0
max_holes = random.randint(3, 10)#WIDTH * HEIGHT // 100  # 控制洞的数量，可调整
for (x, y) in all_walls:
    if can_convert_wall(x, y):
        maze[x][y] = PATH
        holes += 1
        if holes >= max_holes:
            break

# 使用BFS计算最短路径长度
def bfs_distance(start_x, start_y, end_x, end_y):
    # 创建距离矩阵
    dist = [[-1] * WIDTH for _ in range(HEIGHT)]
    dist[start_x][start_y] = 0
    
    # 使用队列进行BFS
    queue = deque([(start_x, start_y)])
    
    while queue:
        x, y = queue.popleft()
        
        # 如果到达终点，返回距离
        if x == end_x and y == end_y:
            return dist[x][y]
        
        # 检查四个方向
        for dx, dy in [(0,1), (0,-1), (1,0), (-1,0)]:
            nx, ny = x + dx, y + dy
            
            # 确保在迷宫范围内且是路径
            if 0 <= nx < HEIGHT and 0 <= ny < WIDTH:
                if maze[nx][ny] == PATH and dist[nx][ny] == -1:
                    dist[nx][ny] = dist[x][y] + 1
                    queue.append((nx, ny))
    
    # 如果无法到达，返回一个很大的负数
    return -10000

# 找到所有可能的出口位置
def find_possible_exits():
    exits = []
    
    # 上边界
    for y in range(1, WIDTH-1, 2):
        if maze[1][y] == PATH:
            exits.append((0, y))
    
    # 下边界
    for y in range(1, WIDTH-1, 2):
        if maze[HEIGHT-2][y] == PATH:
            exits.append((HEIGHT-1, y))
    
    # 左边界
    for x in range(1, HEIGHT-1, 2):
        if maze[x][1] == PATH:
            exits.append((x, 0))
    
    # 右边界
    for x in range(1, HEIGHT-1, 2):
        if maze[x][WIDTH-2] == PATH:
            exits.append((x, WIDTH-1))
    
    return exits

# 找到距离起点最远的出口
def find_farthest_exit():
    possible_exits = find_possible_exits()
    if not possible_exits:
        # 如果没有找到出口，使用右下角
        maze[HEIGHT-2][WIDTH-1] = PATH
        return (HEIGHT-2, WIDTH-1)
    
    max_distance = -1
    farthest_exit = None
    
    for exit_x, exit_y in possible_exits:
        # 临时设置出口为路径
        maze[exit_x][exit_y] = PATH
        
        # 计算从起点到出口的距离
        distance = bfs_distance(randomx, randomy, exit_x, exit_y)
        
        if distance > max_distance:
            max_distance = distance
            farthest_exit = (exit_x, exit_y)
        
        # 恢复出口为墙（稍后我们会设置真正的出口）
        maze[exit_x][exit_y] = WALL
    
    # 设置真正的出口
    if farthest_exit:
        ex, ey = farthest_exit
        maze[ex][ey] = PATH
        return farthest_exit
    
    # 如果所有出口都无效，使用右下角
    maze[HEIGHT-2][WIDTH-1] = PATH
    return (HEIGHT-2, WIDTH-1)

# 找到距离起点最远的出口
exit_pos = find_farthest_exit()


# 可视化
def print_maze(maze):
    start = (randomx, randomy)  # 起点
    end = exit_pos  # 终点
    for i, row in enumerate(maze):
        line = ""
        for j, cell in enumerate(row):
            if (i, j) == start:
                line += 'SS'  # 用特殊字符表示起点
            elif (i, j) == end:
                line += 'EE'  # 用特殊字符表示终点（可选）
            else:
                line += '  ' if cell == PATH else '██'
        print(line)


print_maze(maze)
