import random

def difficultSetup():
    difficulty = int(input("Choose your difficulty(1~5)"))
    return difficulty

difficulty = difficultSetup()
WIDTH, HEIGHT = (difficulty * 10 + 1), (difficulty * 6 + 5)

WALL, PATH = 0, 1

wall = [[WALL for _ in range(WIDTH)] for _ in range(HEIGHT)]