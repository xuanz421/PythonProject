import random


def difficultSetup():
    difficulty = int(input("Choose your difficulty(1~5)"))
    return difficulty

difficulty = difficultSetup()
WIDTH, HEIGHT = (difficulty * 10 + 1), (difficulty * 6 + 5)
WALL, PATH = 0, 1

maze = [[WALL for _ in range(WIDTH)] for _ in range(HEIGHT)]


#以n点(x,y)为坐标，随机抽选一个方向，往前两格（设为Target），
#判定其周围八方位是否=PATH，判定Target本身是否=PATH。
#若Target周围确认都是WALL，没有PATH，则将n点与Target之间的WALL变成PATH
def carve(x,y):
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
                carve(nx,ny)#旧的Target变成新的n点，寻找新的Target

carve(1,1)#起点

maze[1][0] = PATH 
maze[HEIGHT-2][WIDTH-1] = PATH #强制开通开口出口

def can_convert_wall(x,y):
    if maze[x][y] != WALL:
        return False