import pygame,json,os
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
mainMDIr = os.path.dirname(__file__) + '\images\\bg2.jpg'
# pygame.display.set_caption("Snake")
screen = pygame.display.set_mode((ScreenFeatures["width"],ScreenFeatures["height"]))
# screenBlur = screen.convert_alpha()
backgroundObj = Background(backgroundDIr + "\Classic\\backgrounds.jpg",ScreenFeatures["width"],ScreenFeatures["height"],screen)
mainMBG = Background(mainMDIr,ScreenFeatures["width"],ScreenFeatures["height"],screen)
snakeObj = Snake(screen)
foodObj = Food(foodUsed,screen)
paused = 0
collided = 0
sfxV = 0
musicV = 0
score = 0
mode = 'Classic'
save = {
    'Snake': list(),
    'Food' : list(),
    'Others' : ['Classic',0],
    'HighScores' : {
        'Classic' : list(),
        'Caged' : list(),
        'HardToGet' : list(),
        'Inverted' : list(),
        'EarthQuake' : list(),
        'MollyAsFood' : list(),
        'Nightmare' : list(),
    }
}
def calcScore(typeFood,value):
    global score
    if typeFood:
        score += int(((5-value) / 5) * 20)
    else:
        score += 1
def spawnScore(TFonts):
    TFonts.chText(str(score))
    TFonts.spawn()

def loadSave():
    global save
    try:
        with open('save.json','r') as save_file:
            save = json.load(save_file)
    except FileNotFoundError:
        with open('save.json','w') as save_file:
            json.dump(save,save_file,
            indent= 4)
def saveTOJson():
    global save,score,mode,collided
    if not collided:
        save['Food'] = foodObj.save()
        save['Snake'] = snakeObj.save()
        save['Others'] = [mode,score]
    else:
        save['Others'] = [mode,0]
    with open('save.json','w') as save_file:
        json.dump(save,save_file,
        indent=4)
def continueS():
    if save['Others'][1] != 0:
        return 1
    return 0
def loadFromJson():
    global save,score,paused
    snakeObj.load(save['Snake'])
    foodObj.load(save['Food'])
    score = save['Others'][1]
        # paused = 1
def returnValue(desc):
    if desc == True:
        return collided
    elif desc == False:
        return paused
    else:
        return score
def assignValue():
    global paused
    paused = 0
def collisions():
    global collided
    if snakeObj.boundaryChk(snakeObj.snakePoints[0],snakeObj.snakeDirection[0][0]):
        if detectCollision(snakeObj.reflectorPoint[0],snakeObj.snakePoints[2:len(snakeObj.snakePoints)+1],[100]):
            snakeObj.pause(1)
            foodObj.pause(1)
            collided = 1
    elif detectCollision(snakeObj.snakePoints[0],snakeObj.snakePoints[2:len(snakeObj.snakePoints)+1],[100]):
        snakeObj.pause(1)
        foodObj.pause(1)
        collided = 1
    valueCollided = returnCollided(snakeObj.centerPoints[0],[foodObj.foodCenter,foodObj.LfoodCenter],[100,150])
    if len(valueCollided)!=0:
        snakeObj.addBody()
        foodObj.respawn(valueCollided[0])
        calcScore(valueCollided[0],foodObj.stop)
    # print(collided)
def pauser():
    global paused
    paused = not paused
    snakeObj.pause(paused)
    foodObj.pause(paused)
def controlSnake(events_in):
    global paused
    controls = [pygame.K_UP,pygame.K_DOWN,pygame.K_RIGHT,pygame.K_LEFT]
    if events_in.type == pygame.KEYDOWN:
        if events_in.key in controls:
            if paused or snakeObj.speed==0:
                paused = False
                snakeObj.pause(paused)
                foodObj.pause(paused)
            snakeObj.turn(controls.index(events_in.key))
        elif events_in.key == pygame.K_ESCAPE:
            pauser()
def printer():
    print('Booo')
def restart():
    global collided,paused,score
    score= 0
    collided =0
    paused = 0
    snakeObj.init1()
    foodObj.init1()