import pyglet
import numpy as np

import time
import threading
import random

from mover import Mover

#Generate a random color
random_color = lambda : tuple( ( random.randint(0, 255) for i in range(0, 3) ) )

class ObjectPursuit( pyglet.window.Window ):
    """
    Models a Pursuit Curve problem on a three dimensional space
    """
    key = pyglet.window.key
    
    def __init__(self, moving_objects, size, dt ):
        """
        Constructor method
        Arguments:
            moving_objects: list with moving objects where relationships of
            who is the follower and who the leader has been established            
            size: tuple of ints, size of the window            
            dt: float, step size for the time            
        """
        #Create the window
        super(ObjectPursuit, self).__init__(*size,
                                         "Two Object Pursuit Curve", 
                                         fullscreen = False, resizable=True)
        
        #delta refresh time and number of iterations
        self.dt = dt
        
        #Window position on the screen
        self.x, self.y = 0, 0
        
        #Save the follower and leader objects
        #The internal relationship between moving object has already been created
        self.moving_objects = {}
        for m in moving_objects:
            #Set random colors to each object
            self.moving_objects[ m ] = { 'color' : random_color() }
            
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
        if symbol == ObjectPursuitImage.key.ESCAPE: # [ESC]
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
        
        
class ObjectPursuitImage( ObjectPursuit ):
    """
    Models a Pursuit Curve problem on a three dimensional space
    with a fixed image
    """
    def __init__(self, moving_objects, size, dt, iterations = None, 
                 envelope = False,
                 closeness = 0.01):     

        """
        Constructor method
        Arguments:
            moving_objects: list with moving objects where relationships of
            who is the follower and who the leader has been established
            
            size: tuple of ints, size of the window
            
            dt: float, step size for the time
            
            iterations: int, number of iterations of the simulation
            
            envelope: bool, if True, lines between pursuer and leader are drawn
            so that an envelope curve is shown.
            
            closeness: float, stop iterations when the distance between
            all pursuers and leaders are smaller than closeness
            
        """
         
        #create the object
        super(ObjectPursuitImage, self).__init__(moving_objects, size, dt)
        
        self.iterations = iterations
        self.envelope = envelope
        self.closeness = closeness
        
        #Number of iterations is calculated so that if object are close enough
        #we stop calculating new iterations of the problem. Initialized to
        #the maximum number of iterations
        self.max_iter = iterations
        
    
    def render(self):     
        """
        Render the Current position of all mover objects
        """
        
        #We draw lines between pursuers and leaders, if required so that
        #the envelope line is shown in the right colors, since pixels are
        #overlapped at the envelope line
        
        #If envolving curve required, draw lines between pursuers and leaders
        if self.envelope:            
            color = (255, 255, 255)
            
            for m, attributes in self.moving_objects.items():                 
                leader = m.get_leader()
                if not leader is None:
                    #Get access to leader dictionary
                    leader_attributes = self.moving_objects[ leader ]
                    
                    for i in range(0, self.max_iter ):      
                        point_follower = attributes['points'][i]
                        point_leader = leader_attributes['points'][i]             
                        pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
                                             ('v3f', (*point_follower, *point_leader)),
                                             ('c3B',  color*2) #Define color 
                                             )
                        
                        
        #Draw all calculated points for each object as lines between
        #two consecutive states
        for m, attributes in self.moving_objects.items(): 
            
            color = attributes['color']
            
            for i in range(0, self.max_iter - 1 ):      
                point_1 = attributes['points'][i]
                point_2 = attributes['points'][i+1]             
                pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
                                     ('v3f', (*point_1, *point_2)),
                                     ('c3B',  color*2) #Define color 
                                     )
        
    
    def start(self):
        """
        Calculate all points of the simulation
        """
        self.calculate_image()
             
    def calculate_image( self ):
        """
        Calculate the all points to create the fixed image
        """        
        #For each moving object, create empty array with image data
        for m, attributes in self.moving_objects.items():
            attributes['points'] = np.zeros( (self.iterations, 3) )
            
        #Simulate each step up to max iterations or when pursuers and 
        #leader are close enough below the closeness parameter
        for i in range(0, self.iterations):
            
            #Flag to indicate all moving objects are close enough to stop simulation
            all_objects_below_closeness = True
            
            #Update mover positions
            for m in self.moving_objects:
                m.update_position( self.dt )
                
                #save location of the object at this moment of the simulation
                self.moving_objects[m]['points'][i] = m.get_position()
              
            #Check closeness between pursuers and followers
            for m in self.moving_objects:
                
                leader = m.get_leader()
                if not leader is None:
                    pursuer_position = m.get_position()
                    leader_position = leader.get_position()
                    dist = np.sqrt( np.linalg.norm( pursuer_position - leader_position ) )
                    
                    if dist > self.closeness:
                        all_objects_below_closeness = False
            
            #If pursuers and leaders are close enough, stop simulation at this point
            if all_objects_below_closeness:
                self.max_iter = i
                break                
                    
            #Recalculate follower directions
            for m in self.moving_objects:
                m.update_velocity( )

        
class ObjectPursuitCurveAnimator(ObjectPursuit, threading.Thread):
    """
    Models a Pursuit Curve problem on a three dimensional space
    with animation
    """
    
    key = pyglet.window.key
    
    def __init__(self, moving_objects, size, dt):
        
        #Create the thread
        threading.Thread.__init__(self)
        
        #Create the window
        super(ObjectPursuitCurveAnimator, self).__init__(moving_objects,
                                         size, dt)
        
  
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
    
            
def main():
    
    k = 2.0 #Speed ratio
    leader_speed = 2.0
    follower_speed = k * leader_speed
    
    #Time between movements updates on the screen
    DELTA_TIME_SECONDS = 2.0
    
    #Create the followers and leaders
    follower = Mover( "Follower A", (10, 50, 0), (0, 1, 0), follower_speed )
    leader = Mover( "Leader B", (10, 10, 0), (1, 0.25, 0), leader_speed )
    follower.set_leader( leader )
    moving_objects = [follower, leader]
   
    #Create the Pursuit Curve problem
    win_size = (250, 250)
    
    #Animation or fixed image?
    animation = False
    
    if animation:
        problem = ObjectPursuitCurveAnimator(moving_objects, 
                                        size = win_size, 
                                        dt = DELTA_TIME_SECONDS)
    else:
        problem = ObjectPursuitImage(moving_objects, 
                                        size = win_size, 
                                        dt = DELTA_TIME_SECONDS,
                                        iterations = 100,
                                        closeness = 1.5,
                                        envelope = True)
    
    #Force rendering of screen at start up
    problem.dispatch_events()
    problem.dispatch_event('on_draw')
    time.sleep( DELTA_TIME_SECONDS )
        
    #Set Frame Rate
    pyglet.clock.set_fps_limit( 20 )

    #Start the pursuit simulation    
    problem.start()
    
    #Pyglet manual Event loop    
    #there is only one window in the program
    window = list( pyglet.app.windows )[0]
    
    while True:
        pyglet.clock.tick()            
        window.dispatch_events()
        window.dispatch_event('on_draw')
        window.flip()

if __name__ == '__main__':
  main()
  

#TODO: Implement antialiasing
#TODO: define a configuration file where we can define objects
  
###References
#http://www.mat.ucm.es/cosasmdg/cdsmdg/modelizaciones/proyectos/proyecto2/index.htm
#https://fr.wikipedia.org/wiki/Courbe_du_chien
#https://en.wikipedia.org/wiki/Pursuit_curve
#http://mathworld.wolfram.com/PursuitCurve.html
