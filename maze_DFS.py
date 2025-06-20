import random
from collections import deque

# 迷宫参数
WIDTH, HEIGHT = 31, 23  # 必须为奇数
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
def create_start(maze):
    randomx = random.randrange(int(HEIGHT - (HEIGHT / 3 * 2)), int(HEIGHT - (HEIGHT / 3)), 2)
    randomy = random.randrange(int(WIDTH - (WIDTH / 3 * 2)), int(WIDTH - (WIDTH / 3)), 2)
    return randomx, randomy
"""maze[1][0] = PATH  # 起点"""
"""maze[HEIGHT-2][WIDTH-1] = PATH"""  # 终点

# 打洞函数
def create_loops(maze):
    """创建更多更大的环状路径"""
    candidate_walls = []
    
    # 收集所有可能的打洞位置
    for x in range(1, HEIGHT-1):
        for y in range(1, WIDTH-1):
            if maze[x][y] == WALL and has_potential_for_large_loop(maze, x, y):
                candidate_walls.append((x, y))
    
    random.shuffle(candidate_walls)
    max_holes = min(len(candidate_walls), WIDTH * HEIGHT // 8)  # 显著增加打洞数量
    holes_created = 0
    
    for x, y in candidate_walls:
        if holes_created >= max_holes:
            break
        
        # 放宽开放区域检查
        if not will_form_large_open_area(maze, x, y):
            maze[x][y] = PATH
            holes_created += 1
    
    # 打印打洞数量信息
    print(f"创建了 {holes_created} 个环状路径")
    return holes_created

def has_potential_for_large_loop(maze, x, y):
    """检查墙体是否有可能形成大环"""
    if maze[x][y] != WALL:
        return False
    
    # 检查正交方向的路径数量
    orth_dirs = [(0,1), (0,-1), (1,0), (-1,0)]
    orth_paths = 0
    for dx, dy in orth_dirs:
        nx, ny = x + dx, y + dy
        if 0 <= nx < HEIGHT and 0 <= ny < WIDTH and maze[nx][ny] == PATH:
            orth_paths += 1
    
    # 只需要至少1个正交相邻路径（放宽条件）
    if orth_paths < 1:
        return False
    
    # 检查是否有形成大环的潜力（至少两个方向有路径）
    potential_dirs = 0
    for dx, dy in orth_dirs:
        # 检查路径延伸方向
        for distance in range(1, 5):  # 检查4格距离
            nx, ny = x + dx * distance, y + dy * distance
            if 0 <= nx < HEIGHT and 0 <= ny < WIDTH:
                if maze[nx][ny] == PATH:
                    potential_dirs += 1
                    break
    
    # 至少有两个方向有路径延伸
    return potential_dirs >= 2

def will_form_large_open_area(maze, x, y):
    """放宽的开放区域检查 - 允许小开放区域"""
    # 检查3x3区域
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            open_count = 0
            for i in range(3):
                for j in range(3):
                    tx, ty = x + dx + i, y + dy + j
                    if 0 <= tx < HEIGHT and 0 <= ty < WIDTH:
                        if maze[tx][ty] == PATH or (tx == x and ty == y):
                            open_count += 1
            
            # 如果3x3区域中有7个或更多路径点，则阻止打洞
            if open_count >= 5:
                return True
    
    return False


def find_farthest_exit(maze, start_x, start_y):
    """找到距离起点最远的出口"""
    # 计算所有位置到起点的距离
    dist_map = calculate_all_distances(maze, start_x, start_y)
    
    # 找到所有可能的出口位置
    possible_exits = []
    # 上边界
    for y in range(1, WIDTH-1):
        if maze[1][y] == PATH:
            possible_exits.append((0, y))
    # 下边界
    for y in range(1, WIDTH-1):
        if maze[HEIGHT-2][y] == PATH:
            possible_exits.append((HEIGHT-1, y))
    # 左边界
    for x in range(1, HEIGHT-1):
        if maze[x][1] == PATH:
            possible_exits.append((x, 0))
    # 右边界
    for x in range(1, HEIGHT-1):
        if maze[x][WIDTH-2] == PATH:
            possible_exits.append((x, WIDTH-1))
    
    if not possible_exits:
        # 如果没有找到出口，使用右下角
        maze[HEIGHT-2][WIDTH-1] = PATH
        return (HEIGHT-2, WIDTH-1)
    
    # 找到距离最远的出口
    max_distance = -1
    farthest_exit = None
    
    for exit_x, exit_y in possible_exits:
        # 检查距离（出口位置在dist_map中可能为-1，因为当前是墙）
        # 所以检查出口内部相邻点的距离
        if exit_x == 0:  # 上边界
            distance = dist_map[1][exit_y]
        elif exit_x == HEIGHT-1:  # 下边界
            distance = dist_map[HEIGHT-2][exit_y]
        elif exit_y == 0:  # 左边界
            distance = dist_map[exit_x][1]
        else:  # 右边界
            distance = dist_map[exit_x][WIDTH-2]
        
        if distance > max_distance:
            max_distance = distance
            farthest_exit = (exit_x, exit_y)
    
    # 设置真正的出口
    if farthest_exit:
        ex, ey = farthest_exit
        maze[ex][ey] = PATH
        return farthest_exit
    
    # 如果所有出口都无效，使用右下角
    maze[HEIGHT-2][WIDTH-1] = PATH
    return (HEIGHT-2, WIDTH-1)

def calculate_all_distances(maze, start_x, start_y):
    """计算所有位置到起点的距离"""
    dist = [[-1] * WIDTH for _ in range(HEIGHT)]
    dist[start_x][start_y] = 0
    queue = deque([(start_x, start_y)])
    
    while queue:
        x, y = queue.popleft()
        for dx, dy in [(0,1), (0,-1), (1,0), (-1,0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < HEIGHT and 0 <= ny < WIDTH: #确保在迷宫范围内
                if maze[nx][ny] == PATH and dist[nx][ny] == -1: #确认新位置是PATH，且没访问过
                    dist[nx][ny] = dist[x][y] + 1#更新该位置的状态
                    queue.append((nx, ny))
    return dist



# 可视化
def print_maze(maze, start, exit_pos):
    for i, row in enumerate(maze):
        line = ""
        for j, cell in enumerate(row):
            if (i, j) == start:
                line += 'SS'  # 起点
            elif (i, j) == exit_pos:
                line += 'EE'  # 终点
            else:
                line += '  ' if cell == PATH else '██'
        print(line)

def main():
    global maze
    # 重置迷宫
    maze = [[WALL for _ in range(WIDTH)] for _ in range(HEIGHT)]
    
    # 创建起点并生成迷宫主干
    start_x, start_y = create_start(maze)
    carve(start_x, start_y)
    
    # 创建环状路径 - 尝试多次直到有足够环
    loop_count = 0
    max_attempts = 5
    
    for attempt in range(max_attempts):
        loop_count = create_loops(maze)
        if loop_count >= WIDTH * HEIGHT // 15:  # 如果创建了足够多的环
            break
    
    print(f"最终创建了 {loop_count} 个环状路径")
    
    # 找到最远出口
    exit_pos = find_farthest_exit(maze, start_x, start_y)
    start = (start_x, start_y)
    
    # 打印迷宫
    print_maze(maze, start, exit_pos)

if __name__ == "__main__":
    main()