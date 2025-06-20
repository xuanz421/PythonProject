import random
from collections import deque

def difficultSetup():
    difficulty = int(input("Choose your difficulty(1~5)"))
    return difficulty
difficulty = difficultSetup()
WIDTH, HEIGHT = (difficulty * 10 + 1), (difficulty * 6 + 5)
WALL, PATH = 0, 1


#初始化
def initialize_maze():
    maze = [[WALL for _ in range(WIDTH)] for _ in range(HEIGHT)]


#创造起点
def create_start(maze):
    randomx = random.randrange(int(HEIGHT - (HEIGHT / 3 * 2)), int(HEIGHT - (HEIGHT / 3)), 2)
    randomy = random.randrange(int(WIDTH - (WIDTH / 3 * 2)), int(WIDTH - (WIDTH / 3)), 2)
    return randomx, randomy


#以n点(x,y)为坐标,随机抽选一个方向,往前两格(设为Target),
#判定其周围八方位是否=PATH,判定Target本身是否=PATH。
#若Target周围确认都是WALL,没有PATH,则将n点与Target之间的WALL变成PATH

#迷宫生成
def carve(maze,x,y):
    maze[x][y]= PATH
    dirs = [(0,2),(2,0),(0,-2),(-2,0)]#dy,dx从这里随机抽取一个方向
    random.shuffle(dirs)
    for dy, dx in dirs:
        nx, ny = x + dx, y + dy
        if 0 < nx < HEIGHT and 0 < ny < WIDTH and maze[nx][ny] == WALL:#避免把PATH铺设到边界，以及确认目标点位是WALL
            surrounded = True

            for ddx in [-1,0,1]:
                for ddy in [-1,0,1]:
                    if (ddx, ddy) ==(0,0):
                        continue #检查Target周围八个方位是否都为WALL（WALL=0）

                    tx = nx + ddx
                    ty = ny + ddy
                    if 0 <= tx < HEIGHT and 0 <= ty < WIDTH and maze[tx][ty]==PATH:#如果Target本身就是PATH，直接false
                        surrounded = False
            if surrounded:
                maze[x + dx//2][y + dy//2] = PATH #把n点与Target之间的WALL变成PATH
                carve(maze,nx,ny)#旧的Target变成新的n点，寻找新的Target

#创造环路
def create_loop(maze):
    walls_can_be_use = []

    for x in range(1, HEIGHT-1):
        for y in range(1, WIDTH -1):
            if maze[x][y] == WALL and can_convert_wall(maze,x,y):
                walls_can_be_use.append((x,y))

    random.shuffle(walls_can_be_use)
    max_holes = 1000
    holes_created = 0
    for x, y in walls_can_be_use:
        if holes_created >= max_holes:
            break

        if not will_form_open_area(maze,x,y):
            maze[x][y] = PATH
            holes_created += 1

    return holes_created


#打洞，形成环路
def can_convert_wall(maze,x,y):
    if maze[x][y] != WALL:
        return False
    
    #orth, orthogonal,正交
    #检查正交的四个方向，若符合条件且为PATH，加入（append）到orth_path中
    orth_direction = [(0,1), (0,-1), (1,0), (-1,0)]
    orth_paths = 0
    for dy, dx in orth_direction:
        nx, ny= x+dx, y+dy
        if 0 <= nx + HEIGHT and 0 <= ny < WIDTH and maze[nx][ny] == PATH:
                orth_paths += 1

    #确保有两个以上的正交路径
    if orth_paths < 1:
        return False
    
    can_make_loop = 0
    for dx, dy in orth_direction:
        for distance in range(1,5): #检查4格距离
            nx, ny = x + dx * distance, y + dy * distance
            if 0 <= nx < HEIGHT and 0 <= ny < WIDTH:
                if maze[nx][ny] == PATH:
                    can_make_loop += 1
                    break
            
    return can_make_loop >= 2

#检查避免出现2x2以上的“路径面积”, 维持迷宫的线性特性
def will_form_open_area(maze,x,y):
    #检查(x,y)为中心的3x3区域
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            open_count = 0
            for i in range(3):
                for j in range(3):
                    tx, ty = x+dx+i, y+dy+j
                    if 0 <= tx < HEIGHT and 0 <= ty < WIDTH:
                        if maze[tx][ty] == PATH or (tx == x and ty == y):#是路径/将要打洞的位置
                            open_count += 1

            #在3x3区域内，如果有≥5的路径点，则取消打洞
            if open_count >= 5:
                return True
    return False


#寻找距离起点最远的位置作为出口，利用DFS寻找所有最短路径，并在其中选择最长的
def find_farthest_exit(maze, start_x, start_y):
    distant_map = calculate_all_distances(maze, start_x, start_y)

#寻找四个边界的出口位置
    possible_exits = []
    for y in range(1, WIDTH-1):
        if maze[1][y] == PATH:
            possible_exits.append((0, y))
    for y in range(1, WIDTH-1):
        if maze[HEIGHT-2][y] == PATH:
            possible_exits.append((HEIGHT-1, y))
    for x in range(1, HEIGHT-1):
        if maze[x][1] == PATH:
            possible_exits.append((x, 0))
    for x in range(1, HEIGHT-1):
        if maze[x][WIDTH-2] == PATH:
            possible_exits.append((x, WIDTH-1))
        
    max_distance = -1
    farthest_exit = None

    for exit_x, exit_y in possible_exits:
        if exit_x == 0:  # 上边界
            distance = distant_map[1][exit_y]
        elif exit_x == HEIGHT-1:  # 下边界
            distance = distant_map[HEIGHT-2][exit_y]
        elif exit_y == 0:  # 左边界
            distance = distant_map[exit_x][1]
        else:  # 右边界
            distance = distant_map[exit_x][WIDTH-2]

        if distance > max_distance:
            max_distance = distance
            farthest_exit = (exit_x, exit_y)

    # 设置真正的出口
    if farthest_exit:
        ex, ey = farthest_exit
        maze[ex][ey] = PATH
        return farthest_exit
    
    #利用BFS计算所有出口位置到起点的距离
def calculate_all_distances(maze, start_x, start_y):
    dist = [[-1] * WIDTH for _ in range(HEIGHT)]#创造一个width*height的，由-1填满的列表
    dist[start_x][start_y] = 0 #将起点改为0
    queue = deque([(start_x, start_y)])

    while queue:
        x, y = queue.popleft()
        for dx, dy in [(0,1), (0,-1), (1,0), (-1,0)]:
            nx, ny = x+dx, y+dy
            if 0 <= nx < HEIGHT and 0 <= ny < WIDTH: #确保在迷宫范围内
                if maze[nx][ny] == PATH and dist[nx][ny] == -1: #确认新位置是PATH，且没访问过
                    dist[nx][ny] = dist[x][y] + 1#更新该位置的状态
                    queue.append((nx, ny))
    return dist
    
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
    # 创建迷宫数组
    maze = [[WALL for _ in range(WIDTH)] for _ in range(HEIGHT)]
    
    # 创建起点
    start_x, start_y = create_start(maze)
    
    # 生成迷宫主干
    carve(maze, start_x, start_y)
    
    # 创建环状路径
    loop_count = create_loop(maze)
    print(f"创建了 {loop_count} 个环状路径")
    
    # 找到最远出口
    exit_pos = find_farthest_exit(maze, start_x, start_y)
    start = (start_x, start_y)
    
    # 打印迷宫
    print_maze(maze, start, exit_pos)

main()