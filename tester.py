i = [1,2,3,4,5,6,7]
for i in range(1,0,5):
    print(i)
# if i not in range(0,7):
#     print(False)
# import pygame
# pygame.init()
# screen = pygame.display.set_mode((1200,600))
# head = pygame.image.load('.\images\SnakeSkins\Classic\head.png')
# body = pygame.image.load(r'.\images\SnakeSkins\Classic\body.png')
# res = pygame.transform.scale(head,(100,100))
# resB = pygame.transform.scale(body,(100,100))
# rotres = pygame.transform.rotate(res,-90)
# running = True
# while running:
#     screen.fill((250,50,20))
#     for events_in in pygame.event.get():
#         if events_in.type == pygame.QUIT:
#             running = False
#     screen.blit(rotres,(100,50))
#     screen.blit(resB,(50,0))
#     pygame.display.update()