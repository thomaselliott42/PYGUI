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

screen1 = UImanager(screen, debug=True, threadedCollisionDetection=True)


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

canvas2 = Canvas(screen1, isMoveable=True, objectPosition=(400,100), isVisible=True)
label4 = Label( '!', (255,0,0), parent=canvas2, identifier='!')
label5 = Label('World', (255,0,0), parent=label4, identifier='World')
label6 = Label('Hello', (255,0,0), parent=label5, identifier='Hello')
ScrollBar(canvas2, bgColour=(255,250,250), objectSize=(5,10))
positon(label4, label5, label6)
####

# 2 : example of using objects to create a new object and ui manipulation [Drop down menu]
def update_canvas_scale(canvas, *labels):

    canvas.object.w = 0
    for width in [label.object.w for label in labels]:
        canvas.object.w += width
    canvas.object.w += 10

    canvas.object.h = 0
    for height in [label.object.h for label in labels]:
        canvas.object.h += height
    canvas.object.h += len(labels)*5


c = Container(screen1)
canvas = Canvas(None, parent=c, objectSize=(55,45), objectPosition=(100,105),isMoveable=False)
label1 = Label('I', (255,0,0), parent=canvas, objectPosition=(100, 180))
label2 = Label('DO', (255,0,0), parent=label1, objectPosition=(100, 165))
label3 = Label('OR', (255,0,0), parent=label2, objectPosition=(100, 150))
label4 = Label('NOTHING', (255,0,0), parent=label3, objectPosition=(100, 135))
label5 = Label('DO', (255,0,0), parent=label4, objectPosition=(100, 120))
label6 = Label('I', (255,0,0), parent=label5, objectPosition=(100, 105))
b = Button(event=None, eventArgs=[], child=canvas, text='Click Me', textColour=(255,0,0), parent=c, objectPosition=(100,90))

update_canvas_scale(canvas, label1, label2, label3, label4, label5, label6)
####


# 3 : project zomboid like inventory example 

inventoryContainer = Container(screen1)
canvas = Canvas(None, parent=inventoryContainer, objectSize=(100,45), objectPosition=(100,0),isMoveable=True, identifier='canvas1')
canvas2 = Canvas(None, parent=canvas, objectSize=(100,100), objectPosition=(100,0),isMoveable=True, identifier='canvas2')
buttonOpen = Button(event=None, eventArgs=[], child=canvas2, text='Bobs Inventory', textColour=(255,0,0), parent=canvas, objectPosition=(100,0))
c3 = Canvas(None, parent=canvas2, objectSize=(100,100), objectPosition=(100,0),isVisible=False, identifier='canvas3')
Canvas(None, parent=c3, objectSize=(100,100), objectPosition=(100,0),isVisible=False, identifier='canvas4')
canvas.object.h = buttonOpen.object.h 

print(canvas2.attachedObjects)

run = True
while run:
    screen.fill((0,0,0))

    pygame.display.set_caption(f'UI TEST FPS({round(clock.get_fps())}) Container Objects({screen1.numbContainers}) Parent Objects({screen1.numbParentObjs}) Child Objects({screen1.numbChildObjs})')

    events = pygame.event.get()


    for event in events:
        if event.type == pygame.QUIT:  
            run = False
    
        if event.type == pygame.KEYDOWN:

            # DEBUG
            # switches between threaded and non threaded collison detectiono
            if pygame.key.get_pressed()[pygame.K_c]:
                screen1.threadedCollisionDetection = not(screen1.threadedCollisionDetection)
                print(screen1.threadedCollisionDetection )

    screen1.update_ui(events)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()