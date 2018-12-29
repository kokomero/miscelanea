import pyglet
import time
import numpy as np

from mover import Mover
from object_pursuit_image import ObjectPursuitImage
from object_pursuit_animator import ObjectPursuitCurveAnimator

def create_problem_scenario( config ):
    """
    Given a config dict describing the problem, create the moving objects and
    their relationship as specified in the problem description file
    
    Arguments:
        config: dict containing the definition of the moving objects as well
        as other configuration parameters
    
    Returns:
        dict containing the moving objects
    """
    movers = config['movers'] #definition of the moving objects of the problem
    moving_objects = { } #dict storing all moving objects from the problem description
    
    #Create object
    for mover in movers:                
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
            
    return moving_objects
    

#Problem configuration
k = 2.0 #Speed ratio
leader_speed = 2.0
follower_speed = k * leader_speed

#Time between movements updates on the screen
DELTA_TIME_SECONDS = 6.0

#Two body problem
config_two_body = {
        'problem_name' : 'Two Object Pursuing Problem',
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
        
#Three body problem
config_three_body = {
        'problem_name' : 'Three Object Pursuing Problem forming a Triangle',
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
        
#Three body problem
config_four_body = {
        'problem_name' : 'Three Object Pursuing Problem forming a Triangle',
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
                       'r_0' : ( 210, 210, 0),
                       'v_0' : (1, 0, 0),
                       'speed' : leader_speed,
                       'leader' : 'D'
                     },
                     { 'name' : 'D',
                       'r_0' : ( 10, 210, 0),
                       'v_0' : (1, 0, 0),
                       'speed' : leader_speed,
                       'leader' : 'A'
                     }
                  ]
        }
            
def main():
    
    #Create the followers and leaders from config file
    config = config_four_body
    moving_objects = create_problem_scenario( config )
    
    #Create the Pursuit Curve problem depending on whether it is an animation
    #or a fixed image
    if config['animation']:
        problem = ObjectPursuitCurveAnimator(config['problem_name'],
                                             moving_objects, 
                                             size = config['windows_size'], 
                                             dt = config['dt'])
    else:
        problem = ObjectPursuitImage(config['problem_name'],
                                     moving_objects, 
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
    window = list( pyglet.app.windows )[0] #there is only one window in the program
    
    while True:
        pyglet.clock.tick()            
        window.dispatch_events()
        window.dispatch_event('on_draw')
        window.flip()

if __name__ == '__main__':
  main()
  

