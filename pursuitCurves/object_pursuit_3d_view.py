import pyglet
import numpy as np

from pyglet.gl import *
from OpenGL.GLUT import *

from object_pursuit import ObjectPursuit

INCREMENT = 5

class ObjectPursuit3DView( ObjectPursuit ):
    """
    Models a Pursuit Curve problem on a three dimensional space
    with a fixed image
    """
    
    # Cube 3D start rotation
    xRotation = yRotation = zRotation = 0
   
    def __init__(self, name, moving_objects, size, dt, iterations = None, 
                 envelope = False,
                 closeness = 0.01):     

        """
        Constructor method
        Arguments:
            name: str, name of the problem
            
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
        super(ObjectPursuit3DView, self).__init__(name, moving_objects, size, dt)
        
        self.iterations = iterations
        self.envelope = envelope
        self.closeness = closeness
        
        #Number of iterations is calculated so that if object are close enough
        #we stop calculating new iterations of the problem. Initialized to
        #the maximum number of iterations
        self.max_iter = iterations
        

    def on_key_press(self, symbol, modifiers):
        """
        Method derived from window class
        End the game when we press ESC key
        """
        if symbol == ObjectPursuit3DView.key.ESCAPE: # [ESC]
            self.close() #Close window
            self.stop() #Stop thread
            pyglet.app.exit() #Exit application
        elif symbol == ObjectPursuit3DView.key.UP:
            self.xRotation += INCREMENT
        elif symbol == ObjectPursuit3DView.key.DOWN:
           self.xRotation -= INCREMENT
        elif symbol == ObjectPursuit3DView.key.LEFT:
           self.zRotation -= INCREMENT
        elif symbol == ObjectPursuit3DView.key.RIGHT:
           self.zRotation += INCREMENT
        elif symbol == ObjectPursuit3DView.key.PAGEUP:
            self.yRotation += INCREMENT
        elif symbol == ObjectPursuit3DView.key.PAGEDOWN:
            self.yRotation -= INCREMENT
            
    def on_draw(self):
        """
        Method derived from Window class
        """
        
        # Clear the current GL Window
        self.clear()
        
        # Push Matrix onto stack
        pyglet.gl.glPushMatrix()
        pyglet.gl.glRotatef(self.xRotation, 1, 0, 0)
        pyglet.gl.glRotatef(self.yRotation, 0, 1, 0)
        pyglet.gl.glRotatef(self.zRotation, 0, 0, 1)
        
        self.render()
       
        # Pop Matrix off stack
        pyglet.gl.glPopMatrix()
        
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
