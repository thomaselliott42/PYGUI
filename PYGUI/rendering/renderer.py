import pygame

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.text_lookup_table = self.initalise_text_table()
    
    def initalise_text_table(self):
        pass
    
    def render_animated_object(self, image):
        pass

    def render_multiple_objects(self, list_images):
        for image in list_images:
            self.render_single_object(image[0], image[1])

    def render_single_object(self, image, position):
        self.screen.blit(image, position)
    
    def render_rectangle(self, bg_colour, rect):
        pygame.draw.rect(self.screen, bg_colour, rect)

    def render_text(self, text, position, font):
        self.screen.blit(font.render(text, True, (0, 255, 0), (0, 0, 128)), position)
        
        #screen.blit(font.render(text[0], text[1], text[2], text[3]), (t[4][0], t[4][1]))

    def render_ui_widget_text(self, textFormatData, font, rectangleHeight, rectangleWidth, rectanglePosition):
        
        for y, text in enumerate(textFormatData):
            if y * font.get_linesize() + font.get_linesize() > rectangleHeight:
                break
            if text[1]:
                for value in text[1]:
                    if value == 'M':
                        self.render_single_object(text[0], (rectanglePosition[0]+rectangleWidth/4, rectanglePosition[1]+(y*font.get_linesize())))
                    elif value == 'image':
                        self.render_single_object(text[0], (rectanglePosition[0]+rectangleWidth/2, rectanglePosition[1]+((y-2.5)*font.get_linesize())))
                    elif value == 'button':
                        text[0].rectangle.x, text[0].rectangle.y = rectanglePosition[0], rectanglePosition[1]+(y*font.get_linesize())
                        self.render_rectangle(text[0].bg_colour, text[0].rectangle)
                        self.render_single_object(text[0].text, (rectanglePosition[0], rectanglePosition[1]+(y*font.get_linesize())))
            else:
                self.render_single_object(text[0], (rectanglePosition[0], rectanglePosition[1]+(y*font.get_linesize())))


class Sprites(Renderer):
    def __init__(self):
        super().__init__()
        pass



