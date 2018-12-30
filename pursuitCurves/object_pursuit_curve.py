import pyglet
import time
import json
import sys, getopt

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
            
def main( argv ):
    
    #Read command line arguments for config file
    try:
      #Get input file argument
      opts, args = getopt.getopt(argv, "hi:",["input="])
      
      if len(opts) < 1:
          print( 'Syntax: object_pursuit_curve.py -i <inputfile>' ) 
          print( 'Using default four body problem as scenario (four_body_problem.cfg)' )
          file_name = r'four_body_problem.cfg'
      
      for opt, arg in opts:
          if opt == '-h':
             print('Syntax: object_pursuit_curve.py -i <inputfile>')
             sys.exit()
          elif opt in ("-i", "--input"):
             file_name = arg
             
    except getopt.GetoptError:
      print( 'Syntax: object_pursuit_curve.py -i <inputfile>' )
      print( 'Using default four body problem as scenario (four_body_problem.cfg)' )
      file_name = r'four_body_problem.cfg'
    
    #Read config file with the description of the problem
    with open(file_name, 'r') as f:
        config = json.load( f )
        
    #Create object from the config file
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
  main( sys.argv[1:] )
  

