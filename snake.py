import pygame,random,math,time

pygame.init()
ScreenFeatures = {
    "width" : 1300,
    "height" : 700
}
directionChange = {
    'N' : (0,100),
    'S' : (0,-100),
    'E' : (-100,0),
    'W' : (100,0)
}
tailCoord = {
    'N' : (50,100),
    'E' : (-100,50),
    'S' : (50,-100),
    'W' : (100,50)

}
def bfs(points,changeGrid,checkBool):
    for i in points:
        if  checkBool[i]:
            if i[0] < (ScreenFeatures["width"]-changeGrid[0]):
                newGrid = (i[0]+changeGrid[0],i[1])
                if newGrid not in checkBool.keys():
                    points.append(newGrid)
                    checkBool[newGrid] = True
            if i[1] < (ScreenFeatures["height"]-changeGrid[1]):
                newGrid = (i[0],i[1]+changeGrid[1])
                if newGrid not in checkBool.keys():
                    points.append(newGrid)
                    checkBool[newGrid] =True
grids = [(0,0)]
visitedGrids = {
    (0,0) : True
}
bfs(grids,(100,100),visitedGrids)
visitedGrids = {x :False for x in visitedGrids}
darkBlue = (10,10,34)
red = (236,28,36)
white = (230,227,220)
colorGrids = {x :red for x in visitedGrids}
backgroundDIr = ".\images\BackGrounds"
foodDir = ".\images\Foods"
snakeDir = ".\images\SnakeSkins"
foodUsed = foodDir + '\Classic'
# snakeList = ["\snakeHead.png","\snakebody.png","\snaketail.png"]

pygame.display.set_caption("Snake")
screen = pygame.display.set_mode((ScreenFeatures["width"],ScreenFeatures["height"]))
class Background():
    def __init__(self,dir):
        self.position = [(0,0)]
        self.visited = {
            (0,0) : True
        }
        self.backgroundImage = pygame.image.load(backgroundDIr + dir + "\\backgrounds.jpg")
        self.objSize = self.backgroundImage.get_size()
        bfs(self.position,self.objSize,self.visited)
    def display(self):
        for i in self.position:
            screen.blit(self.backgroundImage,i)
class Snake():
    def __init__(self):
        self.speed = 1
        self.directions = [('N',(0,-1)),('S',(0,1)),('E',(1,0)),('W',(-1,0))]
        self.snakeCP = random.choice(self.directions)
        self.point = (random.randrange(300,1000,100),random.randrange(300,500,100))
        self.snakePoints = [self.point]
        self.snakeDirection = [self.snakeCP for i in range(3)]
        self.reflectorPoint = [self.point]
        self.centerPoints = [(0,0) for i in range(3)]
        self.turningPoint = []
        self.turnActive = []
        self.bodyCount = 1
        self.init2()
    def init2(self,n=1):
        if n != len(self.snakeDirection):
            self.addSegment()
            n+=1
            self.init2(n)
    def addSegment(self):
        X = self.snakePoints[-1][0]+directionChange[self.snakeDirection[-1][0]][0]
        Y = self.snakePoints[-1][1]+directionChange[self.snakeDirection[-1][0]][1]
        self.snakePoints.append((X,Y))
        self.reflectorPoint.append((X,Y))
        self.centerPoints.append((0,0))
    def head(self,coorD):
        pygame.draw.ellipse(screen,darkBlue,[coorD[0],coorD[1],100,100])
        self.centerPoints[0] = getCenter(coorD,100)
    def body(self,coorD):
        rect = pygame.Rect(coorD[0],coorD[1],100,100)
        pygame.draw.rect(screen,darkBlue,rect)
    def spawn(self,n = 0):
        self.draw_shapes(n,self.snakePoints)
        if False in self.boundaryChk(self.snakePoints[n]):
            self.draw_shapes(n,self.reflectorPoint)
        n+=1
        if n!=len(self.snakePoints):
            self.spawn(n)
    def mechanics(self):
        self.spawn()
        self.collided()
        self.reflector()
        self.resetter()
        self.turnRest()
        self.eat()
        self.move()
    def collided(self):
        if detectCollision(self.snakePoints[0],self.snakePoints[2:len(self.snakePoints)+1],[100]):
            self.speed =0
    def draw_shapes(self,n,CoordList):
        if n == 0:
            self.head(CoordList[n])
        else:
            self.body(CoordList[n])
            self.centerPoints[n] = getCenter(self.snakePoints[n],100)
    def boundaryChk(self,coOrd):
        boundaryBool = [True,True]
        if coOrd[0] < 0 or coOrd[0]>= 1200:
            boundaryBool[0]=False
        elif coOrd[1] <0 or coOrd[1]>=600:
            boundaryBool[1]=False
        return boundaryBool
    def reflect(self,coOrd,boundary):
        if abs(coOrd-boundary)<=boundary:
            return coOrd - boundary
        return coOrd + boundary
    def reflector(self,n=0):
        exceedBDR = self.boundaryChk(self.snakePoints[n])
        x = self.snakePoints[n][0]
        y = self.snakePoints[n][1]
        newCoord = [0,0]
        if not exceedBDR[0]:
            newCoord[0] = self.reflect(x,1300)
            newCoord[1] = y
            self.reflectorPoint[n] = tuple(newCoord)
        elif not exceedBDR[1]:
            newCoord[0] = x
            newCoord[1] = self.reflect(y,700)
            self.reflectorPoint[n] = tuple(newCoord)
        n+=1
        if n != len(self.snakePoints):
            self.reflector(n)
    def resetter(self,n=0):
        if self.snakePoints[n][0] <= -100 or self.snakePoints[n][0] >= 1300:
            self.snakePoints[n] = self.reflectorPoint[n]
        elif self.snakePoints[n][1] <= -100 or self.snakePoints[n][1] >= 700:
            self.snakePoints[n] = self.reflectorPoint[n]
        n+=1
        if n!= len(self.snakePoints):
            self.resetter(n)
    def chDirection(self,dir,booL):
        if dir == 'N' or dir == 'S':
            vAxis = self.getTurnedPoint(self.snakePoints[0][1]/100,booL) *100
            if vAxis >=600 or vAxis <0:
                vAxis = self.getTurnedPoint(self.reflectorPoint[0][1]/100,booL)*100
        else:
            vAxis = self.getTurnedPoint(self.snakePoints[0][0]/100,booL) *100
            if vAxis >=1200 or vAxis<0:
                vAxis = self.getTurnedPoint(self.reflectorPoint[0][0]/100,booL) *100
        return vAxis
    def getTurnedPoint(self,value,booL):
        if booL:
            return math.ceil(value)
        else:
            return math.floor(value)
    def turnRest(self):
        for i,k in enumerate(self.turnActive):
            pygame.draw.line(screen,darkBlue,self.turningPoint[i],self.turningPoint[i])
            for j in range(len(self.snakeDirection)):
                if k !=self.snakeDirection[j] and round(getDist(self.snakePoints[j],self.turningPoint[i])) == self.speed:
                    self.snakeDirection[j] = k
                    self.snakePoints[j] = self.turningPoint[i]
                    if j == len(self.snakeDirection)-1:
                        self.turnActive.pop(i)
                        self.turningPoint.pop(i)
    def turn(self,dir):
        dir = self.directions[dir]
        if dir != self.snakeDirection[0][0] and dir[1] != (self.snakeDirection[0][1][0] *-1,self.snakeDirection[0][1][1] *-1):
            booL = 0
            initDir = self.snakeDirection[0][0]
            if initDir == 'S'or initDir == 'E':
                booL = 1
            if initDir == 'N' or initDir == 'S':
                temp = (self.snakePoints[0][0],self.chDirection(initDir,booL))
            else:
                temp = (self.chDirection(initDir,booL),self.snakePoints[0][1])
            if self.addTurn(temp):
                self.turningPoint.append(temp)
                self.turnActive.append(dir)
    def addTurn(self,coord):
        if len(self.turningPoint) != 0:
            if getDist(self.turningPoint[-1],coord) >= 99:
                return True
            else:
                return False
        else:
            return True
    def addBody(self):
        self.bodyCount+=1
        self.addSegment()
        self.snakeDirection.append(self.snakeDirection[-1])
    def move(self,n=0):
        direction = self.snakeDirection[n][1]
        changeX = direction[0] * self.speed
        changeY = direction[1] * self.speed
        self.snakePoints[n] = (self.snakePoints[n][0]+changeX,self.snakePoints[n][1]+ changeY)
        if  False in self.boundaryChk(self.snakePoints[n]):
            self.reflectorPoint[n] = (self.reflectorPoint[n][0]+changeX,self.reflectorPoint[n][1]+ changeY)
            # print(self.snakePoints[n],self.reflectorPoint[n],sep='==')
        else:
            self.reflectorPoint[n] = self.snakePoints[n]
        n+=1
        if n != len(self.snakePoints):
            self.move(n)
    def eat(self):
        valueCollided = returnCollided(self.centerPoints[0],[foodObj.foodCenter,foodObj.LfoodCenter],[100,150])
        if len(valueCollided)!=0:
            snakeObj.addBody()
            foodObj.respawn(valueCollided[0])
class Food():
    def __init__(self,foodDir):
        self.mFood = pygame.image.load(foodDir + '/M.png')
        self.lFood = pygame.image.load(foodDir + '/L.png')
        self.FoodT = False
        self.collided = 0
        self.LfoodCoord = (-1000000,-100000)
        self.LfoodCenter  = (-100000,-100000)
        self.foodCoord = self.getPosition([1200,600],50,self.LfoodCenter)
        self.foodCenter = getCenter(self.foodCoord,100)
    def getPosition(self,boundary,width,other):
        while True:
            x = random.randrange(0,boundary[0],100)
            y = random.randrange(0,boundary[1],100)
            center = getCenter((x,y),width*2)
            if detectCollision(center,snakeObj.centerPoints+[other],[width+50]):
                continue
            else:
                break
        return (x,y)
    def spawn(self):
        if self.FoodT:
            screen.blit(self.lFood,self.LfoodCoord)
            pygame.draw.arc(screen,white,self.rect,0,self.degree,10000)
            self.calculate()
        screen.blit(self.mFood,(self.foodCoord))
    def mechanics(self):
        self.spawn()
    def respawn(self,num):
        if num ==1:
            self.LfoodCoord = (-1000000,-100000)
            self.LfoodCenter= (-100000,-100000)
            self.FoodT =False
        elif num ==0:
            self.collided +=1
            self.foodCoord = self.getPosition([1200,600],50,self.LfoodCenter)
            self.foodCenter = getCenter(self.foodCoord,100)
        if self.collided ==5:
            self.FoodT = True
            self.start = time.perf_counter()
            self.LfoodCoord = self.getPosition([1100,500],100,self.foodCenter)
            self.LfoodCenter = getCenter(self.LfoodCoord,200)
            self.calculate()
            self.collided = 0
    def calculate(self):
        percent = (time.perf_counter()-self.start)/5
        self.degree  = round(360 * percent * 0.0175,1)
        self.rect = [self.LfoodCoord[0],self.LfoodCoord[1],200,200]
        if percent >= 1:
            self.FoodT =False

def getCenter(coord,width):
        x = ((2*coord[0]) +width)/2
        y = ((2*coord[1]) +width)/2
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
    return False
def getDist(coord1,coord2):
    x = (coord2[0] - coord1[0])**2
    y = (coord2[1] - coord1[1])**2
    return math.sqrt(x+y)

backgroundObj = Background("\Classic")
snakeObj = Snake()
foodObj = Food(foodUsed)
def runGame():
    running=True
    snakeObj.spawn()
    while running:
        backgroundObj.display()
        for events_in in pygame.event.get():
            if events_in.type == pygame.QUIT:
                running = False
            elif events_in.type == pygame.KEYDOWN:
                if events_in.key == pygame.K_DOWN:
                    snakeObj.turn(1)
                elif events_in.key == pygame.K_UP:
                    snakeObj.turn(0)
                elif events_in.key == pygame.K_LEFT:
                    snakeObj.turn(3)
                elif events_in.key == pygame.K_RIGHT:
                    snakeObj.turn(2)
        snakeObj.mechanics()
        foodObj.mechanics()
        pygame.display.update()
runGame()

