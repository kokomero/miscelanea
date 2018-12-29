import threading
import pyglet

from object_pursuit import ObjectPursuit

class ObjectPursuitCurveAnimator(ObjectPursuit, threading.Thread):
    """
    Models a Pursuit Curve problem on a three dimensional space
    with animation
    """
    
    def __init__(self, name, moving_objects, size, dt):
        
        #Create the thread
        threading.Thread.__init__(self)
        
        #Create the window
        super(ObjectPursuitCurveAnimator, self).__init__(name, 
                                         moving_objects,
                                         size, 
                                         dt)
        
  
    def render(self):     
        """
        Render the Current position of all mover objects
        """
        #Draw each object as points
        for m, attributes in self.moving_objects.items():            
            pyglet.graphics.draw(1, pyglet.gl.GL_POINTS,
                                 ('v3f', m.get_position()),
                                 ('c3B', attributes['color'] ) #Define color
                                 )
            
        #Print representation
        #print( self )
    
    def stop(self):
        """
        Signal the thread to stop
        """
        self.thread_running = False
        
    
    def next_step( self, args =  None ):
        """
        Calculate the next step in the game
        """        
        #Update mover positions
        for m in self.moving_objects:
            m.update_position( self.dt )
                
        #Recalculate follower directions
        for m in self.moving_objects:
            m.update_velocity( )
                
    def run(self):
        """
        Main loop method for the Pursuit Curve Problem
        """
        #Signal the thread as running
        self.thread_running = True
  
        #Print Initial position
        print( self )
        
        #Call back function to be called every refresh
        pyglet.clock.schedule_interval(self.next_step, self.dt )   