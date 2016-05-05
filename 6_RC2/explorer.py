import pickle

#Use the following global variables to enable the pre-provided functions
'''Actually, you do not need to declare the global variables below here. You can either declare
them in the functions where it is assgined, or directly use these variables when assigning
them values in your main script.
The declaration is presented here only for better understanding of the coding.
'''

global maze #maze contains the maze information loaded from your original secret maze file,
            #identical to the maze information written to mazeFile.pkl, and changed when
            #the additional brick is added. It contains values:
            #0: empty block which is not explored
            #1: brick
            #2: START or the current position
            #3: GOAL
global currentPosition #This is the current position
global path #The previous path trajectory stored in explorerPath.pkl
global START, GOAL #The START and GOAL positions



#(1) File read: when keyboard event is activated, load maze
def LoadMaze():
    'Load the maze information into the global variable maze.'
    global maze, START, GOAL
    file=open('mazeFile.pkl','rb')
    maze=pickle.load(file)
    file.close()
    for i in range(len(maze)):
        if 2 in maze[i]:
            START=(i, maze[i].index(2))
        if 3 in maze[i]:
            GOAL=(i, maze[i].index(3))


#(2) File read: load path and get current position
def ReadCurrentPosition():
    '''Get the previous stored path from explorerPath.pkl and put it to the global variable path.
Extract out the current position and put it in the global variable currentPosition.
Call this function when needed.'''
    global path, currentPosition
    file=open('explorerPath.pkl','rb')
    path=pickle.load(file)
    currentPosition=path[len(path)-1]
    file.close()

#(3) File read & write: load last path and store the new path
def WriteExplorerPath():
    file=open('explorerPath.pkl','rb')
    path=pickle.load(file)
    file.close()
    file=open('explorerPath.pkl','wb')
    path.append(currentPosition)
    pickle.dump(path,file)
    file.close()



#To Guest team: complete these functions. DO NOT change the function names. Otherwise, mazer.py can not call them.

def KeyUp(self):
    key_event('UP')
    #To Guest team: complete this function. DO NOT change the function name, so that mazer.py can call it.


def KeyDown(self):
    key_event('DOWN')
    #To Guest team: complete this function. DO NOT change the function name, so that mazer.py can call it.


def KeyLeft(self):
    key_event('LEFT')
    #To Guest team: complete this function. DO NOT change the function name, so that mazer.py can call it.


def KeyRight(self):
    key_event('RIGHT')
    #To Guest team: complete this function. DO NOT change the function name, so that mazer.py can call it.


#To Guest team: write your coding in the part below.

def have_a_try(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            log('[ERROR] There is no path from the start to goal')
    return wrapper


# @have_a_try
def key_event(key):
    log('[{}] - Key event detected.'.format(key))
    LoadMaze()
    ReadCurrentPosition()
    global apex24_raw_maze, apex24_is_added
    global AE_done, AE_p, AE_MRP3_C
    # Path forming
    if currentPosition == GOAL:
        log('[System] Success')
    else:
        if maze != apex24_raw_maze:
            log('[MAZE] New maze file detected.')
            if len(apex24_raw_maze) == 0:
                apex24_raw_maze = maze
                log('[MAZE] Maze has been stored in explorer.')
            else:
                apex24_is_added = True
                AE_done = False
                apex24_raw_maze = maze
                log('[MAZE] Maze change find. Updated.')
        global currentPosition
        if not AE_done:
            log('[AE] No known path found.')
            log('[AE] Alpha explorer start...')
            AE_p = alpha_explorer(maze, brick_added=apex24_is_added)
            log('[AE] The most rational path is ' + AE_p.__repr__())

            log('[AE] Alpha explorer done.')
        else:
            log('[AE] Follow Alpha explorer path.')

        if AE_MRP3_C == 0:
            AE_p = alpha_explorer(maze, brick_added=True)

        currentPosition = AE_p[1]
        AE_MRP3_C -= 1
        AE_p.pop(1)
        WriteExplorerPath()


def log(text):
    print('In Explorer: {}'.format(text))


def alpha_explorer(maze1, brick_added=False):
    import pickle
    import math
    import copy
    from functools import reduce

    AE_STATUS_BLANK = 0
    AE_STATUS_BRICK = 1
    AE_STATUS_START = 2
    AE_STATUS_GOAL = 3
    AE_WIDTH = 12
    AE_HEIGHT = 12
    AE_UP = -AE_WIDTH
    AE_DOWN = AE_WIDTH
    AE_LEFT = -1
    AE_RIGHT = 1
    AE_BLANK_POSITION = list()
    AE_BRICK_POSITION = list()
    AE_START = int()
    AE_GOAL = int()
    AE_PATH = list()
    AE_MRP1 = math.inf
    AE_MRP2 = 0
    AE_MRP3 = math.inf
    AE_MRPPA1 = list()
    AE_MRPPA2 = list()
    AE_MRPPA3 = list()
    AE_MAZE = list()
    AE_single_path = list()
    AE_MAZE = reduce(lambda x, y: x + y, maze1)

    for i, status in enumerate(AE_MAZE):  # Loading maze and store critical points.
        if status == AE_STATUS_START:
            AE_START = i
        elif status == AE_STATUS_GOAL:
            AE_GOAL = i
        elif status == AE_STATUS_BLANK:
            AE_BLANK_POSITION.append(i)
        elif status == AE_STATUS_BRICK:
            AE_BRICK_POSITION.append(i)

    def get_coordinate(index):
        nonlocal AE_WIDTH
        return divmod(index, AE_WIDTH)

    def get_index(coordinate):
        nonlocal AE_WIDTH
        return coordinate[0] * AE_WIDTH + coordinate[1]

    def find_path(i=AE_START, not_in=-1, clear=False):
        nonlocal AE_PATH, AE_single_path
        if clear:
            AE_PATH = list()
            AE_single_path = list()
        AE_single_path.append(i)
        if i == not_in:
            pass
        elif i == AE_GOAL:
            AE_PATH.append(copy.copy(AE_single_path))
        else:
            if AE_MAZE[i + AE_UP] != AE_STATUS_BRICK and ((i + AE_UP) not in AE_single_path):
                find_path(i=i + AE_UP, not_in=not_in)
                AE_single_path.pop()
            if AE_MAZE[i + AE_DOWN] != AE_STATUS_BRICK and ((i + AE_DOWN) not in AE_single_path):
                find_path(i=i + AE_DOWN, not_in=not_in)
                AE_single_path.pop()
            if AE_MAZE[i + AE_LEFT] != AE_STATUS_BRICK and ((i + AE_LEFT) not in AE_single_path):
                find_path(i=i + AE_LEFT, not_in=not_in)
                AE_single_path.pop()
            if AE_MAZE[i + AE_RIGHT] != AE_STATUS_BRICK and ((i + AE_RIGHT) not in AE_single_path):
                find_path(i=i + AE_RIGHT, not_in=not_in)
                AE_single_path.pop()

    if not brick_added:
        find_path(clear=True)
        raw_path = copy.deepcopy(AE_PATH)
        AE_MRP3 = math.inf  # The length of the most rational path.
        for i in raw_path:
            # find the lowest 2 to 3
            j_max = len(i)-1
            AE_MRP2 = 0  # The length of the most rational path by going along a certain path.
            # AE_MRP1_critical = -1
            for j, k in enumerate(i):
                # find the highest 1 to 2
                if j == 0:
                    # Put the Brick just next to the start
                    continue
                if j == j_max:
                    # Put the Brick at which will cause an index error
                    continue
                find_path(i=k, not_in=i[j+1], clear=True)
                AE_MRP1 = math.inf  # The shortest path under the additional brick placed at i[j+1]

                AE_MRPPA1 = list()
                if len(AE_PATH) != 0:
                    for l in AE_PATH:
                        # find the lowest p to 1
                        if len(l) < AE_MRP1:
                            AE_MRP1 = len(l)
                            AE_MRPPA1 = l
                            # AE_MRP1_critical = len(AE_MRPPA1)
                if AE_MRP2 < j + AE_MRP1 and (AE_MRP1 < math.inf):
                    AE_MRP2 = j + AE_MRP1
                    AE_MRP2_C = j
                    AE_MRPPA2 = i[:j] + copy.deepcopy(AE_MRPPA1)
            if AE_MRP3 > AE_MRP2 and (AE_MRP2 != 0):
                AE_MRP3 = AE_MRP2
                global AE_MRP3_C
                AE_MRP3_C = AE_MRP2_C
                AE_MRPPA3 = copy.deepcopy(AE_MRPPA2)
        AE_MRP3 -= 1  # Remove the first place
        log('[AE] Evaluation is over: MRP[{}]\tESC[{}]\tSTA[{}]\t'.format(
            str(AE_MRP3),
            str(AE_MRP3-len(AE_BRICK_POSITION)+44),
            str(AE_MRP3-len(AE_BRICK_POSITION)-1+85)))
        log('[AE] Critical point at %s' % str(AE_MRP3_C))
    elif brick_added:
        global currentPosition
        find_path(i=get_index(currentPosition), clear=True)
        AE_MRPPA3 = AE_PATH[0]
        for i in AE_PATH:
            if len(AE_MRPPA3) > len(i):
                AE_MRPPA3 = i
        log('[AE] PATH: {}'.format(AE_MRPPA3.__repr__()))

    global AE_done
    AE_done = True

    return list(map(lambda x: get_coordinate(x), AE_MRPPA3))


def main():
    log('The module is running independently.')


def explorer():
    log('[MODULE] The module is imported from mazer.')
    global apex24_raw_maze, apex24_is_added
    global AE_done
    AE_done = False
    apex24_raw_maze = list()
    apex24_is_added = False
    log('[MODULE] The var for raw maze initialized.')
    global AE_MRP3_C
    AE_MRP1_C = -1


if __name__ == '__main__':
    main()
elif __name__ == 'explorer':
    explorer()
