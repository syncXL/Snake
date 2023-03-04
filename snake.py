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
gridSize = 50
mainMDIr = os.path.dirname(__file__) + '\images\\bg2.jpg'
screen = pygame.display.set_mode((ScreenFeatures["width"],ScreenFeatures["height"]))
backgroundObj = Background(backgroundDIr + "\Classic\\backgrounds.jpg",ScreenFeatures["width"],ScreenFeatures["height"],screen,gridSize)
mainMBG = Background(mainMDIr,ScreenFeatures["width"],ScreenFeatures["height"],screen)
minSpawn = (gridSize*3+50,gridSize*3+50)
maxSpawn = (1300 - gridSize*3 +50,700 - gridSize*3+50)
snakeObj = Snake(screen,gridSize,True,minSpawn,maxSpawn)
foodObj = Food(foodUsed,screen,gridSize)
paused = 0
collided = 0
score = 0
AllModes = ['Classic','Caged','Hard To Get','Inverted','Earthquake','Molly As Food','Nightmare']
def toCagedMode():
    global backgroundObj,snakeObj,foodObj
    backgroundObj.showoutline()
    snakeObj.reflectBool =False
    foodObj.addBoundary(gridSize)
def toClassicMode():
    global backgroundObj,snakeObj,foodObj
    backgroundObj.showoutline()
    snakeObj.reflectBool =True
    foodObj.removeBoundary()
def printer():
    print('Booo')
transMode = [toClassicMode,toCagedMode,printer,printer,printer,printer,printer]
mode = 0
save = {
    'Snake': list(),
    'Food' : list(),
    'Others' : ['Classic',0],
    'HighScores' : {
        'Classic' : list(),
        'Caged' : list(),
        'Hard To Get' : list(),
        'Inverted' : list(),
        'EarthQuake' : list(),
        'Molly As Food' : list(),
        'Nightmare' : list(),
    }
}
hScoreNavigator = 0
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
    global save,score,mode,collided,AllModes
    modetosave = AllModes[mode]
    if not collided:
        save['Food'] = foodObj.save()
        save['Snake'] = snakeObj.save()
        save['Others'] = [modetosave,score]
    else:
        save['Others'] = [modetosave,0]
    with open('save.json','w') as save_file:
        json.dump(save,save_file,
        indent=4)
def continueS():
    if save['Others'][1] != 0:
        return 1
    return 0
def highScore():
    global save,mode,score,AllModes
    if score !=0:
        modetype = AllModes[mode]
        save['HighScores'][modetype].append(score)
        save['HighScores'][modetype].sort(reverse = True)
        if len(save[ 'HighScores'][modetype]) > 15:
            save['HighScores'][modetype] = save['HighScores'][modetype][:15]
        score= 0
def loadFromJson():
    global save,score,paused,mode
    snakeObj.load(save['Snake'])
    foodObj.load(save['Food'])
    score = save['Others'][1]
    mode = AllModes.index(save['Others'][0])
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
    global collided,mode,gridSize
    if snakeObj.boundaryChk(snakeObj.snakePoints[0],snakeObj.snakeDirection[0][0]) and mode not in [1,6]:
        if detectCollision(snakeObj.reflectorPoint[0],snakeObj.snakePoints[2:len(snakeObj.snakePoints)+1],[gridSize-1]):
            gOver()
    elif detectCollision(snakeObj.snakePoints[0],snakeObj.snakePoints[2:len(snakeObj.snakePoints)+1],[gridSize-1]):
        gOver()
    elif mode in [1,6]:
        if False in snakeObj.boundaryChk(snakeObj.snakePoints[0],snakeObj.snakeDirection[0][0],(gridSize,gridSize),(1300 - (gridSize*2) +snakeObj.speed,700 - (gridSize*2) +snakeObj.speed)):
            gOver()
    valueCollided = returnCollided(snakeObj.centerPoints[0],[foodObj.foodCenter,foodObj.LfoodCenter],[gridSize,gridSize + (gridSize/2)])
    if len(valueCollided)!=0:
        snakeObj.addBody()
        foodObj.respawn(valueCollided[0])
        calcScore(valueCollided[0],foodObj.stop)
def gOver():
    global collided
    snakeObj.pause(1)
    foodObj.pause(1)
    collided = 1
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
def restart():
    global collided,paused,score,minSpawn,maxSpawn
    highScore()
    collided =0
    paused = 0
    snakeObj.init1(minSpawn,maxSpawn)
    foodObj.init1()
def changeHscore(val = 0):
    global hScoreNavigator
    hScoreNavigator += val
    if hScoreNavigator not in range(0,7):
        hScoreNavigator = abs(7-abs(hScoreNavigator))

def returnHscore():
    global hScoreNavigator
    return hScoreNavigator
def stylehScores():
    global hScoreNavigator,save
    scores = list(save['HighScores'].values())[hScoreNavigator]
    return list(map(lambda x: str(x[0]+1)+ '. ' + str(x[1]),list(enumerate(scores)))) if len(scores) !=0  else ['No Games Played']

def hScoreControls(events_in):
    if events_in.type == pygame.KEYDOWN:
        if events_in.key  == pygame.K_LEFT:
            changeHscore(-1)
        elif events_in.key == pygame.K_RIGHT:
            changeHscore(1)

def chMode(ind):
    global mode,transMode
    if mode != ind:
        mode = ind
        transMode[ind]()


def returnMode():
    global mode
    return AllModes[mode]