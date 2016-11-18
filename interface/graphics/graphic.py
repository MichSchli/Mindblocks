class Graphic():

    def __init__(self):
        pass

    def draw(self, canvas, position, fit_to_size=None):
        pass

'''
White box placeholder
'''
class Placeholder(Graphic):

    width = 80
    height = 40
    
    def __init__(self, title):
        self.title = title

    def copy(self):
        return Placeholder(self.title)
        
    def contains_position(self, position):
        if self.position[0] <= position[0] <= self.position[2]:
            if self.position[1] <= position[1] <= self.position[3]:
                return True
        return False
        
    def draw(self, canvas, position, fit_to_size=None):
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

        #TODO: offset for no reason
        canvas.create_rectangle(xmin,ymin-5,xmax,ymax-5)
        canvas.create_text(position[0], position[1]-5, text=self.title)

        
