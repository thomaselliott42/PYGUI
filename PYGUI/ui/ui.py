import pygame 
import threading
import os 
import math 

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
    def __init__(self, screen, threadedCollisionDetection=True, debug=False):
        self.objectQueue = []
        self.debug = debug
        self.renderer = Renderer(screen)
        self.screen = screen
        self.actionInProgress = False
        self.threadedCollisionDetection = threadedCollisionDetection

        # DEBUG
        self.numbParentObjs = 0
        self.numbContainers = 0
        self.numbChildObjs = 0


    # Calls the render cycle  
    def ui_render(self):
        self.numbChildObjs = 0
        self.render_cycle()
    

    # Calls the collision cycle
    def ui_collisions(self):
        if self.threadedCollisionDetection:
            self.numbParentObjs = 0
            self.numbContainers = 0
            self.check_mouse_collision_threaded()
        else:
            self.numbParentObjs = 0
            self.numbContainers = 0
            self.check_mouse_object_collision()


    ''' 
    1. objectQueue -> [class] ....
    
    2. render all objects in object list:
       object -> {rectangle or text}

    3. check child objects -> [class] ....

    4. if child objects call function again 
    '''
    def check_child_objects(self, function, object):
        if object.childObjects:
            function(object.childObjects)


    def render_objects(self, object, type):
        for obj in object.objects[type]:
            if type == 'rectangle':
                self.renderer.render_rectangle(object.bgColour, obj)
            elif type == 'text':
                self.renderer.render_single_object(obj, (object.object.x, object.object.y))
            elif type == 'image':
                pass


    def render_cycle(self, objectQueue=None):
        if not objectQueue:
            objectQueue = self.objectQueue

        for object in objectQueue:
            if object.__class__ == Container:
                if object.isVisible:
                    self.check_child_objects(self.render_cycle, object)
            elif object.isVisible:
                self.numbChildObjs += 1
                for type in object.objects:
                    self.render_objects(object, type)
                self.check_child_objects(self.render_cycle, object)
    

    # Renders and Checks the objects for mouse Collision
    def update_ui(self, events=[]):
        self.cA = None
        self.numbChildObjs = 0

        if self.objectQueue:
            self.ui_render()
            if self.actionInProgress:
                self.actionInProgress = self.lastCA.get_action(events)

            else:
                self.ui_collisions()

            if self.cA:
                self.actionInProgress = self.cA.get_action(events)
                self.lastCA = self.cA


    def check_mouse_collision_threaded(self):
        self.threads = []
        self.numbParentObjs = 0
        self.numbContainers = 0

        for object in self.objectQueue:
            x = threading.Thread(target=self.check_mouse_object_collision_threaded, args=(object,))
            self.threads.append(x)
            x.start()

        for index, thread in enumerate(self.threads):
            thread.join()
    

    def check_collision(self, object, type):
        for obj in object.objects[type]:
            if type == 'rectangle':
                if object.check_mouse_collision(obj):
                    if self.debug:
                        object.bgColour = (255,192,203)
                    self.cA = object 
                elif self.debug:
                    object.bgColour = object.ogColour


    def check_mouse_child_collision_threaded(self, objectQueue):
        objectQueue.reverse()
        for object in objectQueue:
           
            if object.isVisible:
                for type in object.objects:
                    self.check_collision(object, type)
                self.check_child_objects(self.check_mouse_child_collision_threaded, object)
        objectQueue.reverse()


    def check_mouse_object_collision_threaded(self, object):
        if object.__class__ == Container:
            if object.isVisible:
                self.numbContainers += 1
                self.check_child_objects(self.check_mouse_child_collision_threaded, object)
        else:
            if object.isVisible:
                self.numbParentObjs += 1
                for type in object.objects:
                    self.check_collision(object, type)
                self.check_child_objects(self.check_mouse_child_collision_threaded, object)


    # non threaded collision checking 
    def check_mouse_object_collision(self, objectQueue=None):
        if objectQueue == None:
            objectQueue = self.objectQueue

        objectQueue.reverse()
        
        for object in objectQueue:
            if object.__class__ == Container:
                if object.isVisible:
                    self.numbContainers += 1
                    self.check_child_objects(self.check_mouse_object_collision, object)
            elif object.isVisible:
                for type in object.objects:
                    self.check_collision(object, type)
            self.check_child_objects(self.check_mouse_object_collision, object)

        objectQueue.reverse()

          
# This is how ui objects are grouped together, this is where the screen is initialised i.e ui manager 
class Container:
    def __init__(self, ui, isVisible=True):
        self.ui = ui
        self.childObjects = []
        self.ui.objectQueue.append(self)
        self.isVisible = isVisible

        # testing, used for anchoring in the future maybe 
        self.objectPosition = (100,100)
        

# Parent Class for every UI object 
class UIobjects:
    def __init__(self, objectPosition=(0,0), anchour=None, objectSize=(200,200), bgColour=(20, 50, 120),
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

        # list of ui objects  
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

    def get_action(self, events):
        for event in events:
            if pygame.mouse.get_pressed()[0]:
                print(self.identifier)
        return False


class Canvas(UIobjects):
    def __init__(self, ui, *args, **kwargs):
        super(Canvas, self).__init__(*args, **kwargs)
        self.ui = ui

        if self.parent:
            if self.parent.__class__ == Container:
                self.uiScreen = self.parent.ui.screen.get_rect()
            self.parent.childObjects.append(self)
        else:
            self.uiScreen = self.ui.screen.get_rect()
            self.ui.objectQueue.append(self)


    def transform(self, rel):
        self.object.move_ip(rel)

        self.object.clamp_ip(self.uiScreen)

        if self.childObjects:
            self.transformChildren(self.childObjects, rel)
        

    def transformChildren(self, objectQueue, rel):
        for object in objectQueue:
            for type in object.objects:
                for obj in object.objects[type]:
                    if type == 'rectangle':
                     
                        obj.move_ip(rel)
                        obj.clamp_ip(self.uiScreen)

                                
            if object.childObjects:
                self.transformChildren(object.childObjects, rel)

    
    def get_action(self, events):
        for event in events:
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
    def __init__(self, text, textColour, ui=None, isTextBackgroundVisible=True, *args, **kwargs):
        super(Label, self).__init__(*args, **kwargs)

        self.ui = ui
        self.object.w = self.get_width(text)
        self.object.h = self.font.get_height()

        self.text = text
        self.textColour = textColour

        self.textObject = self.font.render(self.text, True, self.textColour)
        self.objects['text'].append(self.textObject)

        # hack for now
        if not isTextBackgroundVisible:
            self.objects['rectangle'] = []

        if not self.identifier:
            self.identifier = text

        if self.parent:
            self.parent.childObjects.append(self)
        else:
            self.ui.objectQueue.append(self)
    

    def update_text(self, text, textColour=None):
        if textColour:
            self.textColour = textColour
        self.text = text
        
        self.textObject = self.font.render(self.text, True, self.textColour)

        # nasty hack for now 
        self.objects['text'] = [self.textObject]
        self.object.w = self.get_width(text)
        self.object.h = self.font.get_height()
             

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

    
    def get_action(self, events):
        for event in events:
            # self.angleSin += 2
            # self.angleCos += 1
            if pygame.mouse.get_pressed()[0]:
                self.child.isVisible = True
                # self.child.object.x = self.object.x + translateX(self.angleCos, 20)
                # self.child.object.y = self.object.y + translateY(self.angleSin, 20)
                # self.child.bgColour = (0,255,0)


''' 
NOT HOW BUTOTN IS GOING TO WORK 
'''
class Button(Tab):
    def __init__(self, event=None, eventArgs=[], *args, **kwargs):
        super(Button, self).__init__(*args, **kwargs)
        
        self.event = event
        self.eventArgs = eventArgs
        self.childObjects = []   
             
    
    def set_visible(self) -> None:
        self.child.isVisible = not(self.child.isVisible)
    
    
    def get_action(self, events):
        # self.event(*self.eventArgs)
        for event in events:
            if pygame.mouse.get_pressed()[0]:
                self.set_visible()
  





  

             

    

