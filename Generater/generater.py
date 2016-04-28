# TODO: generate mazes by algorithm.
# TODO: real time evaluation.
import time
import pickle
import math
import copy
file = open('mazeFileForTest.pkl', 'rb')
raw_maze = pickle.load(file)
file.close()
maze = copy.deepcopy(raw_maze)
blank_position = list()
UPPER_BOUND = 100
STATUS_BLANK = 0
STATUS_BRICK = 1
STATUS_START = 2
STATUS_GOAL = 3
MRP = math.inf
MRPH = 0
ADDED_BRICK = (-1, -1)
print('pickle done', time.clock())
for i, row in enumerate(raw_maze):
    for j, status in enumerate(row):
        if status == STATUS_START:
            print('Start point is ({},{}).'.format(str(i), str(j)))
            start = i, j
            maze[i][j] = 0
        elif status == STATUS_GOAL:
            print('End point is ({},{}).'.format(str(i), str(j)))
            goal = i, j
            maze[i][j] = UPPER_BOUND
        elif status == STATUS_BLANK:
            maze[i][j] = UPPER_BOUND
            blank_position.append((i, j))
        elif status == STATUS_BRICK:
            maze[i][j] = math.inf
# print('The start point is {}, the goal is {}.'.format(start.__repr__(), goal.__repr__()))
print('scan done', time.clock())


def print_maze(abc, b=True):
    def t(i):
        if i < math.inf:
            return ''
        else:
            return 'inf'
    if b:
        print('\n'.join(['\t'.join([t(j) for j in i]) for i in abc]))
    else:
        print('\n'.join(['\t'.join([j.__repr__() for j in i]) for i in abc]))


def min_step(i, j):
    global maze
    if maze[i-1][j] < math.inf and (maze[i-1][j] > maze[i][j]+1):
        maze[i-1][j] = maze[i][j] + 1
        min_step(i-1, j)
    if maze[i][j+1] < math.inf and (maze[i][j+1] > maze[i][j] + 1):
        maze[i][j+1] = maze[i][j] + 1
        min_step(i, j+1)
    if maze[i+1][j] < math.inf and (maze[i+1][j] > maze[i][j] + 1):
        maze[i+1][j] = maze[i][j] + 1
        min_step(i+1, j)
    if maze[i][j-1] < math.inf and (maze[i][j-1] > maze[i][j] + 1):
        maze[i][j-1] = maze[i][j] + 1
        min_step(i, j-1)


def refresh_step():
    for i, row in enumerate(maze):
        for j, status in enumerate(row):
            if status != math.inf:
                maze[i][j] = UPPER_BOUND

init_maze = copy.deepcopy(maze)
init_maze[start[0]][start[1]] = UPPER_BOUND
# all upper copy
min_step(*start)
# print_maze(maze, b=False)
# print_maze(maze)
first_half_maze = copy.deepcopy(maze)
# first layer try
fhm = first_half_maze
maze = copy.deepcopy(init_maze)
print('start search', time.clock())
for p_previous in blank_position:
    step_first_half = first_half_maze[p_previous[0]][p_previous[1]]
    MRPH = 0
    for p_add_brick in blank_position:
        if p_add_brick == p_previous:
            continue
        # maze = copy.deepcopy(init_maze)
        maze[p_add_brick[0]][p_add_brick[1]] = math.inf
        maze[p_previous[0]][p_previous[1]] = step_first_half
        min_step(*p_previous)
        if MRPH < maze[goal[0]][goal[1]] < UPPER_BOUND:
            # print(p_previous.__repr__(), p_add_brick.__repr__())
            MRPH = maze[goal[0]][goal[1]]
        maze[p_add_brick[0]][p_add_brick[1]] = UPPER_BOUND
        refresh_step()
    if MRP > MRPH:
        MRP = MRPH
print('search done', time.clock())
# print('The brick will be added on {}'.format(ADDED_BRICK.__repr__()))
print('The MRP is {}'.format(str(MRP)))
# print('\n'.join(['\t'.join([j.__repr__() for j in i]) for i in init_maze]))
# print('\n')
# print('The closest way from start to goal need {} steps'.format(maze[goal[0]][goal[1]]))

