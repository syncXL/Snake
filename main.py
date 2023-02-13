from snake import *
darkWhite = colors['darkWhite']
darkBlue = colors['darkBlue']
violet = colors['Violet']
pygame.init()
running=True
fpsS = pygame.time.Clock()
def quitter():
    global running
    if returnValue(3) != 0:
        saveTOJson()
    running = False

Title = ['C:\WINDOWS\Fonts\\impact.ttf',200]
detailsSmall = ['C:\WINDOWS\Fonts\\impact.ttf',50]
details = ['C:\WINDOWS\Fonts\\impact.ttf',60]
scoreTxt = Text(detailsSmall,str(score),darkBlue,screen,False,(636,0))
GameOverText = Text(Title,'Game Over',[red,darkWhite],screen,True,(1300,0))
itemColor = [violet,darkWhite]
gameOverList = ListText(details,['  New Game ','  Return To Menu  '],itemColor,screen,[lambda : tranState(restart),lambda : tranState(lambda : checkVal(0),'MainMenu')],1300,275,100)

PauseText = Text(Title,'Paused',[red,darkWhite],screen,True,(1300,0))
pauseList = ListText(details,['  Resume  ','  Restart  ','  Options  ','  Return To Menu  ','  Quit  '],itemColor,screen,[lambda : tranState(pauser),
            lambda : tranState(restart),printer,lambda : tranState(lambda : checkVal(1),'MainMenu'),quitter],1300,200,20)
pauseList.addShortcut(pygame.K_ESCAPE,lambda : tranState(pauser))

snakeTxt =  Text(Title,'Snake.py',[darkBlue,darkWhite],screen,True,(1300,0))
mainM = ListText(detailsSmall,['  New Game  ','  Wardrobe  ','  Modes  ','  Options  ','  Exit  '],itemColor,screen,
        [lambda : tranState(restart,'Start','MainMenu'), printer,printer,printer,quitter],1300,220,20)
loadSave()
if continueS():
    mainM.insertItem(0,'  Continue  ',lambda : tranState(loadFromJson,'Start','MainMenu'))
def checkVal(state):
    mainM.removeItem('  Continue  ')
    if state:
        assignValue()
        mainM.insertItem(0,'  Continue  ', lambda : tranState('','Start','MainMenu'))
# if returnValue(3) != 0:

# SnakeTxt = Text(Title,'Snake',[darkBlue,darkWhite])
# MainMenuState = dict()
# GameeObj = Text(,200,"Game Over",[red,white],(200,50),screen)
# newGame = Text('C:\WINDOWS\Fonts\\impact.ttf',100,'New Game',colors['darkBlue'],(400,300),screen)
# returnToMainMenu = Text('C:\WINDOWS\Fonts\\impact.ttf',100,'Return To Main Menu',colors['darkBlue'],(200,450),screen)

historyState = []
def tranState(command='',value=-1,parent = ''):
    global currentState,historyState
    if value != -1:
        currentState = GameState[value]
        historyState.append(parent)
    else:
        currentState = GameState[historyState[-1]]
        historyState.pop()
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
    'Wardrobe' : Wardrobe,
    'Modes' : Modes,
    'Options' : Options,
    'GameOver' : GOState,
    'Pause' :PauseState
}
currentState = GameState['MainMenu']


# def runState(state):

def runGame():
    global running
    while running:
        for events_in in pygame.event.get():
            currentState['Controls'](events_in)
            if events_in.type == pygame.QUIT:
                quitter()
        for i in currentState.keys():
            if i not in currentState.keys():
                break
            elif i != 'Controls':
                currentState[i]()
        pygame.display.update()
        fpsS.tick_busy_loop(180)
runGame()
