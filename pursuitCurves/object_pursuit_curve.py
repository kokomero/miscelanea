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
            moving_objects: dict with moving objects where relationships of
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
            
            pyglet.gl.glLineWidth( 0.5 )
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
        pyglet.gl.glLineWidth( 3.0 )
        for m, attributes in self.moving_objects.items(): 
            
            color = attributes['color']
            
            for i in range(0, self.max_iter - 1):      
                point_1 = attributes['points'][i]
                point_2 = attributes['points'][i+1]             
                pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
                                     ('v3f', (*point_1, *point_2)),
                                     ('c3B',  color*2) 
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
        #For each moving object, create empty array with image data where
        #the simulated positions will be stored
        for m, attributes in self.moving_objects.items():
            attributes['points'] = np.zeros( (self.iterations, 3) )
            
        #Simulate each step up to max iterations or when pursuers and 
        #leader are close enough below the closeness parameter
        for i in range(0, self.iterations):
            
            #Flag to indicate all moving objects are close enough to stop simulation
            all_objects_below_closeness = True
            
            #Check closeness between pursuers and followers
            for m in self.moving_objects:
                
                leader = m.get_leader()
                if not leader is None:
                    pursuer_position = m.get_position()
                    leader_position = leader.get_position()
                    dist = np.sqrt( np.linalg.norm( pursuer_position - leader_position ) )
                    
                    if dist > self.closeness:
                        all_objects_below_closeness = False
            
            #Update movers positions
            for m in self.moving_objects:
                m.update_position( self.dt )
                
                #save location of the object at this moment of the simulation
                self.moving_objects[m]['points'][i] = m.get_position()
              
            #If pursuers and leaders are close enough, stop simulation at this point
            if all_objects_below_closeness:
                self.max_iter = i
                break           
                    
            #Recalculate follower directions for next iteration
            for m in self.moving_objects:
                m.update_velocity( )

        
class ObjectPursuitCurveAnimator(ObjectPursuit, threading.Thread):
    """
    Models a Pursuit Curve problem on a three dimensional space
    with animation
    """
    
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
    
    #Problem configuration
    k = 2.0 #Speed ratio
    leader_speed = 2.0
    follower_speed = k * leader_speed
    
    #Time between movements updates on the screen
    DELTA_TIME_SECONDS = 6.0
    
    #config dict to be exported as a json file
    #TODO: Move line width and colors to the configuration file
    
    #Two body problem
    config_two_body = {
            'dt' : DELTA_TIME_SECONDS,
            'windows_size' : (400, 400),
            'animation' : False,
            'iterations' : 1000,
            'closeness' : DELTA_TIME_SECONDS,
            'envelope' : True,
            'frame_per_second' : 20,
            'movers' : [
                         { 'name' : 'Follower A',
                           'r_0' : (10, 250, 0),
                           'v_0' : (0, 1, 0),
                           'speed' : follower_speed,
                           'leader' : 'Leader B'
                         },
                         { 'name' : 'Leader B',
                           'r_0' : (10, 10, 0),
                           'v_0' : (1, 0.25, 0),
                           'speed' : leader_speed,
                           'leader' : None
                         }
                      ]
            }
            
    #Two body problem
    config_three_body = {
            'dt' : DELTA_TIME_SECONDS,
            'windows_size' : (400, 400),
            'animation' : False,
            'iterations' : 1000,
            'closeness' : DELTA_TIME_SECONDS / 2,
            'envelope' : True,
            'frame_per_second' : 20,
            'movers' : [
                         { 'name' : 'A',
                           'r_0' : (10, 10, 0),
                           'v_0' : (1, 0, 0),
                           'speed' : leader_speed,
                           'leader' : 'B'
                         },
                         { 'name' : 'B',
                           'r_0' : (210, 10, 0),
                           'v_0' : (1, 0, 0),
                           'speed' : leader_speed,
                           'leader' : 'C'
                         },
                         { 'name' : 'C',
                           'r_0' : ( 200 / 2 + 10, 10 + 200 * np.sqrt(3) / 2.0 , 0),
                           'v_0' : (1, 0, 0),
                           'speed' : leader_speed,
                           'leader' : 'A'
                         }
                      ]
            }
            
    
    #Create the followers and leaders from config file
    config = config_three_body
    movers = config['movers']
    moving_objects = { }
    
    for mover in movers:        
        #Create object
        mover_obj = Mover( name = mover['name'], 
                      r0 = mover['r_0'], 
                      v0 = mover['v_0'], 
                      speed = mover['speed'] )
        
        #Store in the moving object dict
        moving_objects[ mover_obj.get_name() ] = mover_obj
 
    #Create pursuer-leader relationships
    for m in movers:
        name = m['name']
        leader_name = m['leader']
        if not leader_name is None:      
            leader = moving_objects[ leader_name ]
            moving_objects[ name ].set_leader( leader )
    
   
    #Create the Pursuit Curve problem depending on whether it is an animation
    #or a fixed image
    if config['animation']:
        problem = ObjectPursuitCurveAnimator(moving_objects, 
                                        size = config['windows_size'], 
                                        dt = config['dt'])
    else:
        problem = ObjectPursuitImage(moving_objects, 
                                        size = config['windows_size'], 
                                        dt = config['dt'],
                                        iterations = config['iterations'],
                                        closeness = config['closeness'],
                                        envelope = config['envelope'] )
    
    #Force rendering of screen at start up
    problem.dispatch_events()
    problem.dispatch_event('on_draw')
    time.sleep( config['dt'] )
        
    #Set Frame Rate
    pyglet.clock.set_fps_limit( config['frame_per_second'] )

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
  

