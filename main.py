# import math
from snake import *
darkWhite = colors['darkWhite']
darkBlue = colors['darkBlue']
anotherblue = colors['blue+']

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
details = ['C:\WINDOWS\Fonts\\impact.ttf',60]
itemColor = [anotherblue,darkWhite]

scoreTxt = Text(detailsSmall,str(score),darkBlue,screen,False,(636,0))

GameOverText = Text(Title,'Game Over',[red,darkWhite],screen,True,(1300,0))
gameOverList = ListText(details,['  New Game ','  Return To Menu  '],itemColor,screen,1300,275,100,
            [lambda : tranState(restart,'Start'),lambda : tranState(lambda : checkVal(0),'MainMenu')],)

PauseText = Text(Title,'Paused',[red,darkWhite],screen,True,(1300,0))
pauseList = ListText(details,['  Resume  ','  Restart  ','  Options  ','  Return To Menu  ','  Quit  '],itemColor,screen,1300,200,20,[lambda : tranState(pauser),
            lambda : tranState(restart),printer,lambda : tranState(lambda : checkVal(1),'MainMenu'),quitter])

snakeTxt =  Text(Title,'Snake.py',[darkBlue,darkWhite],screen,True,(1300,0))
mainM = ListText(detailsSmall,['  New Game  ','  LeaderBoard  ','  Wardrobe  ','  Modes  ','  Options  ','  Exit  '],itemColor,screen,1300,220,8,
        [lambda : tranState(restart,'Start','Start'),lambda : tranState(dispScore,'HighScore','MainMenu'), printer,printer,printer,quitter])

highScoreTxt = Text(Title,'HighScores',[colors['turquoise'],darkWhite],screen,True,(1300,0))
modeTxt = Text(details,list(save['HighScores'].keys())[returnHscore()],[colors['turquoise'],darkWhite],screen,True,(1300,220))
hScoresTxt = []
def dispScore():
    global hScoresTxt,modeTxt
    modeTxt.chText(list(save['HighScores'].keys())[returnHscore()])
    whole = int(len(stylehScores())/5)
    remainder = len(stylehScores()) % 5
    hScoresTxt = []
    x = 250
    for i in range(1,whole*5,5):
        j = i-1
        hScoresTxt.append(ListText(detailsSmall,stylehScores()[j:j+5],itemColor,screen,x,300,15,[],False,False))
        x += 350
    if remainder != 0:
        hScoresTxt.append(ListText(detailsSmall,stylehScores()[whole*5:(whole*5)+(remainder+1)],itemColor,screen,250,300,15,[],False,False))


scoresTxt = ListText(detailsSmall,stylehScores(),itemColor,screen,300,300,15,[],False,False)
navImg = pygame.image.load(os.path.dirname(__file__) + "\images\\next.png")
navButtons = [pygame.transform.flip(navImg,True,False),navImg]
navCoord =[(0,350),(1100,350)]
if continueS():
    mainM.insertItem(0,'  Continue  ',lambda : tranState(loadFromJson,'Start','Start'))
def checkVal(state):
    mainM.removeItem('  Continue  ')
    if state:
        assignValue()
        mainM.insertItem(0,'  Continue  ', lambda : tranState('','Start','Start'))
    else:
        highScore()
def tranState(command='',value=-1,parent = ''):
    global currentState,historyState,stateName,exceptions
    if value != -1:
        stateName = value
        currentState = GameState[value]
        historyState.append(parent)
    else:
        if stateName not in exceptions:
            currentState = GameState[historyState[-1]]
            # historyState.pop()
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
    'SpawnTitle' : lambda : spawnALl([highScoreTxt,modeTxt]),
    'SpawnTxt' : lambda: spawnALl([x for x in hScoresTxt]),
    'SpawnButtons' : lambda: screen.blits(((navButtons[0],navCoord[0]),(navButtons[1],navCoord[1]))),
    'Controls' : hScoreControls,
    'update' : lambda : dispScore() if modeTxt.text != list(save['HighScores'].keys())[returnHscore()] else False

}
Wardrobe = {
    'ChangeBackGround' : '1',
    'ChangeSkin' : '2',
    'ChangeFood' : '3',
    'BackToMainMenu' : 0
}
Modes = {
    'Classic' : '1',
    'Inverted' : '2',
    'SpeedStar' : '3',
    'HardToGet' : '4',
    'RedZone' : '5',
    'Caged' : '6',
    'AllExceptClassic' : '7',
    'BackToMainMenu' : 0
}
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
addListToDict(MainMenuState,mainM,snakeTxt)
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
