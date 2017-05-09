import numpy as np

class Graphic():

    def __init__(self):
        pass

    def draw(self, canvas, position, fit_to_size=None):
        pass

    
'''
White box placeholder
'''
class PlaceholderGraphic(Graphic):

    width = 80
    height = 40
    
    def __init__(self, title):
        self.title = title
        
    def contains_position(self, position):
        if self.position[0] <= position[0] <= self.position[2]:
            if self.position[1] <= position[1] <= self.position[3]:
                return True
        return False
    
    def draw(self, canvas, position, fit_to_size=None):
        self.center = position
        width = self.width
        height = self.height
        
        if fit_to_size is not None:
            #Expand or shrink to fit width:
            if fit_to_size[0] != width:
                ratio = fit_to_size[0] / float(width)
                width = width*ratio
                height = height*ratio

            #Shrink to fit heigh:
            if fit_to_size[1] < height:
                ratio = fit_to_size[1] / float(height)
                width = width*ratio
                height = height*ratio
                
        xmin = position[0] - width / 2
        xmax = position[0] + width / 2
        ymin = position[1] - height / 2
        ymax = position[1] + height / 2

        self.position = (xmin, ymin, xmax, ymax)

        canvas.create_rectangle(xmin,ymin,xmax,ymax)
        canvas.create_text(position[0], position[1], text=self.title)

        #Test:
        #l = Link(self)
        #l.draw_from_parent(canvas, [0,-self.height/2])
        
class LinkBall(Graphic):

    link_radius = 6
        
    def draw(self, canvas, position, fit_to_size=None):
        self.center = position
        self.__create_circle(canvas, position[0], position[1], self.link_radius)

    def __create_circle(self, canvas, x, y, r):
        canvas.create_oval(x-r, y-r, x+r, y+r, fill='black')

    def contains_position(self, position):
        return (position[0] - self.center[0])**2 + (position[1] - self.center[1])**2 <= self.link_radius**2

class EdgeLine(Graphic):

    def __init__(self, out_socket, in_socket):
        self.out_socket = out_socket
        self.in_socket = in_socket

    def draw(self, canvas):
        canvas.create_line(self.out_socket.get_position()[0],
                           self.out_socket.get_position()[1],
                           self.in_socket.get_position()[0],
                           self.in_socket.get_position()[1])

    # TODO
    def contains_position(self, position):
        return False
