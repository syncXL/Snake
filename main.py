from snake import *
darkWhite = colors['darkWhite']
darkBlue = colors['darkBlue']
pygame.init()
fpsS = pygame.time.Clock()
FontUsed = 'C:\WINDOWS\Fonts\\impact.ttf'
scoreTxt = Text(FontUsed,50,str(score),colors['darkBlue'],(636,0),screen)
GameOverText = Text(FontUsed,200,'Game Over',[red,darkWhite],(200,50),screen)
NewGame = Text(FontUsed,100,'New Game',[darkBlue,darkWhite],(400,300),screen)
mainMenu = Text(FontUsed,100,'Back To Main Menu',[darkBlue,darkWhite],(200,450),screen)
gameOverList = ListText([GameOverText,NewGame,mainMenu],[printer,printer,printer],[0,1,1])

resume = Text(FontUsed,100,'Resume',[darkBlue,darkWhite],(100,100),screen)
restart = Text(FontUsed,100,'Restart',[darkBlue,darkWhite],(100,200),screen)
optionTxt = Text(FontUsed,100,'Options',[darkBlue,darkWhite],(100,300),screen)
pauseList = ListText([resume,restart,mainMenu,optionTxt],[printer,printer,printer,printer],[1,1,1,1])

# SnakeTxt = Text(FontUsed,200,'Snake',[darkBlue,darkWhite])
# MainMenuState = dict()
# PauseState = dict()
# GameeObj = Text(,200,"Game Over",[red,white],(200,50),screen)
# newGame = Text('C:\WINDOWS\Fonts\\impact.ttf',100,'New Game',colors['darkBlue'],(400,300),screen)
# returnToMainMenu = Text('C:\WINDOWS\Fonts\\impact.ttf',100,'Return To Main Menu',colors['darkBlue'],(200,450),screen)
def tranState(value):
    global currentState
    currentState = GameState[value]
# def runList(listTxt):
#     listTxt.spawn()
#     listTxt.controls()
#     listTxt.highlight(pygame.mouse.get_pos())
GOState = {
    'background' : backgroundObj.display,
    'SnakeMechanics' : snakeObj.mechanics,
    'FoodMechanics' : lambda : foodObj.mechanics(snakeObj.centerPoints),
    'scoring' : lambda : spawnScore(scoreTxt),
    'spawnTxt' :gameOverList.spawn,
    'Controls' : gameOverList.controls,
    'highlight' : lambda : gameOverList.highlight(pygame.mouse.get_pos(),pygame.mouse.get_rel())

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
    'Sender' : '0',
    'Sound' : '1',
    'Music' : '2',
    'BackToSender' : [0,1]
}
StartState = {
    'background' : backgroundObj.display,
    'SnakeMechanics' : snakeObj.mechanics,
    'FoodMechanics' : lambda : foodObj.mechanics(snakeObj.centerPoints),
    'Collisions' : collisions,
    'Controls' : controlSnake,
    'scoring' : lambda : spawnScore(scoreTxt),
    'Pause' : lambda : tranState(pauseList) if paused else False,
    'GameOver' : lambda : tranState('GameOver') if returnValue(True) else False
}
MainMenuState = {
    'Continue' : '1',
    'NewGame' : StartState,
    'WardRobe' : Wardrobe,
    'Modes': Modes,
    'Options' : Options,
    'Exit' : '6'
}
GameState = {
    'MainMenu': MainMenuState,
    'Start' : StartState,
    'Wardrobe' : Wardrobe,
    'Modes' : Modes,
    'Options' : Options,
    'GameOver' : GOState
}
currentState = GameState['Start']


# def runState(state):

def runGame():
    running=True
    while running:
        for events_in in pygame.event.get():
            if events_in.type == pygame.KEYDOWN:
                currentState['Controls'](events_in)
            elif events_in.type == pygame.QUIT:
                    running = False
        for i in currentState.keys():
            if i != 'Controls':
                currentState[i]()
        pygame.display.update()
        fpsS.tick_busy_loop(180)
runGame()


# class State:
#     def __init__(self,initState):
#         self.currState = initState
#     def loadState
#initializing gameplay states
# names = ['background','SnakeMechanics','FoodMechanics','Collisions','Controls','Scoring','Pause','GameOver']
# features = [backgroundObj.display,snakeObj.mechanics,foodObj.mechanics,collisions,controlSnake,calcScore]
# states = [PauseState,GameOverState]
# GamePlay = State(names,features,states)
# # Game Over
# names = 
