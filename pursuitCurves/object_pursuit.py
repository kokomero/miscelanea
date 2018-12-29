import pyglet
import random

#Generate a random color
random_color = lambda : tuple( ( random.randint(0, 255) for i in range(0, 3) ) )

class ObjectPursuit( pyglet.window.Window ):
    """
    Models a Pursuit Curve problem on a three dimensional space
    """
    key = pyglet.window.key
    
    def __init__(self, name, moving_objects, size, dt ):
        """
        Constructor method
        Arguments:
            name : str, problem name
            moving_objects: dict with moving objects where relationships of
            who is the follower and who the leader has been established            
            size: tuple of ints, size of the window            
            dt: float, step size for the time            
        """
        #Create the window
        super(ObjectPursuit, self).__init__(*size,
                                         name, 
                                         fullscreen = False, resizable=True)
        
        #delta refresh time and number of iterations
        self.dt = dt
        
        #Window position on the screen
        self.x, self.y = 0, 0
        
        #Save the follower and leader objects
        #The internal relationship between moving object has already been created
        self.moving_objects = {}
        for name, mover in moving_objects.items():
            
            print("Setting up configuration for object: {}".format( name ) )
            
            #Set random colors to each object
            self.moving_objects[ mover ] = { 'color' : random_color() }
            
    def __repr__(self):
        """
        String representation for moving objects of the problem
        """
        out = "#\n"

        #For each mover
        for m in self.moving_objects:
            out += str( m ) + "\n"
            
        out += "#\n"
        return out
    
    def on_key_press(self, symbol, modifiers):
        """
        Method derived from window class
        End the game when we press ESC key
        """
        if symbol == ObjectPursuit.key.ESCAPE: # [ESC]
            self.close() #Close window
            self.stop() #Stop thread
            pyglet.app.exit() #Exit application
            
    def on_close(self):
        """
        MEthod derived from window class
        """
        self.close() #Close window
        self.stop() #Stop thread
        pyglet.app.exit() #Exit application
        
    def on_draw(self):
        """
        Method derived from Window class
        """
        self.render()
        
    def stop(self):
        pass
    
    def run(self):
        """
        Main loop method for the Pursuit Curve Problem
        """
        pass