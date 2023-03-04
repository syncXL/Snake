# import math
from snake import *
darkWhite = colors['darkWhite']
darkBlue = colors['darkBlue']
anotherblue = colors['blue+']
turquoise = colors['turquoise']
pygame.init()
running=True
fpsS = pygame.time.Clock()
historyState = []
def quitter():
    global running,historyState
    if 'Start' in historyState:
        saveTOJson()
    running = False
loadSave()
Title = ['C:\WINDOWS\Fonts\\impact.ttf',200]
detailsSmall = ['C:\WINDOWS\Fonts\\impact.ttf',50]
detailsTiny = ['C:\WINDOWS\Fonts\\impact.ttf',20]
details = ['C:\WINDOWS\Fonts\\impact.ttf',60]
itemColor = [anotherblue,darkWhite]

scoreTxt = Text(detailsSmall,str(score),turquoise,screen,False,(636,0))
mmTitle = Text(Title,'Snake.py',[turquoise,darkWhite],screen,True,(1300,0))
GameOverText = Text(Title,'Game Over',[red,darkWhite],screen,True,(1300,0))
gameOverList = ListText(details,['  New Game ','  Return To Menu  '],itemColor,screen,1300,275,100,
            [lambda : tranState(restart,'Start'),lambda : tranState(lambda : checkVal(0),'MainMenu')],)

PauseText = Text(Title,'Paused',[red,darkWhite],screen,True,(1300,0))
pauseList = ListText(details,['  Resume  ','  Restart  ','  Options  ','  Return To Menu  ','  Quit  '],itemColor,screen,1300,200,20,[lambda : tranState(pauser),
            lambda : tranState(restart),printer,lambda : tranState(lambda : checkVal(1),'MainMenu'),quitter])

mainM = ListText(detailsSmall,['  New Game  ','  LeaderBoard  ','  Wardrobe  ','  Modes  ','  Options  ','  Exit  '],itemColor,screen,1300,220,8,
        [lambda : tranState(restart,'Start','Start'),lambda : tranState(dispScore,'HighScore','MainMenu'), printer,
        lambda : tranState(lambda : placeInUse(AllModes.index(returnMode())),'Modes','MainMenu'),printer,quitter])

hScoreModeTxt = Text(details,list(save['HighScores'].keys())[returnHscore()],[turquoise,darkWhite],screen,True,(1300,220))
hScoresTxt = []
def changeMode():
    global modesTxt
    chMode(modesTxt.highlightedOne)
    placeInUse(modesTxt.highlightedOne)

def dispScore():
    global hScoresTxt,hScoreModeTxt
    hScoreModeTxt.chText(list(save['HighScores'].keys())[returnHscore()])
    whole = int(len(stylehScores())/5)
    remainder = len(stylehScores()) % 5
    hScoresTxt = []
    x = 250
    for i in range(1,whole*5,5):
        j = i-1
        hScoresTxt.append(ListText(detailsSmall,stylehScores()[j:j+5],itemColor,screen,x,300,15,[],False,False))
        x += 350
    if remainder != 0:
        hScoresTxt.append(ListText(detailsSmall,stylehScores()[whole*5:(whole*5)+(remainder+1)],itemColor,screen,x,300,15,[],False,False))

modesTxt =  ListText(detailsSmall,list(map(lambda x: '  ' + x + '  ',AllModes)),itemColor,screen,1300,200,10,[changeMode for x in range(7)],True,True)
modesTxt.resetH = False
modeSelected = Text(detailsSmall,"In Use",itemColor,screen,False,(1150,210))


scoresTxt = ListText(detailsSmall,stylehScores(),itemColor,screen,300,300,15,[],False,False)
navImg = pygame.image.load(os.path.dirname(__file__) + "\images\\next.png")
navButtons = [pygame.transform.flip(navImg,True,False),navImg]
navCoord =[(0,350),(1100,350)]
if continueS():
    mainM.insertItem(0,'  Continue  ',lambda : tranState(loadFromJson,'Start','Start'))
def placeInUse(ind):
    global modeSelected,modesTxt
    mainM.removeItem('  Continue  ') if save['Others'][0] != returnMode() else False
    modeSelected.coord = (1150,modesTxt.Y[ind])
def checkVal(state):
    mainM.removeItem('  Continue  ')
    if state:
        assignValue()
        mainM.insertItem(0,'  Continue  ', lambda : tranState('','Start','Start'))
    else:
        highScore()
def tranState(command='',value=-1,parent = ''):
    global currentState,historyState,stateName,exceptions,mmTitle
    if value != -1:
        stateName = value
        currentState = GameState[value]
        historyState.append(parent)
    else:
        if stateName not in exceptions:
            currentState = GameState[historyState[-1]]
    if parent == 'MainMenu':
        mmTitle.chText(value)
    elif value == 'MainMenu' or historyState[-1] == "MainMenu":
        mmTitle.chText('Snake.py')
    if command != '':
        command()
def addListToDict(dictName,listName,additons = ''):
    dictName['spawnTxt'] =  listName.spawn if additons == '' else lambda : spawnALl([listName,additons])
    dictName['Controls'] = listName.controls
    dictName['highlight'] = lambda : listName.highlight(pygame.mouse.get_pos(),pygame.mouse.get_rel())
def inheritValues(child,parent,keys):
    for i in keys:
        child[i] = parent[i]
GOState = dict()
PauseState = dict()
HighScore = {
    'background' : mainMBG.display,
    'SpawnTitle' : lambda : spawnALl([mmTitle,hScoreModeTxt]),
    'SpawnTxt' : lambda: spawnALl([x for x in hScoresTxt]),
    'SpawnButtons' : lambda: screen.blits(((navButtons[0],navCoord[0]),(navButtons[1],navCoord[1]))),
    'Controls' : hScoreControls,
    'update' : lambda : dispScore() if hScoreModeTxt.text != list(save['HighScores'].keys())[returnHscore()] else False

}
Wardrobe = {
    'ChangeBackGround' : '1',
    'ChangeSkin' : '2',
    'ChangeFood' : '3',
    'BackToMainMenu' : 0
}
Modes = {
    'background' : mainMBG.display,
    'In Use' : modeSelected.spawn
}
addListToDict(Modes,modesTxt,mmTitle)
Options = {
    'Sound' : '1',
    'Music' : '2',
}
StartState = {
    'background' : backgroundObj.display,
    'SnakeMechanics' : snakeObj.mechanics,
    'FoodMechanics' : lambda : foodObj.mechanics(snakeObj.centerPoints),
    'scoring' : lambda : spawnScore(scoreTxt),
    'Collisions' : collisions,
    'Controls' : controlSnake,
    'Pause' : lambda : tranState('','Pause','Start') if returnValue(False) else False,
    'GameOver' : lambda : tranState('','GameOver','Start') if returnValue(True) else False
}
inheritValues(GOState,StartState,['background','SnakeMechanics','FoodMechanics','scoring'])
inheritValues(PauseState,StartState,['background','SnakeMechanics','FoodMechanics','scoring'])
addListToDict(PauseState,pauseList,PauseText)
addListToDict(GOState,gameOverList,GameOverText)
MainMenuState = {
    'background' : mainMBG.display
}
addListToDict(MainMenuState,mainM,mmTitle)
GameState = {
    'MainMenu': MainMenuState,
    'Start' : StartState,
    'HighScore' : HighScore,
    'Wardrobe' : Wardrobe,
    'Modes' : Modes,
    'Options' : Options,
    'GameOver' : GOState,
    'Pause' :PauseState
}
exceptions = ['MainMenu','Start','GameOver']
stateName = 'MainMenu'
currentState = GameState[stateName]


def runGame():
    global running
    while running:
        for events_in in pygame.event.get():
            if events_in.type == pygame.KEYDOWN:
                if events_in.key == pygame.K_ESCAPE:
                    tranState()
            elif events_in.type == pygame.QUIT:
                quitter()
            currentState['Controls'](events_in)
        for i in currentState.keys():
            if i not in currentState.keys():
                break
            elif i != 'Controls':
                currentState[i]()
        pygame.display.update()
        fpsS.tick_busy_loop(180)
runGame()
