import numpy as np

class Mover(object):    
    """
    This class models a mover in a 3-dimensional space, i.e. an object which moves
    The internal state is represented by:
        - r: tuple with the position (r_x, r_y, r_z)
        - v: velocity vector (v_x, v_y, v_z)
        - speed: float with the speed of the object
        - name: str with the name of the object for representational purpose
        - leader: object we are pursuing, if any
        - followers: list of object following us.
        
    """    
    def __init__(self, name, r0, v0, speed):
        """
        Constructor for the class
        Arguments
            - name: str with the name of the object for representational purposes
            - r0: initial position, as a 3-tuple
            - v0: initial velocity, as a 3-tuple. The vector will be normalized
            only direction is considered
            - speed: constant speed, as a float
        """
        
        self.name = name
        self.r = np.array( r0, dtype=np.float )
        
        #Normalize velocity vector
        velocity = np.array( v0, dtype=np.float )
        self.v = velocity / np.linalg.norm( velocity )
        
        #Scale by speed
        self.speed = speed
        self.v = self.v * self.speed
        
        #Feader of this object, if any
        self.leader = None        
        
    def get_name(self):
        """
        Return the name of the object
        """
        return self.name
    
    def get_position(self):
        """
        Return the position of the object
        """
        return self.r
        
    def set_leader(self, leader):
        """
        Set the leader moving object we are pursuing
        """
        self.leader = leader
        
    def get_leader(self):
        """
        Return the object we are pursuing
        """
        return self.leader
        
    def update_position(self, delta_t):
        """
        Update the position of the object according to the velocity vector
        and a delta_t time 
        """
        self.r = self.r + self.v * delta_t
        
    def update_velocity(self):
        """
        Update the velocity vector of the object
        If we have a leader, the direction of the velocity vector is such that
        the follower is always pursuing the leader in the shortest path 
        direction.
        
        If we do not have a leader, just follow the initial velocity vector
        """        
        if not self.leader is None:   
            direction = self.leader.get_position() - self.r
            self.v = direction / np.linalg.norm( direction ) * self.speed
        
    def __repr__(self):
        """
        String representation of this object
        """
        r_str = "({:f}, {:f}, {:f})".format( *self.r )
        v_str = "({:f}, {:f}, {:f})".format( *self.v )
        s_str = "{:f}".format( self.speed )
        out = "{} --> pos: {}, vel: {}, Speed: {}".format(self.name, 
                                                        r_str, 
                                                        v_str, 
                                                        s_str)
        return out
        
def main():  
    #Create a follower and a Leader and define relationship
    follower = Mover( "Follower A", (1, 0, 0), (0, 1, 0), np.sqrt(2.0) )
    leader = Mover("Leader B", (0, 1, 0), (0, 1, 0), 1.0 )
    follower.set_leader( leader )
    
    iterations = 10
    
    #Moving object list
    moving_objects = [follower, leader]
    
    #For each object
    for m in moving_objects:        
        #Print initial state
        print("Initial state: ", m )
    
    print(  )
    
    for i in range(0, iterations):
        
        for m in moving_objects:            
            #Update velocities        
            m.update_velocity()

            #Print state
            print("Updated state: ", m )
            
            #Update positions        
            m.update_position( 1.0 )
        
        print(  )

    
if __name__ == '__main__':
  main()