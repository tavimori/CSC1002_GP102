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
    #To Guest team: complete this function. DO NOT change the function name, so that mazer.py can call it.


def KeyDown(self):
    #To Guest team: complete this function. DO NOT change the function name, so that mazer.py can call it.


def KeyLeft(self):
    #To Guest team: complete this function. DO NOT change the function name, so that mazer.py can call it.


def KeyRight(self):
    #To Guest team: complete this function. DO NOT change the function name, so that mazer.py can call it.


#To Guest team: write your coding in the part below.















