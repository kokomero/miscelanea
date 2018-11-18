import pyglet

class Rectangle:
    """
    Rectangle graphic component. 
    (x,y) represents the center of rectangle, w the wide and h the height. 
    """
    def __init__(self, center, w, h, color):
        """
        Create a Rectangle.
        Arguments:
            center: tuple contanining the coordinates for the center
            w: wide
            h: height
            color: a 3-tuple with the RGB levels
        """
        self.center = center
        self.wide = w
        self.height = h
        self.color = color
        self.calculate_vertex()
    
    def draw(self):
        """
        Draws the rectangle on the screen using pyglet framework
        """
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, 
                             self._quad, #Define positions
                             ('c3B', self.color*4 ) #Define colors
                             ) 
    
    def calculate_vertex(self):
        """
        Calculate the vertex for this rectangle
        """
        wide = self.wide
        height = self.height
        center = self.center
        p1 = ( center[0] - wide / 2.0, center[1] + height / 2.0 )
        p2 = ( center[0] - wide / 2.0, center[1] - height / 2.0 )
        p3 = ( center[0] + wide / 2.0, center[1] - height / 2.0 )
        p4 = ( center[0] + wide / 2.0, center[1] + height / 2.0 )
        self._quad = ('v2f', ( *p1, *p2, *p3, *p4) )
        
    def move(self, center):
        """
        Move the rectangle to the given position
        Arguments:
            center: tuple containing the coordinates for the center
        """
        self.center = center
        self.calculate_vertex()        
    
    def __repr__(self):
        """
        str representation of the rectangle
        """
        p1 = f"p1=({self._quad[1][0]}, {self._quad[1][1]})"
        p2 = f"p2=({self._quad[1][2]}, {self._quad[1][3]})"
        p3 = f"p3=({self._quad[1][4]}, {self._quad[1][5]})"
        p4 = f"p4=({self._quad[1][6]}, {self._quad[1][7]})"        
        return f"Rect( {p1}, {p2}, {p3}, {p4} )"