import json,os
# import math,time,pygame
# from classespyg import Text
# import tkinter
# fat = {
#     'dd' : 3,
#     'ee' : 4,
#     'hl' : 2
# }
a= 3
b= 4
c =6
for i in [a,b,c]:
    i += 7
print(a)
# if not os.path.isfile('save.json'):
#     open('save.json')
# try:
#     with open('save.json','r+') as f:
#         data = json.load(f)
#         print(data)
# except FileNotFoundError:
#     with open('save.json','') as f:
#         data = json.load(f)
    # data['dd'] = 10
    # f.seek(0)
    # json.dump(data,f,
    #     indent='\n',
    #     )
    # f.truncate()
# ll.sort(reverse=True)
# print(llrev)
# print(llrev.index(1))
# pygame.init()
# print(pygame.mouse.get_pos())
# print(type(lambda))
# stop = [3,4,5,6,7,8,9,10]
# start = {
#     'N' : stop
# }
# stop = (-3,-4)
# print(abs(stop[0]))
# for i in range (1,2):
#     print('MOTHAFUCKA')
# print(time.perf_counter()-start)
# for i in range(len(stop)):
#     stop.pop(i)
    # pri/nt(stop)
# print(not 0)
# pygame.init()
# screen = pygame.display.set_mode((1200,600))
# # screen.se
# fontnLocation = list(map(lambda x:pygame.font.match_font(x),pygame.font.get_fonts()))
# fontName = pygame.font.get_fonts()
# fontObj = Text(fontnLocation[0],100,fontName[0],(230,227,220),(400,150))
# running = True
# i = time.perf_counter()
# j = 0
# while running:
#     screen.fill((250,50,20))
#     for events_in in pygame.event.get():
#         if events_in.type == pygame.QUIT:
#             running = False
#     if j < len(fontnLocation):
#         if time.perf_counter()-i >= 2:
#             i = time.perf_counter()
#             j+=1
#             fontObj.chText(fontName[j])
#             fontObj.chFont(fontnLocation[j])
#     fontObj.spawn(screen)
#     pygame.display.update()
# def collided(self):
#         if 
#         if snakeObj.boundaryChk(snakeObj.snakePoints[0],snakeObj.snakeDirection[0][0]):
#             if detectCollision(snakeObj.reflectorPoint[0],snakeObj.snakePoints[2:len(snakeObj.snakePoints)+1],[100]):
#                 snakeObj.speed =0
