import pygame,random,time
from classespyg import *
white = colors['white']
class Food():
    def __init__(self,foodDir,screen):
        self.mFood = pygame.image.load(foodDir + '/M.png')
        self.lFood = pygame.image.load(foodDir + '/L.png')
        self.FoodT = False
        self.collided = 0
        self.LfoodCoord = (-1000000,-100000)
        self.LfoodCenter  = (-100000,-100000)
        self.paused= 0
        self.breakPoint = 0
        self.screen = screen
        self.start = 0
        self.spawned = [False,True]
        self.stop = 0
    def getPosition(self,boundary,width,other,secondFood):
        while True:
            x = random.randrange(0,boundary[0],100)
            y = random.randrange(0,boundary[1],100)
            center = getCenter((x,y),[width*2,width*2])
            if detectCollision(center,other+[secondFood],[width+50]):
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
            self.foodCoord = self.getPosition([1200,600],50,occupiedPoint,self.LfoodCenter)
            self.foodCenter = getCenter(self.foodCoord,[100,100])
            self.spawned[0] = True
        if not self.spawned[1] and self.FoodT:
                self.LfoodCoord = self.getPosition([1100,500],100,occupiedPoint,self.foodCenter)
                self.LfoodCenter = getCenter(self.LfoodCoord,[200,200])
                self.spawned[1] = True
                self.calculate()
        self.spawn()
    def respawn(self,num):
        if num ==1:
            self.LfoodCoord = (-1000000,-100000)
            self.LfoodCenter= (-100000,-100000)
            self.breakPoint = 0
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
            self.stop =self.stop
        else:
            self.stop = (time.perf_counter() - self.start) -self.breakPoint
        percent = (self.stop)/5
        self.degree  = round(360 * percent * 0.0175,1)
        self.rect = [self.LfoodCoord[0],self.LfoodCoord[1],200,200]
        if percent >= 1:
            self.breakPoint = 0
            self.FoodT =False
    def pause(self,value):
        if not value and self.FoodT:
            self.breakPoint += time.perf_counter() - self.initBreak
        elif self.FoodT:
            self.initBreak = time.perf_counter()
        self.paused = value
