import pygame,random,time
from classespyg import *
white = colors['white']
class Food():
    def __init__(self,foodDir,screen,smallFoodBoundary = [0,1250,650],lFoodBoundary = [0,1225,525]):
        self.mFood = pygame.transform.scale(pygame.image.load(foodDir + '/M.png'),(50,50))
        self.lFood = pygame.transform.scale(pygame.image.load(foodDir + '/L.png'),(100,100))
        self.screen = screen
        self.smallBoundary = smallFoodBoundary
        self.largeBoundary = lFoodBoundary
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
    def getPosition(self,boundary,width,other,secondFood):
        while True:
            x = random.randrange(boundary[0],boundary[1],50)
            y = random.randrange(boundary[0],boundary[2],50)
            center = getCenter((x,y),[width*2,width*2])
            otherSize = width + (width*2 if width == 25 else width/2)
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
            self.foodCoord = self.getPosition(self.smallBoundary,25,occupiedPoint,self.LfoodCenter)
            self.foodCenter = getCenter(self.foodCoord,[50,50])
            self.spawned[0] = True
        if not self.spawned[1] and self.FoodT:
                self.LfoodCoord = self.getPosition(self.largeBoundary,50,occupiedPoint,self.foodCenter)
                self.LfoodCenter = getCenter(self.LfoodCoord,[100,100])
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
        self.rect = [self.LfoodCoord[0],self.LfoodCoord[1],100,100]
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
