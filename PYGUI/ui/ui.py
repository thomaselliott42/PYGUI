import pygame 
import threading
import os 
import math 

from assets.spriteSheetHandler import SpriteSheet
from rendering.renderer import Renderer

pygame.font.init()

'''
Child objects position moves relative to parent to keep in the same position  
'''

# maths for thing
def translateX(angle, radius):
    return math.cos(angle)* radius

def translateY(angle, radius):
    return math.sin(angle*-1)* radius

class UImanager:
    def __init__(self, screen, debug=False):
        self.objectQueue = []
        self.debug = debug
        self.renderer = Renderer(screen)
        self.screen = screen
        self.actionInProgress = False

        # DEBUG
        self.numbParentObjs = 0
        self.numbChildObjs = 0


    # Renders and Checks for Collision
    def ui_cycle(self):
        self.numbChildObjs = 0
        self.numbParentObjs = 0
        if self.objectQueue:
            self.ui_render()
            return self.ui_collisions()


    # Only Renders 
    def ui_render(self):
        self.numbChildObjs = 0
        self.render_objects()
    

    # Only Checks for collision
    def ui_collisions(self):
        return self.check_mouse_collisions()


    ''' 
    1. objectQueue -> [class] ....
    
    2. render all objects in object list:
       object -> {rectangle or text}

    3. check child objects -> [class] ....

    4. if child objects call function again 
    

    '''
    def render_objects(self, objectQueue=None):
        if not objectQueue:
            objectQueue = self.objectQueue

        for object in objectQueue:
            if object.isVisible:
                for type in object.objects:
                    for obj in object.objects[type]:
                        if type == 'rectangle':
                            self.renderer.render_rectangle(object.bgColour, obj)
                        elif type == 'text':
                            self.renderer.render_single_object(obj, (object.object.x, object.object.y))
                if object.childObjects:
                    self.numbChildObjs += len(object.childObjects)
                    self.render_objects(object.childObjects)
       

    def threaded_cycle(self):
        self.cA = None
        self.numbChildObjs = 0

        if self.objectQueue:
            self.ui_render()
            if self.actionInProgress:
                self.actionInProgress = self.lastCA.get_action()
            else:
                self.thread_test_thingy()
            if self.cA:
                self.actionInProgress = self.cA.get_action()
                self.lastCA = self.cA


    def thread_test_thingy(self):
        self.threads = []
        self.numbParentObjs = 0

        for object in self.objectQueue:
            x = threading.Thread(target=self.thread_test_thingy2, args=(object, 1))
            self.threads.append(x)
            x.start()

        for index, thread in enumerate(self.threads):
            thread.join()
    

    # add return back 
    def thread_test_thingy2(self, objectQueue, s):
        if not s:
            objectQueue.reverse()
            for object in objectQueue:
                for type in object.objects:
                    for obj in object.objects[type]:
                        if type == 'rectangle':
                            if object.check_mouse_collision(obj):
                                if self.debug:
                                    object.bgColour = (170, 255, 0)
                                self.cA = object 
                            else:
                                if self.debug:
                                    object.bgColour = object.ogColour
                        
                if object.childObjects:
                    self.thread_test_thingy2(object.childObjects, 0)
        else:
            self.numbParentObjs += 1
            for type in objectQueue.objects:
                for obj in objectQueue.objects[type]:
                    if type == 'rectangle':
                        if objectQueue.check_mouse_collision(obj):
                            if self.debug:
                                objectQueue.bgColour = (170, 255, 0)
                            self.cA = objectQueue 
                        else:
                            if self.debug:
                                objectQueue.bgColour = objectQueue.ogColour
                        
                if objectQueue.childObjects:
                    self.thread_test_thingy2(objectQueue.childObjects, 0)
      

    # non threaded collision checking 
    def check_mouse_collisions(self, objectQueue=None):
        if objectQueue == None:
            objectQueue = self.objectQueue

        objectQueue.reverse()
        
        if not objectQueue:
            return objectQueue
        else:
            for object in objectQueue:
                if object.isVisible:
                    for type in object.objects:
                        for obj in object.objects[type]:
                            if type == 'rectangle':
                                if object.check_mouse_collision(obj):
                                    if self.debug:
                                        object.bgColour = (170, 255, 0)
                                    object.get_action()
                                    return object 
                                else:
                                    if self.debug:
                                        object.bgColour = (20, 50, 120)
                        
                if object.childObjects:
                    return self.check_mouse_collisions(object.childObjects)




# This is how ui objects are grouped together, this is where the screen is initialised i.e ui manager 
class Container:
    def __init__(self, ui):
        self.ui = ui
        self.childObjects = []
        self.ui.objectQueue.append(self)
        

# Parent Class for every UI object 
class UIobjects:
    def __init__(self, objectPosition=(0,0), objectSize=(200,200), bgColour=(20, 50, 120),
                 font=pygame.font.Font(None, 16), parent=None, isVisible=True, isMoveable=True, identifier=None):
        self.object = pygame.Rect(objectPosition, objectSize)

        self.objects = {
            'rectangle' : [],
            'text' : [],
            'image' : []
        }

        self.objects['rectangle'].append(self.object)

        self.bgColour = bgColour
        self.font = font
        self.isMoveable = isMoveable
        self.isVisible = isVisible
        self.parent = parent
        self.identifier = identifier

        # not implemented yet 
        self.parentContainer = None
        self.parentObject = None

        self.ogColour = self.bgColour

        # class 
        self.childObjects = []
    

    def check_mouse_collision(self, obj):
        return obj.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])


    def get_width(self, text):
        line_width = 0
        space_width = self.font.size(' ')[0]
        line = []
        for word in text.split(' '):
                line_width += self.font.size(word)[0] + space_width 
                line.append(word)
               
        return line_width

    def get_action(self):
        for event in pygame.event.get():
            if pygame.mouse.get_pressed()[0]:
                print(self.identifier)
        return False


class Widget(UIobjects):
    def __init__(self, ui, *args, **kwargs):
        super(Widget, self).__init__(*args, **kwargs)
        self.ui = ui

        if self.parent:
            self.parent.childObjects.append(self)
        else:
            self.ui.objectQueue.append(self)
    

    def transform(self, rel):
        self.object.move_ip(rel)
        self.object.clamp_ip(self.ui.screen.get_rect())

        if self.childObjects:
            self.transformChildren(self.childObjects, rel)
        

    def transformChildren(self, objectQueue, rel):
        for object in objectQueue:
            for type in object.objects:
                for obj in object.objects[type]:
                    if type == 'rectangle':
                     
                        obj.move_ip(rel)
                        obj.clamp_ip(self.ui.screen.get_rect())

                                
            if object.childObjects:
                self.transformChildren(object.childObjects, rel)

    
    def get_action(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
                if self.isMoveable:
                    self.transform(event.rel)
                    return True

            elif not pygame.mouse.get_pressed()[0]:
                return False
        return True
            
        
    def create_collision_boxes(self):
        pass


'''
Used to display a word or single line of text 
'''
class Label(UIobjects):
    def __init__(self, text, textColour, ui=None, *args, **kwargs):
        super(Label, self).__init__(*args, **kwargs)

        self.ui = ui
        self.object.w = self.get_width(text)
        self.object.h = self.font.get_height()

        if self.parent:
            # make it so it checks if item in position then moves it 
            self.object.x = self.parent.object.topleft[0]
            self.object.y = self.parent.object.topleft[1] - self.object.h

        self.textObject = self.font.render(text, True, textColour)
        self.objects['text'].append(self.textObject)

        if self.parent:
            self.parent.childObjects.append(self)
        else:
            self.ui.objectQueue.append(self)
             

class ScrollBar(UIobjects):
    def __init__(self, parent, *args, **kwargs):
        super(ScrollBar, self).__init__(*args, **kwargs)

        self.object.h = parent.object.h 

        self.object.x = parent.object.topleft[0] - self.object.w
        self.object.y = parent.object.topleft[1]

        # self.object2 = Widget(None, parent=self, objectPosition=(self.object.x, self.object.y), objectSize=(self.object.w, 20), bgColour=(105,105,105), identifier='hello')
        # self.objects['rectangle'].append(self.object2.object)

        self.parent = parent
        self.parent.childObjects.append(self)
    
    
    def check_mouse_collision(self, obj):
        return obj.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])


class Tab(Label):
    def __init__(self, child, *args, **kwargs):
        super(Tab, self).__init__(*args, **kwargs)
        self.child = child
        if child != self.parent:
            self.child.isVisible = False
            self.childObjects.append(self.child)
        # self.angleSin = 0
        # self.angleCos = 0

    
    def get_action(self):
        for event in pygame.event.get():
            # self.angleSin += 2
            # self.angleCos += 1
            if pygame.mouse.get_pressed()[0]:
                self.child.isVisible = True
                # self.child.object.x = self.object.x + translateX(self.angleCos, 20)
                # self.child.object.y = self.object.y + translateY(self.angleSin, 20)
                # self.child.bgColour = (0,255,0)

