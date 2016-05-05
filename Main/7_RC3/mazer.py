import pickle
from tkinter import *

import explorer #Import explorer as a module and call its functions later.

# Use these global variables to enable the pre-provided functions.

'''Actually, you do not need to declare the global variables below here. You can either declare
them in the functions where it is assgined, or directly use these variables when assigning
them values in your main script.
The declaration is presented here only for better understanding of the coding.
'''
global currentPosition #This is the current position
global root #Define your Tk object as root
global maze #maze contains the maze information loaded from your original secret maze file,
            #identical to the maze information written to mazeFile.pkl, and changed when
            #the additional brick is added. It contains values:
            #0: empty block which is not explored
            #1: brick
            #2: START or the current position
            #3: GOAL
global tempMaze #tempMaze contains the maze information with explored blocks. It will not be 
                #written to mazeFile.pkl for read by explorer.py. Its difference with maze is
                #only in the new value below:
                #4: the block is previously empty and has been explored.
global labelCurrentPositionExplorer #It is the Label object showing the current position in
                                    #explore.py. CommunicationMazerExplorer() will update it
                                    #and thus we make it global variable
global START, GOAL  #The START and GOAL positions. They can be located in any two distinct positions
                    #of the maze, except for the positions


#(0) File read: only in initialization
#The function below read from the secret path .pkl file.
#START and GOAL can be located in any two distinct positions of the maze, except for the positions
#on boundary.
def LoadMazeFile():
    'Load from the initial secret maze file, and extract START and GOAL.'
    global maze, START, GOAL
    file=open('afdefaa18a3656a99043d728d6fc87bb.pkl','rb')#For Host team: You can change to your .pkl file name.
    maze=pickle.load(file)
    file.close()
    for i in range(len(maze)):
        if 2 in maze[i]:
            START=(i, maze[i].index(2))
        if 3 in maze[i]:
            GOAL=(i, maze[i].index(3))
     

#(1) File write: only in initialization
#The functions below write the explorerPath.pkl for communication initialization with explorer.py.
#Just include it in the coding. You do not need to call it.

def InitializeExplorerPath():    
    'Initialize explorerPath.pkl for explorer.py.   mazer.py write explorerPath.pkl only this time.'
    file=open('explorerPath.pkl','wb') #Overwrite the previous path information.
    pickle.dump([START], file)
    print('In Mazer: explorerPath.pkl initialized.')
    file.close()


#Initialize by calling LoadMazeFile() and InitializeExplorerPath()
def Initialization():
    LoadMazeFile()  #Call LoadMazeFile() to read from the original secret path file.
    InitializeExplorerPath() #Call InitializeExplorerPath()
                             #to initialize explorerPath.pkl at the begining of your file.

Initialization()

#The function above read from the original secret path file, and the write to the explorerPath.pkl for
#communication initialization with explorer.py.
#Just include it in the coding. You do not need to call it again.




#(2) File write: in initialization
#(3) File write: when a new brick is added
#The function below is pre-provided for writing mazeFile.pkl.
#Call it at appropriate place to coordinate mazer.py to explorer.py communication.

def WriteMazeFile():
    'Write the global variable maze to mazeFile.pkl for explorer.py to read.'
    file=open('mazeFile.pkl','wb')
    pickle.dump(maze, file)
    file.close()

#The function above is pre-provided for writing mazeFile.pkl.
#Call it at appropriate place to coordinate mazer.py to explorer.py communication.




#(4) File read: every 0.1s approximately
#The functions below are pre-provided for read from explorerPath.pkl around every 0.1 second and update
#the global variable tempMaze and the GUI.
# -- ReadCurrentPosition(): read from explorerPath.pkl, and assign current position to the global variable 
#    currentPosition. It is called in CommunicationMazerExplorer().
# -- CommunicationMazerExplorer(): read from explorerPath.pkl around every 0.1 second, and if there is move 
#    to a new position, update the the global variable tempMaze and show it in the GUI.
# -- UpdateTempMaze(previousPosition, currentPosition): update the global variable tempMaze and show it in
#    the GUI. !!! There is still need to write a function ReDraw to update the GUI.

      
def CommunicationMazerExplorer():# Use this function before the root.mainloop()
    ''' This function checks the new current position from Explorer, updates the labelCurrentPositionExplorer in GUI,
stores the new current position in path, and updates the global variable tempMaze (ReDraw the GUI in function UpdateMaze()).
CommunicationMazerExplorer() will be called around every 100 mini seconds.
'''
    global currentPosition, path
    previousPosition=currentPosition
    ReadCurrentPosition()#The global currentPosition will be changed by the position information in explorerPath.pkl    

    labelCurrentPositionExplorer.configure(text='In Explorer: \ncurrentPosition=(%s,%s)'%(currentPosition[0],currentPosition[1]),
                                           justify=CENTER)
    #labelCurrentPositionExplorer shows the current position feedback from Explorer.

    if currentPosition!=previousPosition:
        UpdateGUI(previousPosition,currentPosition)
        #This function only updates tempMaze, rather than maze, which is changed only when you add a brick.
        
    root.after(100, CommunicationMazerExplorer)#CommunicationMazerExplorer() will be called every 100 ms.

def ReadCurrentPosition():
    '''Read the current position stored in currentPosition.pkl and assign to the global variable currentPosition.
After InitializeCommunicationFile(), only explorer.py can write currentPosition.pkl, and thus it is the latest current
position information after keyboard input. 
'''
    global currentPosition, path
    file=open('explorerPath.pkl','rb')
    path=pickle.load(file) 
    currentPosition=path[len(path)-1]
    file.close()
    
def UpdateGUI(previousPosition, currentPosition):
    '''Update the global varialble tempMaze, and then update GUI by ReDraw().
This function is called in CommunicationMazerExplorer().
You may not need to call it in your coding.'''
    tempMaze[previousPosition[0]][previousPosition[1]]=4
    tempMaze[currentPosition[0]][currentPosition[1]]=2
    ReDraw()    #For Host team: ReDraw will update the maze GUI. You need to write it. It does not need to return anything.




#The function below counts the number of bricks in the maze. Call it when needed.
    
def CountBricks():
    'It counts the brick number in the global variable maze, and return it.'
    brickNumber=0
    for mazeRow in maze:
        brickNumber+=mazeRow.count(1)# Add the number of 1s, i.e. bricks.
    return brickNumber

#The function above counts the number of bricks in the maze. Call it when needed.


#!!!Include the above code and use them in mazer.py. Do not modify it, unless instructed to do so.!!!


def ReDraw():
    image_car = PhotoImage(file="genius.gif")
    label_count_brick.configure(text='Brick #: \n%s' % str(CountBricks()))
    for i in range(12):
        for j in range(12):
            maze_label[i][j].configure(image='')
            if tempMaze[i][j] == 0:
                maze_label[i][j].configure(bg="white", fg="black")
            elif tempMaze[i][j] == 1:
                maze_label[i][j].configure(bg="black", fg="white")
            elif tempMaze[i][j] == 2:
                # image_car = PhotoImage(file='robot.gif')
                maze_label[i][j].configure(bg='yellow', image=image_car)
                maze_label[i][j].photo = image_car
                maze_label[i][j].configure(text='START')
            elif tempMaze[i][j] == 3:
                maze_label[i][j].configure(bg='SteelBlue1')
            elif tempMaze[i][j] == 4:
                maze_label[i][j].configure(bg="LightPink", fg="white", text='PATH')

    global path, label_mazer
    for i, j in enumerate(path[:-1]):
        maze_label[j[0]][j[1]].configure(bg="LightPink", fg="white", text='PATH')
        maze_label[j[0]][j[1]].configure(text=str(i))
    label_mazer.configure(text='In Mazer: \ncurrentPosition=%s' % currentPosition.__repr__())
    log('[GUI] Redraw successfully.')


def log(text):
    print('In Mazer: {}'.format(text))


def main():
    import copy
    global currentPosition, root, labelCurrentPositionExplorer, tempwindow, tempMaze, maze_label, label_mazer
    global label_count_brick
    ReadCurrentPosition()
    WriteMazeFile()
    tempMaze = maze
    currentPosition = START
    root = Tk()
    root.geometry('600x650')
    root.resizable(False, False)
    root.title('Maze')

    label_mazer = Label(root, text='In Mazer: \ncurrentPosition=%s' % currentPosition.__repr__())
    label_mazer.place(x=0, y=0, width=200, height=50)
    label_count_brick = Label(root, text='Brick #: \n  ')
    label_count_brick.place(x=200, y=0, width=200, height=50)
    labelCurrentPositionExplorer = Label(root, text='In Explorer: \ncurrentPosition=%s' % currentPosition.__repr__())
    labelCurrentPositionExplorer.place(x=400, y=0, width=200, height=50)
    maze_label = copy.deepcopy(maze)
    for i in range(12):
        for j in range(12):
            maze_label[i][j] = Label(root)
            maze_label[i][j].place(x=j*50, y=(i+1)*50, width=50, height=50)

            def brick_click(e, i=i, j=j):
                global maze, tempMaze
                if maze[i][j] == 0:
                    maze[i][j] = 1
                    tempMaze[i][j] = 1
                    WriteMazeFile()
                    ReDraw()
            maze_label[i][j].bind('<Button-1>', brick_click)
    log('[Init] Mouse click event initialized.')

    ReDraw()
    log('[Init] All set, initializing is over.')

if __name__ == '__main__':
    main()

#!!!Include the code below and use it in mazer.py.
        
root.bind("<KeyRelease-Up>", explorer.KeyUp)#To Host Team: We change the KeyPress event to KeyRelease event,
                                            #to prevent from continuous KeyPress. When the key is released from
                                            #the pressed state, the event will be activated.
root.bind("<KeyRelease-Down>", explorer.KeyDown)
root.bind("<KeyRelease-Left>", explorer.KeyLeft)
root.bind("<KeyRelease-Right>", explorer.KeyRight)
CommunicationMazerExplorer()

root.mainloop()
