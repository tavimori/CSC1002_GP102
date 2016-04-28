import pickle
import math
import copy
from functools import reduce

# TODO: USE recursion to find mrp.
def check(maze1):
    global MRP1, MRP2, MRP3, MRPPA1, MRPPA2, MRPPA3, MAZE, START, GOAL, PATH
    UPPER_BOUND = 100
    STATUS_BLANK = 0
    STATUS_BRICK = 1
    STATUS_START = 2
    STATUS_GOAL = 3
    WIDTH = 12
    HEIGHT = 12
    UP = -WIDTH
    DOWN = WIDTH
    LEFT = -1
    RIGHT = 1
    BLANK_POSITION = list()
    BRICK_POSITION = list()
    START = int()
    GOAL = int()
    PATH = list()
    MRP1 = math.inf
    MRP2 = 0
    MRP3 = math.inf
    MRPPA1 = list()
    MRPPA2 = list()
    MRPPA3 = list()
    MAZE = list()
    single_path = list()
    MAZE = reduce(lambda x, y: x + y, maze1)
    # MAZE[70] = STATUS_BLANK
    # TODO Delete it
    for i, status in enumerate(MAZE):
        if status == STATUS_START:
            START = i
            # print('Start point is ({}).'.format(START.__repr__()))
            # MAZE[i] = 0
        elif status == STATUS_GOAL:
            GOAL = i
            # print('End point is ({}).'.format(GOAL.__repr__()))
            # MAZE[i] = UPPER_BOUND
        elif status == STATUS_BLANK:
            # MAZE[i] = UPPER_BOUND
            BLANK_POSITION.append(i)
        elif status == STATUS_BRICK:
            BRICK_POSITION.append(i)

    def get_coordinate(index):
        global WIDTH
        return divmod(index, WIDTH)

    def find_path(i=START, not_in=-1, clear=False):
        global PATH, single_path
        if clear:
            PATH = list()
            single_path = list()
        single_path.append(i)
        if i == not_in:
            pass
        elif i == GOAL:
            PATH.append(copy.copy(single_path))
        else:
            if MAZE[i + UP] != STATUS_BRICK and ((i + UP) not in single_path):
                find_path(i=i + UP, not_in=not_in)
                single_path.pop()
            if MAZE[i + DOWN] != STATUS_BRICK and ((i + DOWN) not in single_path):
                find_path(i=i + DOWN, not_in=not_in)
                single_path.pop()
            if MAZE[i + LEFT] != STATUS_BRICK and ((i + LEFT) not in single_path):
                find_path(i=i + LEFT, not_in=not_in)
                single_path.pop()
            if MAZE[i + RIGHT] != STATUS_BRICK and ((i + RIGHT) not in single_path):
                find_path(i=i + RIGHT, not_in=not_in)
                single_path.pop()
    find_path(clear=True)
    raw_path = copy.deepcopy(PATH)
    MRP3 = math.inf
    for i in raw_path:
        # find the lowest 2 to 3
        j_max = len(i)-1
        MRP2 = 0
        for j, k in enumerate(i):
            # find the highest 1 to 2
            if j == 0:
                # Put the Brick just next to the start
                continue
            if j == j_max:
                # Put the Brick at which will cause an index error
                continue
            find_path(i=k, not_in=i[j+1], clear=True)
            # The shortest path under the additional brick placed at i[j+1]
            MRP1 = math.inf
            MRPPA1 = list()
            if len(PATH) != 0:
                for l in PATH:
                    # find the lowest p to 1
                    if len(l) < MRP1:
                        MRP1 = len(l)
                        MRPPA1 = l
            if MRP2 < j + MRP1 and (MRP1 < math.inf):
                MRP2 = j + MRP1
                # print('Brick at', str(j), 'remain steps', str(MRP1))
                MRPPA2 = i[:j] + copy.deepcopy(MRPPA1)
        if MRP3 > MRP2 and (MRP2 != 0):
            MRP3 = MRP2
            MRPPA3 = copy.deepcopy(MRPPA2)
    MRP3 -= 1
    MRPPA3 = MRPPA3[1:]
    # Remove the first place
    print('MRP{}\tESC{}\tSTA{}\t'.format(str(MRP3), str(MRP3-len(BRICK_POSITION)+44), str(MRP3-len(BRICK_POSITION)-1+85)))
    return str(MRP3)


def print_maze(list1):
    a = '\n'.join([i.__repr__()[1:-1] for i in list1]).replace('1', '█').replace(' ', '').replace(',', '').replace('0', ' ')
    print(a)
    return a


def read_maze(str1):
    return str1.replace(' ', '0 ').replace('█', '1 ').replace(' \n', '\n')


def main():
    file = open('MAZEFileForTest.pkl', 'rb')
    raw_maze = pickle.load(file)
    file.close()

    file = open('output.txt', 'r')
    data = file.read()
    file.close()
    mazeList = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
                [1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1],
                [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1],
                [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1],
                [1, 2, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1],
                [1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1],
                [1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1],
                [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1],
                [1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1],
                [1, 0, 0, 0, 0, 1, 3, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]


    mazeList1 = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
                [1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1],
                [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1],
                [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1],
                [1, 2, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1],
                [1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1],
                [1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1],
                [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1],
                [1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1],
                [1, 0, 0, 0, 1, 3, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

    mazeList2 = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
                 [1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1],
                 [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1],
                 [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1],
                 [1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1],
                 [1, 3, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1],
                 [1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1],
                 [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1],
                 [1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1],
                 [1, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
    file = open('a.pkl', 'wb')
    pickle.dump(mazeList2, file)
    file.close()
    check(mazeList)
    check(mazeList1)
    check(mazeList2)
    # print_maze(mazeList2)
    a = data
    a = a.split('\n#\n')
    def f(str1):
        k = str1.split('\n')
        return list(map(g, k))
    def g(str2):
        v = str2.split(' ')
        return list(map(lambda x: int(x), v))
    c = list(map(f, a))
    for mmm in c:
        check(mmm)
    print('Done')


if __name__ == '__main__':
    main()





