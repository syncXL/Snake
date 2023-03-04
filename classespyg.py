import pygame,math
import matplotlib.pyplot as plt
colors = {
    'darkBlue' : (10,10,34),
    'red' : (236,28,36),
    'white' : (230,227,220),
    'darkWhite' : (195,195,195),
    'Violet' : (191,28,229),
    'turquoise' : (0,168,243),
    'blue+' : (51,101,123)
}
def placeCenter(maxVal,val):
    return int(maxVal/2 -val/2)
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
# def dispMultiple(screen,imgs,coords):
#     for i in range(len(imgs)):
#         screen.blit()
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
    def __init__(self,dir,width,height,screen,outlineThickness=10):
        self.position = [(0,0)]
        self.visited = {
            (0,0) : True
        }
        self.backgroundImage = pygame.image.load(dir)
        self.objSize = self.backgroundImage.get_size()
        bfs(self.position,self.objSize,self.visited,width,height)
        self.outline = pygame.Rect(0,0,width,height)
        self.outlineBool = False
        self.outlineThickness = outlineThickness
        self.screen = screen
    def display(self):
        for i in self.position:
            self.screen.blit(self.backgroundImage,i)
        if self.outlineBool:
            pygame.draw.rect(self.screen,colors['red'],self.outline,self.outlineThickness)
    def showoutline(self):
        self.outlineBool = not self.outlineBool

class Text():
    def __init__(self,fStyle,text,color,screen,anchor=False,coord = 0):
        self.fontObj = pygame.font.Font(fStyle[0],fStyle[1])
        self.text = text
        self.textObj = self.fontObj.render(self.text,False,color[0])
        self.color = color
        self.textsize = fStyle[1]
        self.size = self.textObj.get_size()
        self.screen = screen
        self.highlighted = False
        if coord != 0 and anchor:
            self.initCoord = coord
            self.coord = (placeCenter(coord[0],self.size[0]),coord[1])
        else:
            self.coord = coord
        self.anchor = anchor
        if coord != 0:
            self.centerPoint= getCenter(self.coord,self.size)
    def spawn(self,num=0):
        self.checkHighlight()
        if not num:
            self.screen.blit(self.textObj,self.coord)
        elif self.anchor and self.coord ==0:
            coord = (placeCenter(num[0],self.size[0]),num[1])
            self.centerPoint= getCenter(coord,self.size)
            self.screen.blit(self.textObj,coord)
        else:
            self.centerPoint= getCenter(num,self.size)
            self.screen.blit(self.textObj,num)
    def chText(self,newText):
        self.text = newText
        self.textObj = self.fontObj.render(self.text,False,self.color[0])
        self.border= getCenter(self.coord,self.textObj.get_size())
        if self.anchor:
            self.size = self.textObj.get_size()
            self.coord = (placeCenter(self.initCoord[0],self.size[0]),self.coord[1])

    def checkHighlight(self):
        if self.highlighted:
            self.textObj = self.fontObj.render(self.text,False,self.color[0],self.color[1])
        else:
            self.textObj = self.fontObj.render(self.text,False,self.color[0])
class ListText:
    def __init__(self,tStyle,items,color,screen,x,y,padding,commands=[],highlightable= True,anchor=True):
        self.tStyle = tStyle
        self.color = color
        self.screen = screen
        self.padding = padding
        self.minY = y
        self.X = x
        self.textObjs = list(map(lambda x:Text(tStyle,x,color,screen,anchor),items))
        self.Y = []
        self.commands = commands
        self.resetH = True
        self.calcY(padding,y)
        if highlightable:
            self.highlightOne(0)
        self.mode = False
        self.shortcut = {
            'sbutton' : [],
            'action'  : []
        }
    def calcY(self,pad,miny):
        height = self.textObjs[0].size[1]
        for i in range(len(self.textObjs)):
            try:
                self.Y.append(self.Y[-1] + height + pad)
            except IndexError:
                self.Y.append(miny +pad)
    def spawn(self):
        for i,j in enumerate(self.textObjs):
            coord = (self.X,self.Y[i])
            j.spawn(coord)
    def highlightOne(self,ind):
        if ind <0:
            ind = len(self.textObjs)-1
        elif ind > len(self.textObjs)-1:
            ind = 0
        self.textObjs[ind].highlighted= True
        self.highlightedOne = ind
        for i in range(len(self.textObjs)):
            if i !=ind:
                self.textObjs[i].highlighted = False
    def addShortcut(self,control,action):
        self.shortcut['sbutton'].append(control)
        self.shortcut['action'].append(action)
    def insertItem(self,index,text,command):
        self.textObjs.insert(index,Text(self.tStyle,text,self.color,self.screen,True))
        self.commands.insert(0,command)
        self.highlightOne(0)
        self.Y.clear()
        self.calcY(self.padding,self.minY)
    def removeItem(self,value):
        allItems = [x.text for x in self.textObjs]
        try:
            index = allItems.index(value)
            self.textObjs.pop(index)
            self.commands.pop(index)
            self.highlightOne(0)
            self.Y.clear()
            self.calcY(self.padding,self.minY)
        except ValueError:
            pass
    def highlight(self,mpos,vel):
        if vel == (0,0):
            self.mode = True
        else:
            self.mode = False
        if not self.mode:
            for i,j in enumerate(self.textObjs):
                halfPos = (j.size[0]/2,j.size[1]/2)
                if inRange(mpos,j.centerPoint,halfPos):
                    self.highlightOne(i)
                    break
    def runHighlighted(self):
        self.commands[self.textObjs.index(self.textObjs[self.highlightedOne])]()
        if self.resetH:
            self.highlightOne(0)
    def controls(self,events_in):
        keys = [pygame.K_UP,pygame.K_DOWN]
        actions = [-1,1]
        if events_in.type == pygame.KEYDOWN:
            if events_in.key in keys:
                self.mode = True
                self.highlightOne(self.highlightedOne+actions[keys.index(events_in.key)])
            elif events_in.key == pygame.K_RETURN:
                self.runHighlighted()
            elif events_in.key in self.shortcut['sbutton']:
                self.shortcut['action'][self.shortcut['sbutton'].index(events_in.key)]()
        elif events_in.type == pygame.MOUSEBUTTONUP:
            self.runHighlighted()
    def chgeText(self,newVal,ind):
        if ind == 'all':
            map(lambda x: x.chText(newVal[self.textObjs.index(x)]),self.textObjs)
        else:
            self.textObjs[ind].chText(newVal)
def spawnALl(items):
    for x in items:
        x.spawn()


def createFPSGraph(frames):
    second = list(range(1,len(frames)+1))
    plt.plot(second,frames)
    plt.xlabel('Seconds')
    plt.ylabel('Frames')
    plt.title('Visualization Of FPS')
    plt.show()


