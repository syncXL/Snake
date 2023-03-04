import pygame,random,time
from classespyg import *
white = colors['white']
class Food():
    def __init__(self,foodDir,screen,gSize,boundary = 0):
        self.smallBoundary = [boundary,1300 - (boundary+gSize),700 - (boundary+gSize)]
        self.largeBoundary = [boundary,self.smallBoundary[1] -gSize/2,self.smallBoundary[2]- gSize/2]
        self.mFood = pygame.transform.scale(pygame.image.load(foodDir + '/M.png'),(gSize,gSize))
        self.lFood = pygame.transform.scale(pygame.image.load(foodDir + '/L.png'),(gSize*2,gSize*2))
        self.gridSize = gSize
        self.screen = screen
        self.init1()
    def init1(self):
        self.FoodT = False
        self.collided = 0
        self.LfoodCoord = (-1000000,-100000)
        self.LfoodCenter  = (-100000,-100000)
        self.paused= 0
        self.breakPoint = 0
        self.initBreak = 0
        self.start = 0
        self.spawned = [False,True]
        self.stop = 0
        self.quitTimer = 0
    def save(self):
        return [self.FoodT,self.collided,self.LfoodCoord,self.LfoodCenter,self.paused,self.spawned,self.stop,self.foodCoord,self.foodCenter]
    def load(self,values):
        self.FoodT = values[0]
        self.collided = values[1]
        self.LfoodCoord = tuple(values[2])
        self.LfoodCenter = tuple(values[3])
        self.paused = values[4]
        self.spawned = values[5]
        self.quitTimer = values[6]
        self.stop = values[6]
        self.foodCoord = tuple(values[7])
        self.foodCenter = tuple(values[8])
        if self.FoodT:
            self.calculate()
    def getPosition(self,boundary,radius,other,secondFood):
        while True:
            x = random.randrange(boundary[0],boundary[1],self.gridSize)
            y = random.randrange(boundary[0],boundary[2],self.gridSize)
            center = getCenter((x,y),[radius*2,radius*2])
            otherSize = radius + (radius*2 if radius == self.gridSize/2 else radius/2)
            if detectCollision(center,other+[secondFood],[otherSize]):
                continue
            else:
                break
        return (x,y)

    def spawn(self):
        if self.FoodT:
            self.screen.blit(self.lFood,self.LfoodCoord)
            pygame.draw.arc(self.screen,white,self.rect,0,self.degree,10000)
            self.calculate()
        self.screen.blit(self.mFood,(self.foodCoord))
    def mechanics(self,occupiedPoint):
        if not self.spawned[0]:
            self.foodCoord = self.getPosition(self.smallBoundary,self.gridSize/2,occupiedPoint,self.LfoodCenter)
            self.foodCenter = getCenter(self.foodCoord,[self.gridSize,self.gridSize])
            self.spawned[0] = True
        if not self.spawned[1] and self.FoodT:
                self.LfoodCoord = self.getPosition(self.largeBoundary,self.gridSize,occupiedPoint,self.foodCenter)
                self.LfoodCenter = getCenter(self.LfoodCoord,[self.gridSize*2,self.gridSize*2])
                self.spawned[1] = True
                self.calculate()
        self.spawn()
    def respawn(self,num):
        if num ==1:
            self.LfoodCoord = (-1000000,-100000)
            self.LfoodCenter= (-100000,-100000)
            self.breakPoint = 0
            self.quitTimer = 0
            self.FoodT =False
            self.spawned[1] = True
        elif num ==0:
            self.collided +=1
            self.spawned[0] = False
        if self.collided ==5:
            self.FoodT = True
            self.spawned[1] = False
            self.start = time.perf_counter()
            self.collided = 0
    def calculate(self):
        if self.paused:
            self.stop = self.stop
        else:
            self.stop = (time.perf_counter() - self.start) -self.breakPoint +self.quitTimer
        percent = (self.stop)/5
        self.degree  = round(360 * percent * 0.0175,1)
        self.rect = [self.LfoodCoord[0],self.LfoodCoord[1],self.gridSize*2,self.gridSize*2]
        if percent >= 1:
            self.quitTimer = 0
            self.breakPoint = 0
            self.FoodT =False
    def pause(self,value):
        if not value and self.FoodT:
            self.breakPoint += time.perf_counter() - self.initBreak
        elif self.FoodT and not self.paused:
            self.initBreak = time.perf_counter()
        self.paused = value
    def addBoundary(self,size):
        self.smallBoundary = [size,1300 - (size+self.gridSize),700 - (size+self.gridSize)]
        self.largeBoundary = [size,self.smallBoundary[1] -self.gridSize/2,self.smallBoundary[2]- self.gridSize/2]
    def removeBoundary(self):
        self.smallBoundary = [0,1300 - (0+self.gridSize),700 - (0+self.gridSize)]
        self.largeBoundary = [0,self.smallBoundary[1] -self.gridSize/2,self.smallBoundary[2]- self.gridSize/2]