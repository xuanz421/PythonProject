import random
from collections import deque

WALL, PATH = 0, 1

#初始化
def initialize_maze(width, height):
    maze = [[WALL for _ in range(width)] for _ in range(height)]


def generate_maze_data(width, height):
    
    maze = [[WALL for _ in range(width)] for _ in range(height)]
    start_x, start_y = create_start(maze, width, height)
    carve(maze, start_x, start_y, width, height)
    create_loop(maze, width, height)
    exit_pos = find_farthest_exit(maze, start_x, start_y, width, height)
    start = (start_x, start_y)
    return maze, start, exit_pos


#创造起点
def create_start(maze, width, height):
    randomx = random.randrange(int(height - (height / 3 * 2)), int(height - (height / 3)), 2)
    randomy = random.randrange(int(width - (width / 3 * 2)), int(width - (width / 3)), 2)
    return randomx, randomy


#以n点(x,y)为坐标,随机抽选一个方向,往前两格(设为Target),
#判定其周围八方位是否=PATH,判定Target本身是否=PATH。
#若Target周围确认都是WALL,没有PATH,则将n点与Target之间的WALL变成PATH

#迷宫生成
def carve(maze,x,y, width, height):
    maze[x][y]= PATH
    dirs = [(0,2),(2,0),(0,-2),(-2,0)]#dy,dx从这里随机抽取一个方向
    random.shuffle(dirs)
    for dy, dx in dirs:
        nx, ny = x + dx, y + dy
        if 0 < nx < height and 0 < ny < width and maze[nx][ny] == WALL:#避免把PATH铺设到边界，以及确认目标点位是WALL
            surrounded = True

            for ddx in [-1,0,1]:
                for ddy in [-1,0,1]:
                    if (ddx, ddy) ==(0,0):
                        continue #检查Target周围八个方位是否都为WALL（WALL=0）

                    tx = nx + ddx
                    ty = ny + ddy
                    if 0 <= tx < height and 0 <= ty < width and maze[tx][ty]==PATH:#如果Target本身就是PATH，直接false
                        surrounded = False
            if surrounded:
                maze[x + dx//2][y + dy//2] = PATH #把n点与Target之间的WALL变成PATH
                carve(maze, nx, ny, width, height)#旧的Target变成新的n点，寻找新的Target

#创造环路
def create_loop(maze, width, height):
    walls_can_be_use = []

    for x in range(1, height-1):
        for y in range(1, width -1):
            if maze[x][y] == WALL and can_convert_wall(maze, x, y, width, height):
                walls_can_be_use.append((x,y))

    random.shuffle(walls_can_be_use)
    max_holes = 1000
    holes_created = 0
    for x, y in walls_can_be_use:
        if holes_created >= max_holes:
            break

        if not will_form_open_area(maze,x,y, width, height):
            maze[x][y] = PATH
            holes_created += 1

    return holes_created


#打洞，形成环路
def can_convert_wall(maze,x,y, width, height):
    if maze[x][y] != WALL:
        return False
    
    #orth, orthogonal,正交
    #检查正交的四个方向，若符合条件且为PATH，加入（append）到orth_path中
    orth_direction = [(0,1), (0,-1), (1,0), (-1,0)]
    orth_paths = 0
    for dy, dx in orth_direction:
        nx, ny= x+dx, y+dy
        if 0 <= nx + height and 0 <= ny < width and maze[nx][ny] == PATH:
                orth_paths += 1

    #确保有两个以上的正交路径
    if orth_paths < 1:
        return False
    
    can_make_loop = 0
    for dx, dy in orth_direction:
        for distance in range(1,5): #检查4格距离
            nx, ny = x + dx * distance, y + dy * distance
            if 0 <= nx < height and 0 <= ny < width:
                if maze[nx][ny] == PATH:
                    can_make_loop += 1
                    break
            
    return can_make_loop >= 2

#检查避免出现2x2以上的“路径面积”, 维持迷宫的线性特性
def will_form_open_area(maze,x,y, width, height):
    #检查(x,y)为中心的3x3区域
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            open_count = 0
            for i in range(3):
                for j in range(3):
                    tx, ty = x+dx+i, y+dy+j
                    if 0 <= tx < height and 0 <= ty < width:
                        if maze[tx][ty] == PATH or (tx == x and ty == y):#是路径/将要打洞的位置
                            open_count += 1

            #在3x3区域内，如果有≥5的路径点，则取消打洞
            if open_count >= 5:
                return True
    return False


#寻找距离起点最远的位置作为出口，利用DFS寻找所有最短路径，并在其中选择最长的
def find_farthest_exit(maze, start_x, start_y, width, height):
    distant_map = calculate_all_distances(maze, start_x, start_y, width, height)

#寻找四个边界的出口位置
    possible_exits = []
    for y in range(1, width-1):
        if maze[1][y] == PATH:
            possible_exits.append((0, y))
    for y in range(1, width-1):
        if maze[height-2][y] == PATH:
            possible_exits.append((height-1, y))
    for x in range(1, height-1):
        if maze[x][1] == PATH:
            possible_exits.append((x, 0))
    for x in range(1, height-1):
        if maze[x][width-2] == PATH:
            possible_exits.append((x, width-1))
        
    max_distance = -1
    farthest_exit = None

    for exit_x, exit_y in possible_exits:
        if exit_x == 0:  # 上边界
            distance = distant_map[1][exit_y]
        elif exit_x == height-1:  # 下边界
            distance = distant_map[height-2][exit_y]
        elif exit_y == 0:  # 左边界
            distance = distant_map[exit_x][1]
        else:  # 右边界
            distance = distant_map[exit_x][width-2]

        if distance > max_distance:
            max_distance = distance
            farthest_exit = (exit_x, exit_y)

    # 设置真正的出口
    if farthest_exit:
        ex, ey = farthest_exit
        maze[ex][ey] = PATH
        return farthest_exit
    
    #利用BFS计算所有出口位置到起点的距离
def calculate_all_distances(maze, start_x, start_y, width, height):
    dist = [[-1] * width for _ in range(height)]#创造一个width*height的，由-1填满的列表
    dist[start_x][start_y] = 0 #将起点改为0
    queue = deque([(start_x, start_y)])

    while queue:
        x, y = queue.popleft()
        for dx, dy in [(0,1), (0,-1), (1,0), (-1,0)]:
            nx, ny = x+dx, y+dy
            if 0 <= nx < height and 0 <= ny < width: #确保在迷宫范围内
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



