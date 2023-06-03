import os 

import pygame
from pygame.locals import *

from ui.ui import UImanager, Canvas, Label, ScrollBar, Tab, Container, Button

pygame.init()

SCREEN_WIDTH = 795
SCREEN_HEIGHT = 721


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

pygame.display.set_caption('UI TEST')

screen1 = UImanager(screen, debug=True)


'''
Example 1 is going to be alot easier once each object has its own dictionary of 
objects types attached to it including the objects attached children

example: 

objectTypeList = {
    'Label' : [list of every Label object attached]
}
the code below would just be 
for label in canvas2.objectTypeList['Label']:
    label.object.x = label.parent.object.topleft[0]
    label.object.y = label.parent.object.topleft[1] - label.object.h
'''
# 1 : example of maipulating ui objects 
def positon(*labels):
    for label in labels:
        if label.parent:
            label.object.x = label.parent.object.topleft[0]
            label.object.y = label.parent.object.topleft[1] - label.object.h

canvas2 = Canvas(screen1, isMoveable=False, objectPosition=(400,100), isVisible=True)
label4 = Label( '!', (255,0,0), parent=canvas2, identifier='!')
label5 = Label('World', (255,0,0), parent=label4, identifier='World')
label6 = Label('Hello', (255,0,0), parent=label5, identifier='Hello')
ScrollBar(canvas2, bgColour=(255,250,250), objectSize=(5,10))
positon(label4, label5, label6)
####

# 2 : example of using objects to create a new object [Drop down menu]
c = Container(screen1, isVisible=True)
w = Canvas(None, parent=c, objectSize=(55,45), objectPosition=(100,105),isMoveable=False)
label4 = Label('NOTHING', (255,0,0),parent=w, objectPosition=(100, 135))
label5 = Label('DO', (255,0,0), parent=label4,objectPosition=(100, 120))
label6 = Label('I', (255,0,0), parent=label5,objectPosition=(100, 105))
b = Button(event=None, eventArgs=None, child=w, text='Click Me', textColour=(255,0,0), parent=c, objectPosition=(100,90))
####

run = True
while run:
    screen.fill((0,0,0))

    pygame.display.set_caption(f'UI TEST FPS({round(clock.get_fps())}) Container Objects({screen1.numbContainers}) Parent Objects({screen1.numbParentObjs}) Child Objects({screen1.numbChildObjs})')

    screen1.threaded_cycle()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  
            run = False
    
        if event.type == pygame.KEYDOWN:
            pass
            
    pygame.display.flip()
    clock.tick(60)

pygame.quit()