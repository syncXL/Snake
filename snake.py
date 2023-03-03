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
screen = pygame.display.set_mode((ScreenFeatures["width"],ScreenFeatures["height"]))
backgroundObj = Background(backgroundDIr + "\Classic\\backgrounds.jpg",ScreenFeatures["width"],ScreenFeatures["height"],screen)
backgroundObj.showoutline()
mainMBG = Background(mainMDIr,ScreenFeatures["width"],ScreenFeatures["height"],screen)
minSpawn = (300,300)
maxSpawn = (1000,500)
snakeObj = Snake(screen,False,minSpawn,maxSpawn)
foodObj = Food(foodUsed,screen,[50,1200,600],[50,1175,475])
paused = 0
collided = 0
score = 0
ALLmodes = ['Classic','Caged','Hard To Get','Inverted','Earthquake','Molly As Food','Nightmare']
mode = 1
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
    global save,score,mode,collided,ALLmodes
    modetosave = ALLmodes[mode]
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
    global save,mode,score,ALLmodes
    modetype = ALLmodes[mode]
    save['HighScores'][modetype].append(score)
    save['HighScores'][modetype].sort(reverse = True)
    if len(save[ 'HighScores'][modetype]) > 15:
        save['HighScores'][modetype] = save['HighScores'][modetype][:15]
    score= 0
def loadFromJson():
    global save,score,paused
    snakeObj.load(save['Snake'])
    foodObj.load(save['Food'])
    score = save['Others'][1]
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
    global collided,mode
    if snakeObj.boundaryChk(snakeObj.snakePoints[0],snakeObj.snakeDirection[0][0]) and mode not in [1,6]:
        if detectCollision(snakeObj.reflectorPoint[0],snakeObj.snakePoints[2:len(snakeObj.snakePoints)+1],[49]):
            gOver()
    elif detectCollision(snakeObj.snakePoints[0],snakeObj.snakePoints[2:len(snakeObj.snakePoints)+1],[49]):
        gOver()
    elif mode in [1,6]:
        if False in snakeObj.boundaryChk(snakeObj.snakePoints[0],snakeObj.snakeDirection[0][0],(49,49),(1201,601)):
            print('over')
            gOver()
    valueCollided = returnCollided(snakeObj.centerPoints[0],[foodObj.foodCenter,foodObj.LfoodCenter],[50,75])
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
def printer():
    print('Booo')
def restart():
    global collided,paused,score,minSpawn,maxSpawn
    if score !=0:
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
    return list(map(lambda x: str(scores.index(x)+ 1)+ '. ' + str(x),scores)) if len(scores) !=0  else ['No Games Played']


def hScoreControls(events_in):
    if events_in.type == pygame.KEYDOWN:
        if events_in.key  == pygame.K_LEFT:
            changeHscore(-1)
        elif events_in.key == pygame.K_RIGHT:
            changeHscore(1)
