import pygame,time,os
from classespyg import *
from snakeClass import Snake
from Foods import Food
# pygame.init()
red = colors['red']
white = colors['white']
ScreenFeatures = {
    "width" : 1300,
    "height" : 700
}
backgroundDIr = os.path.dirname(__file__) + "\images\BackGrounds"
foodDir = ".\images\Foods"
snakeDir = ".\images\SnakeSkins"
foodUsed = foodDir + '\Classic'
# pygame.display.set_caption("Snake")
screen = pygame.display.set_mode((ScreenFeatures["width"],ScreenFeatures["height"]))
# screenBlur = screen.convert_alpha()
backgroundObj = Background(backgroundDIr + "\Classic\\backgrounds.jpg",ScreenFeatures["width"],ScreenFeatures["height"],screen)
snakeObj = Snake(screen)
foodObj = Food(foodUsed,screen)
paused = 0
collided = 0
score = 0
def calcScore(typeFood,value):
    global score
    if typeFood:
        score += int(((5-value) / 5) * 20)
    else:
        score += 1
def spawnScore(TFonts):
    TFonts.chText(str(score))
    TFonts.spawn()

def returnValue(desc):
    if desc:
        return collided

def collisions():
    global collided
    if snakeObj.boundaryChk(snakeObj.snakePoints[0],snakeObj.snakeDirection[0][0]):
        if detectCollision(snakeObj.reflectorPoint[0],snakeObj.snakePoints[2:len(snakeObj.snakePoints)+1],[100]):
            snakeObj.speed =0
            collided = 1
    elif detectCollision(snakeObj.snakePoints[0],snakeObj.snakePoints[2:len(snakeObj.snakePoints)+1],[100]):
        snakeObj.speed =0
        collided = 1
    valueCollided = returnCollided(snakeObj.centerPoints[0],[foodObj.foodCenter,foodObj.LfoodCenter],[100,150])
    if len(valueCollided)!=0:
        snakeObj.addBody()
        foodObj.respawn(valueCollided[0])
        calcScore(valueCollided[0],foodObj.stop)
    # print(collided)
def controlSnake(events_in):
    global paused
    controls = [pygame.K_UP,pygame.K_DOWN,pygame.K_RIGHT,pygame.K_LEFT]
    # if events_in.type == pygame.KEYDOWN:
    if events_in.key in controls:
        if paused:
            paused = False
            snakeObj.pause(paused)
            foodObj.pause(paused)
        else:
            snakeObj.turn(controls.index(events_in.key))
    elif events_in.key == pygame.K_ESCAPE:
        paused = not paused
        snakeObj.pause(paused)
        foodObj.pause(paused)
def printer():
    print('Booo')