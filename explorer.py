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


# TODO: Add a maze scorer, structurelize the maze with nodes, then find the most rational path, than give the score.
# TODO: Universal path finder.
def key_event(key):
    log('[{}] - Key event detected.'.format(key))
    LoadMaze()
    ReadCurrentPosition()
    global currentPosition
    # currentPosition = (currentPosition[0], currentPosition[1]+1)
    global apex25_done, apex25_p
    if not apex25_done:
        log('No known path found.')
        log('Alpha explorer start...')
        apex25_p = alpha_explorer(maze)
        log(apex25_p.__repr__())
        log('Alpha explorer done.')
    else:
        log('Follow Alpha explorer path.')
    currentPosition = apex25_p[1]
    apex25_p.pop(1)
    WriteExplorerPath()

def log(text):
    print('In Explorer: {}'.format(text))


def alpha_explorer(maze1):
    import pickle
    import math
    import copy
    from functools import reduce

    # global MRP1, MRP2, MRP3, MRPPA1, MRPPA2, MRPPA3, MAZE, START, GOAL, PATH
    apex25_STATUS_BLANK = 0
    apex25_STATUS_BRICK = 1
    apex25_STATUS_START = 2
    apex25_STATUS_GOAL = 3
    apex25_WIDTH = 12
    apex25_HEIGHT = 12
    apex25_UP = -apex25_WIDTH
    apex25_DOWN = apex25_WIDTH
    apex25_LEFT = -1
    apex25_RIGHT = 1
    apex25_BLANK_POSITION = list()
    apex25_BRICK_POSITION = list()
    apex25_START = int()
    apex25_GOAL = int()
    apex25_PATH = list()
    apex25_MRP1 = math.inf
    apex25_MRP2 = 0
    apex25_MRP3 = math.inf
    apex25_MRPPA1 = list()
    apex25_MRPPA2 = list()
    apex25_MRPPA3 = list()
    apex25_MAZE = list()
    apex25_single_path = list()

    apex25_MAZE = reduce(lambda x, y: x + y, maze1)
    # apex25_MAZE[70] = apex25_STATUS_BLANK
    # TODO Delete it
    for i, status in enumerate(apex25_MAZE):
        if status == apex25_STATUS_START:
            apex25_START = i
            # print('Start point is ({}).'.format(START.__repr__()))
            # MAZE[i] = 0
        elif status == apex25_STATUS_GOAL:
            apex25_GOAL = i
            # print('End point is ({}).'.format(GOAL.__repr__()))
        elif status == apex25_STATUS_BLANK:
            apex25_BLANK_POSITION.append(i)
        elif status == apex25_STATUS_BRICK:
            apex25_BRICK_POSITION.append(i)

    def get_coordinate(index):
        nonlocal apex25_WIDTH
        return divmod(index, apex25_WIDTH)

    def find_path(i=apex25_START, not_in=-1, clear=False):
        nonlocal apex25_PATH, apex25_single_path
        if clear:
            apex25_PATH = list()
            apex25_single_path = list()
        apex25_single_path.append(i)
        if i == not_in:
            pass
        elif i == apex25_GOAL:
            apex25_PATH.append(copy.copy(apex25_single_path))
        else:
            if apex25_MAZE[i + apex25_UP] != apex25_STATUS_BRICK and ((i + apex25_UP) not in apex25_single_path):
                find_path(i=i + apex25_UP, not_in=not_in)
                apex25_single_path.pop()
            if apex25_MAZE[i + apex25_DOWN] != apex25_STATUS_BRICK and ((i + apex25_DOWN) not in apex25_single_path):
                find_path(i=i + apex25_DOWN, not_in=not_in)
                apex25_single_path.pop()
            if apex25_MAZE[i + apex25_LEFT] != apex25_STATUS_BRICK and ((i + apex25_LEFT) not in apex25_single_path):
                find_path(i=i + apex25_LEFT, not_in=not_in)
                apex25_single_path.pop()
            if apex25_MAZE[i + apex25_RIGHT] != apex25_STATUS_BRICK and ((i + apex25_RIGHT) not in apex25_single_path):
                find_path(i=i + apex25_RIGHT, not_in=not_in)
                apex25_single_path.pop()
    find_path(clear=True)
    raw_path = copy.deepcopy(apex25_PATH)
    apex25_MRP3 = math.inf
    for i in raw_path:
        # find the lowest 2 to 3
        j_max = len(i)-1
        apex25_MRP2 = 0
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
            apex25_MRP1 = math.inf
            apex25_MRPPA1 = list()
            if len(apex25_PATH) != 0:
                for l in apex25_PATH:
                    # find the lowest p to 1
                    if len(l) < apex25_MRP1:
                        apex25_MRP1 = len(l)
                        apex25_MRPPA1 = l
            if apex25_MRP2 < j + apex25_MRP1 and (apex25_MRP1 < math.inf):
                apex25_MRP2 = j + apex25_MRP1
                # print('Brick at', str(j), 'remain steps', str(MRP1))
                apex25_MRPPA2 = i[:j] + copy.deepcopy(apex25_MRPPA1)
        if apex25_MRP3 > apex25_MRP2 and (apex25_MRP2 != 0):
            apex25_MRP3 = apex25_MRP2
            apex25_MRPPA3 = copy.deepcopy(apex25_MRPPA2)
        apex25_MRP3 -= 1
        # apex25_MRPPA3 = apex25_MRPPA3[1:]
    # Remove the first place
    print('MRP{}\tESC{}\tSTA{}\t'.format(str(apex25_MRP3), str(apex25_MRP3-len(apex25_BRICK_POSITION)+44),
                                         str(apex25_MRP3-len(apex25_BRICK_POSITION)-1+85)))
    global apex25_done
    apex25_done = True
    return list(map(lambda x: get_coordinate(x), apex25_MRPPA3))


def main():
    log('The module is running independently.')


def explorer():
    log('The module is called from mazer.')


if __name__ == '__main__':
    main()
elif __name__ == 'explorer':
    explorer()
    global apex25_done
    apex25_done = False








