import pygame,random,math
from classespyg import *
darkBlue = colors['darkBlue']
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

class Snake():
    def __init__(self,screen):
        self.speed = 4
        self.directions = [('N',(0,-1)),('S',(0,1)),('E',(1,0)),('W',(-1,0))]
        self.snakeCP = random.choice(self.directions)
        self.point = (random.randrange(300,1000,100),random.randrange(300,500,100))
        self.snakePoints = [self.point]
        self.snakeDirection = [self.snakeCP for i in range(3)]
        self.reflectorPoint = [self.point]
        self.centerPoints = [(0,0) for i in range(3)]
        self.turningPoint = []
        self.turnActive = []
        self.turnQueue = []
        self.bodyCount = 1
        self.initSpeed=0
        self.screen = screen
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
        pygame.draw.ellipse(self.screen,darkBlue,[coorD[0],coorD[1],100,100])
        self.centerPoints[0] = getCenter(coorD,[100,100])
    def body(self,coorD):
        rect = pygame.Rect(coorD[0],coorD[1],100,100)
        pygame.draw.rect(self.screen,darkBlue,rect)
    def spawn(self,n = 0):
        self.draw_shapes(n,self.snakePoints)
        if False in self.boundaryChk(self.snakePoints[n],self.snakeDirection[n][0]):
            self.draw_shapes(n,self.reflectorPoint)
        n+=1
        if n!=len(self.snakePoints):
            self.spawn(n)
    def mechanics(self):
        self.spawn()
        if self.speed != 0:
            self.reflector()
            self.resetter()
            self.turnRest()
            self.move()
    def draw_shapes(self,n,CoordList):
        if n == 0:
            self.head(CoordList[n])
        else:
            self.body(CoordList[n])
            self.centerPoints[n] = getCenter(self.snakePoints[n],[100,100])
    def boundaryChk(self,coOrd,dir):
        boundaryBool = [True,True]
        if (coOrd[0] < 0 and dir == 'W') or (coOrd[0] >= 1200 and dir == 'E'):
            boundaryBool[0]=False
        elif (coOrd[1] <0 and dir == 'N') or (coOrd[1]>=600 and dir== 'S'):
            boundaryBool[1]=False
        return boundaryBool
    def reflect(self,coOrd,boundary):
        if abs(coOrd-boundary)<=boundary:
            return coOrd - boundary
        return coOrd + boundary
    def reflector(self,n=0):
        exceedBDR = self.boundaryChk(self.snakePoints[n],self.snakeDirection[n][0])
        x = self.snakePoints[n][0]
        y = self.snakePoints[n][1]
        newCoord = [x,y]
        if not exceedBDR[0]:
            newCoord[0] = self.reflect(x,1300)
            self.reflectorPoint[n] = tuple(newCoord)
        elif not exceedBDR[1]:
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
        toRemove = []
        for i in range(len(self.turnActive)):
            snakeBody =  self.turnQueue[i]
            if getDist(self.snakePoints[snakeBody],self.turningPoint[i]) <= self.speed:
                self.snakeDirection[snakeBody] = self.turnActive[i]
                self.snakePoints[snakeBody] = self.removeSpace(self.turningPoint[i],snakeBody)
                self.turnQueue[i] +=1
                if snakeBody == len(self.snakeDirection)-1:
                    toRemove.append(i)
        for i in toRemove:
            self.turnActive.pop(i)
            self.turningPoint.pop(i)
            self.turnQueue.pop(i)
    def removeSpace(self,coord,ind):
        if ind == 0:
            return coord
        x = coord[0]
        y = coord[1]
        if getDist(coord,self.snakePoints[ind-1]) != 100:
            if self.snakeDirection[ind][0] == 'N' or self.snakeDirection[ind][0] == 'S':
                y = self.snakePoints[ind-1][1] + directionChange[self.snakeDirection[ind][0]][1]
            elif self.snakeDirection[ind][0] == 'E' or self.snakeDirection[ind][0] == 'W':
                x = self.snakePoints[ind-1][0] + directionChange[self.snakeDirection[ind][0]][0]
        return (x,y)
    def turn(self,dir):
        dir = self.directions[dir]
        self.reflector()
        self.resetter()
        if dir[0] != self.snakeDirection[0][0] and dir[1] != (self.snakeDirection[0][1][0] *-1,self.snakeDirection[0][1][1] *-1):
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
                self.turnQueue.append(0)
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
        self.snakeDirection.append(self.snakeDirection[-1])
        self.addSegment()
    def move(self,n=0):
        direction = self.snakeDirection[n][1]
        changeX = direction[0] * self.speed
        changeY = direction[1] * self.speed
        self.snakePoints[n] = (self.snakePoints[n][0]+changeX,self.snakePoints[n][1]+ changeY)
        if  False in self.boundaryChk(self.snakePoints[n],self.snakeDirection[n][0]):
            self.reflectorPoint[n] = (self.reflectorPoint[n][0]+changeX,self.reflectorPoint[n][1]+ changeY)
        else:
            self.reflectorPoint[n] = self.snakePoints[n]
        n+=1
        if n != len(self.snakePoints):
            self.move(n)
    def pause(self,value):
        if value:
            self.initSpeed = self.speed
            self.speed= 0
        else:
            self.speed = self.initSpeed
