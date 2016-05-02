import pickle
from tkinter import *

counting=0

def draw():
    global num,nums,showBricks
    if element == 1:
        showBricks.append(Label(root, bg="black", fg="white"))
        showBricks[nums].place(x=nums * 50, y=num * 50, width=50, height=50)
    elif element == 0:
        showBricks.append(Label(root, bg="white", fg="black"))
        showBricks[nums].place(x=nums * 50, y=num * 50, width=50, height=50)
    elif element == 3:
        showBricks.append(Label(root, bg="blue"))
        showBricks[nums].place(x=nums * 50, y=num * 50, width=50, height=50)
    elif element == 2:
        showBricks.append(Label(root))
        showBricks[nums].place(x=nums * 50, y=num * 50, width=50, height=50)
        myImage = PhotoImage(file="car.PGM")
        showBricks[nums].configure(image=myImage)
        showBricks[nums].photo = myImage
    elif element == 4:
        showBricks.append(Label(root, bg="blue",fg="white",text=counting))
        showBricks[nums].place(x=nums * 50, y=num * 50, width=50, height=50)

def LoadMazeFile():
    global maze,START, GOAL
    file=open("mazeList.pkl","rb")
    maze=pickle.load(file)
    file.close()
    for i in range(len(maze)):
        if 2 in maze[i]:
            START=(i,maze[i].index(2))
        if 3 in maze[i]:
            GOAL=(i,maze[i].index(3))
def InitializeExplorerPath():
    file=open("explorerPath.pk1","wb")
    pickle.dump([START],file)
    print('In Mazer : explorerPath.pkl initialized')
    file.close()
def Initialization():
    LoadMazeFile()
    InitializeExplorerPath()

Initialization()
def WriteMazeFile():
    file=open("mazefile.pkl","wb")
    pickle.dump(maze,file)
    file.close()
def CreateTempMaze():
    global tempMaze
    file=open("mazeList.pkl","rb")
    tempMaze=pickle.load(file)
    file.close()

def CommunicationMazerExplorer():
    global currentPosition, path, counting
    previousPosition=currentPosition
    ReadCurrentPosition()
    labelCurrentPositionExplorer.configure(justify=CENTER,text="In Explorer: \ncurrentPosition=(%s,%s")%(currentPosition[0],currentPosition[1])
    if currentPosition!=previousPosition:
        counting+=1
        UpdateGUI(previousPosition,currentPosition)
    root.after(100,CommunicationMazerExplorer)
def ReadCurrentPosition():
    global currentPosition, path
    path=pickle.load("explorerPath.pk1","rb")
    currentPosition=path[len(path)-1]
    path.close()
def ReDraw():
    num = 0
    for i in tempMaze:
        num += 1
        nums = -1
        for element in i:
            nums += 1
            draw()
def UpdateGUI(previousPosition, currentPosition):
    tempMaze[previousPosition[0]][previousPosition[1]]=4
    tempMaze[currentPosition[0]][currentPosition[1]]=2
    ReDraw()

def CountBricks():
    brickNumer=0
    for mazeRow in maze:
        brickNumer+=mazeRow.count(1)
    return brickNumer

def Click_0_0(i,element):
    wholeBricks[i][element].configure(bg="black")

root=Tk()
root.geometry('600x650')
root.title('Maze')
showLabel1=Label(root,bg="blue",fg="black",text="In Maze: \ncurrentPosition=(%s,%s")%(currentPosition[0],currentPosition[1]).place(x=0,y=0,width=200,height=50)
showLabel2=Label(root,bg="blue",fg="black",text="Brick.#:\n%s"%(CountBricks())).place(x=200,y=0,width=200,height=50)
labelCurrentPositionExplorer=Label(root,bg="blue",fg="black").place(x=400,y=0,width=200,height=50)
num=0
wholeBricks=[]
for i in maze:
    showBricks=[]
    num+=1
    nums=-1
    for element in i:
        nums+=1
        draw()
    wholeBricks.append(showBricks)
for i in range(12):
    for j in range(12):
        exec('def Click_%s_%s(event):\n\tlabelArray[%s][%s].configure(bg=\'white\')\n\tmaze[%s][%s]=1'%(i,j,i,j,i,j))
        if maze[i][j]==0:
            exec('labelArray[%s][%s].bind(\'<Button-1>\',Click_%s_%s)'%(i,j,i,j))

CommunicationMazerExplorer()
