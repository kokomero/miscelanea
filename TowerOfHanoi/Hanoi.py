import pyglet
import random
import numpy as np

N_DISC = 8
DISC_HEIGHT = 25
RADIUS_MULT = 20
DISTANCE_BETWEEN_TOWER = N_DISC * RADIUS_MULT * 1.0 * 1.5
FIRST_TOWER_X = N_DISC * RADIUS_MULT * 1.05
 
class Rectangle:
    
    """
    Graphic rectangle. (x,y) represents the center of rectangle, w the wide
    and h the height. 
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
        Draws the rectangle on the screen
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
    
class Disc(Rectangle):
    """
    This class models a disc in the Hanoi Tower game
    """
        
    def __init__(self, size, color):
        """
        Create a disc
        Arguments:
            n_disc: number of the disc
            size: size of the disc from 1 to n
            color: (R, G, B) 3-tuple with the color
        """        
        #Define dimensions
        height = DISC_HEIGHT
        wide = size * RADIUS_MULT
        center = (0, 0)  
        
        #Create the graphic object
        super().__init__(center, wide, height, color)
        
    def move(self, num_tower, position):
        """
        Move the disc to the given tower, and set it in a given position
        """
        x_position = FIRST_TOWER_X + num_tower * DISTANCE_BETWEEN_TOWER
        y_position = position * DISC_HEIGHT + 0.5 * DISC_HEIGHT
        super().move( (x_position, y_position) )

    
class HanoiTower(pyglet.window.Window):
    """
    Models a Tower of Hanoi playset, with 3 columns and n discs
    """
    
    key = pyglet.window.key

    def __init__(self, n_disc):
        """
        Create a Tower of Hanoi object with n_disct
        Arguments:
            n_disc: number of discs of the game
            window: Graphical windows where the game will be displayed
        """        
        #Define window size
        window_size = (FIRST_TOWER_X + 2.5 * DISTANCE_BETWEEN_TOWER, 
                       N_DISC * DISC_HEIGHT + 5.0 * DISC_HEIGHT)
        window_size = tuple( map( lambda x : int( x ), window_size ) )
        super(HanoiTower, self).__init__(*window_size,
                                         "Towers of  Hanoi", 
                                         fullscreen = False, resizable=True)
        self.x, self.y = 0, 0
        
        #Number of disc of the game
        self.n_disc = n_disc
        
        #The game has three towers, each tower n_disc possible positions
        self.towers = np.zeros( (3, n_disc), dtype = np.int)

        #Put all discs in the first column
        tower_order = np.linspace(n_disc, 1, n_disc)
        self.towers[0] = tower_order
                
        #dict with position of each disc
        self.positions = { i : (0, i) for i in tower_order - 1 }
        
        #Create disc objects
        random_color = lambda : tuple( ( random.randint(0, 255) for i in range(0,3) ) )
        self.discs = [ Disc(size = i, color = random_color() ) for i in tower_order ]
        
        #Set discs object at initial position of the game
        for (i, disc) in enumerate( self.discs ):
            disc.move( 0, i )
            
        #Create columns
        column_color = (255, 255, 255)
        height = n_disc * DISC_HEIGHT + 1.0 * DISC_HEIGHT
        self.columns = [ Rectangle( center = (FIRST_TOWER_X + i * DISTANCE_BETWEEN_TOWER, height / 2.0 + DISC_HEIGHT),
                                    w = RADIUS_MULT * 0.5,
                                    h = n_disc * DISC_HEIGHT + 3.0 * DISC_HEIGHT,
                                    color = column_color ) for i in range(0,3) ]

            
    def __repr__(self):
        """
        String representation for the play board
        """
        out = "#\n"

        #For each column, print the disc
        for i in range(0, 3):
            column = self.towers[i]
            discs_str = "-".join( [ '{:d}'.format( i ) for i in column.tolist() ] )
            out += r"#|" + discs_str + "\n"

        out += "#\n"
        return out    
    
    def on_key_press(self, symbol, modifiers):
        """
        Method derived from window class
        End the game when we press ESC key
        """
        if symbol == HanoiTower.key.ESCAPE: # [ESC]
            self.close() #Close window
            pyglet.app.exit() #Exit application
            
    def on_close(self):
        """
        MEthod derived from window class
        """
        self.close() #Close window
        pyglet.app.exit() #Exit application
        
    def on_draw(self):
        """
        Method derived from Window class
        """
        self.render()
        
    def render(self):     
        """
        Render the Hanoi Tower play set on the screen
        """
        #Clean the screen
        self.clear()

        #Draw columns
        for c in self.columns:
            print( c )
            c.draw()
            
        #Draw each disc
        for d in self.discs:
            d.draw()
            
    def next_step(self, args):
        """
            Next step in the game
        """
        random_tower = random.randint(0, 2)
        random_position = random.randint(0, self.n_disc)
        random_disc = random.randint(0, self.n_disc - 1)
        self.discs[random_disc].move(random_tower, random_position)
    
    def run(self):
        """
        Main loop method
        """
        #Next step in the game
        pyglet.clock.schedule_interval(self.next_step , 2.0) 
        
        #Run the game
        pyglet.app.run()
        
        
        
    
# main function
if __name__ == '__main__':
    """
    Create a game and let it play.
    Application exits when pressing ESC key or closing window
    """

    #Create Game
    game = HanoiTower( N_DISC )
    
    game.run()
         
    