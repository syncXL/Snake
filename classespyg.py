import pygame,math
import matplotlib.pyplot as plt
colors = {
    'darkBlue' : (10,10,34),
    'red' : (236,28,36),
    'white' : (230,227,220),
    'darkWhite' : (195,195,195)
}
def getCenter(coord,dist):
        x = ((2 * coord[0])+dist[0])/2
        y = ((2 * coord[1]) + dist[1])/2
        return (x,y)
def detectCollision(mainObj,obj2,minDist):
    for i in range(len(obj2)):
        if len(minDist)>1:
            if getDist(mainObj,obj2[i])<minDist[i]:
                return True
        else:
            if getDist(mainObj,obj2[i])<minDist[0]:
                return True
    return False

def inRange(val,val1,minDist):
    distX = abs(val1[0] - val[0])
    distY = abs(val1[1]-val[1])
    if distX < minDist[0] and distY < minDist[1]:
        return True
    return False

def returnCollided(mainObj,obj2,minDist):
    collidedInd = []
    for i in range(len(obj2)):
        if len(minDist)>1:
            if getDist(mainObj,obj2[i])<minDist[i]:
                collidedInd.append(i)
        else:
            if getDist(mainObj,obj2[i])<minDist[0]:
                collidedInd.append(i)
    return collidedInd

def getDist(coord1,coord2):
    x = (coord2[0] - coord1[0])**2
    y = (coord2[1] - coord1[1])**2
    return math.sqrt(x+y)

def bfs(points,changeGrid,checkBool,width,height):
    for i in points:
        if  checkBool[i]:
            if i[0] < (width-changeGrid[0]):
                newGrid = (i[0]+changeGrid[0],i[1])
                if newGrid not in checkBool.keys():
                    points.append(newGrid)
                    checkBool[newGrid] = True
            if i[1] < (height-changeGrid[1]):
                newGrid = (i[0],i[1]+changeGrid[1])
                if newGrid not in checkBool.keys():
                    points.append(newGrid)
                    checkBool[newGrid] =True

class Background():
    def __init__(self,dir,width,height,screen):
        self.position = [(0,0)]
        self.visited = {
            (0,0) : True
        }
        self.backgroundImage = pygame.image.load(dir)
        self.objSize = self.backgroundImage.get_size()
        bfs(self.position,self.objSize,self.visited,width,height)
        self.screen = screen
    def display(self):
        for i in self.position:
            self.screen.blit(self.backgroundImage,i)

class Text():
    def __init__(self,fStyle,size,text,color,coord,screen):
        self.fontObj = pygame.font.Font(fStyle,size)
        self.text = text
        self.textObj = self.fontObj.render(text,False,color[0])
        self.color = color
        self.coord = coord
        self.textsize = size
        self.size = self.textObj.get_size()
        self.screen = screen
        self.centerPoint= getCenter(self.coord,self.size)
        self.highlighted = False
    def spawn(self):
        self.checkHighlight()
        self.screen.blit(self.textObj,self.coord)
    def chText(self,newText):
        self.text = newText
        self.border= getCenter(self.coord,self.textObj.get_size())
    def checkHighlight(self):
        if self.highlighted:
            self.textObj = self.fontObj.render(self.text,False,self.color[0],self.color[1])
        else:
            self.textObj = self.fontObj.render(self.text,False,self.color[0])
class ListText:
    def __init__(self,textObjs,commands,highlightable):
        self.textObjs = textObjs
        self.Htext = list()
        self.filterHighlight(highlightable)
        self.commands = commands
        self.highlightedOne = 0
        self.highlightOne(0)
        self.entered = None
        self.mode = False
    def spawn(self):
        for i in self.textObjs:
            i.spawn()
    def filterHighlight(self,values):
        for i,j in zip(values,self.textObjs):
            if i:
                self.Htext.append(j)
    def highlightOne(self,ind):
        if ind <0:
            ind = 0
        elif ind > len(self.Htext)-1:
            ind = len(self.Htext)-1
            
        self.Htext[ind].highlighted= True
        self.highlightedOne = ind
        for i in range(len(self.Htext)):
            if i !=ind:
                self.Htext[i].highlighted = False
    def highlight(self,mpos,vel):
        if vel == (0,0):
            self.mode = True
        else:
            self.mode = False
        if not self.mode:
            for i,j in enumerate(self.Htext):
                halfPos = (j.size[0]/2,j.size[1]/2)
                if inRange(mpos,j.centerPoint,halfPos):
                    self.highlightOne(i)
                    break
    def runHighlighted(self):
        if self.entered != None:
            self.commands[self.textObjs.index(self.Htext[self.highlightedOne])]()
            self.entered = None
    def controls(self,events_in):
        keys = [pygame.K_UP,pygame.K_DOWN]
        actions = [-1,1]
        if events_in.key in keys:
            self.mode = True
            self.highlightOne(self.highlightedOne+actions[keys.index(events_in.key)])
        elif events_in.key == pygame.K_RETURN:
            self.entered = self.highlightedOne



def createFPSGraph(frames):
    second = list(range(1,len(frames)+1))
    plt.plot(second,frames)
    plt.xlabel('Seconds')
    plt.ylabel('Frames')
    plt.title('Visualization Of FPS')
    plt.show()


