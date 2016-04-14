# TODO: generate mazes by algorithm.
# TODO: real time evaluation.

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
MRP = -1
ADDED_BRICK = (-1, -1)
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
print('The start point is {}, the goal is {}.'.format(start.__repr__(), goal.__repr__()))


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


init_maze = copy.deepcopy(maze)
init_maze[start[0]][start[1]] = UPPER_BOUND
# all upper copy
min_step(*start)
print_maze(maze, b=False)
print_maze(maze)
first_half_maze = copy.deepcopy(maze)
# first layer try
fhm = first_half_maze
for possible_added_brick in blank_position:
    # maze = copy.deepcopy(init_maze)
    # maze[possible_added_brick[0]][possible_added_brick[1]] = STATUS_GOAL
    # maze[goal[0]][goal[1]] = STATUS_BLANK
    # min_step(*start)
    step_first_half = first_half_maze[possible_added_brick[0]][possible_added_brick[1]]-1
    previous_position = list()
    if fhm[possible_added_brick[0]-1][possible_added_brick[1]] == step_first_half:
        previous_position.append((possible_added_brick[0]-1, possible_added_brick[1]))
    if fhm[possible_added_brick[0]][possible_added_brick[1]+1] == step_first_half:
        previous_position.append((possible_added_brick[0], possible_added_brick[1]+1))
    if fhm[possible_added_brick[0]+1][possible_added_brick[1]] == step_first_half:
        previous_position.append((possible_added_brick[0]+1, possible_added_brick[1]))
    if fhm[possible_added_brick[0]][possible_added_brick[1]-1] == step_first_half:
        previous_position.append((possible_added_brick[0], possible_added_brick[1]-1))
    print('Brick at {}, {} previous. half{}'.format(possible_added_brick.__repr__(), len(previous_position), step_first_half))
    for single_previous_position in previous_position:
        maze = copy.deepcopy(first_half_maze)
        maze[single_previous_position[0]][single_previous_position[1]] = -UPPER_BOUND
        min_step(*single_previous_position)
        print(maze[goal[0]][goal[1]] + step_first_half + UPPER_BOUND)
        if MRP < maze[goal[0]][goal[1]] + step_first_half + UPPER_BOUND:
            MRP = maze[goal[0]][goal[1]] + step_first_half + UPPER_BOUND
            ADDED_BRICK = possible_added_brick

print('The brick will be added on {}'.format(ADDED_BRICK.__repr__()))
print('The MRP is {}'.format(str(MRP)))
print('\n'.join(['\t'.join([j.__repr__() for j in i]) for i in init_maze]))
print('\n')
print('The closest way from start to goal need {} steps'.format(maze[goal[0]][goal[1]]))

