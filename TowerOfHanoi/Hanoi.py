import pyglet
import random
import numpy as np
import time
import threading

from Rectangle import Rectangle
import Disk

#Global variables
N_DISK = 6          #Number of disk of the Tower of Hanoi game
DISK_HEIGHT = 25    #Disk Height, for graphical representation, in pixels
RADIUS_MULT = 20    #Multiplier for radius of Disk n

#Define the distance between two pegs
DISTANCE_BETWEEN_TOWER = N_DISK * RADIUS_MULT * 1.0 * 1.5

#X position of the first tower
FIRST_TOWER_X = N_DISK * RADIUS_MULT * 1.05

#Time between movements updates on the screen
DELTA_TIME_SECONDS = 0.7
         
class HanoiTower(pyglet.window.Window, threading.Thread):
    """
    Models a Tower of Hanoi playset, with 3 pegs and n disks
    """    
    key = pyglet.window.key

    def __init__(self, n_disk):
        """
        Create a Tower of Hanoi object with n_disk
        Arguments:
            n_disk: number of disks of the game
            window: Graphical windows where the game will be displayed
        """        
        #Define window size
        window_size = (int( FIRST_TOWER_X + 2.5 * DISTANCE_BETWEEN_TOWER ), 
                       int( N_DISK * DISK_HEIGHT + 5.0 * DISK_HEIGHT) )
        
        #Create the thread
        threading.Thread.__init__(self)
        
        #Create the window
        super(HanoiTower, self).__init__(*window_size,
                                         "Towers of  Hanoi", 
                                         fullscreen = False, resizable=True)
        
        #Window position on the screen
        self.x, self.y = 0, 0
        
        #Number of disk of the game
        self.n_disk = n_disk
        
        #The game has three towers, each tower n_disk possible positions
        self.towers = np.zeros( (3, n_disk), dtype = np.int)

        #Put all disks in the first column
        self.towers[0] = list( reversed( range(1, n_disk + 1) ) )
        
        #Create disk objects with random colors
        random_color = lambda : tuple( ( random.randint(0, 255) for i in range(0, 3) ) )
        self.disks = [ Disk.Disk(size = i, color = random_color() ) 
                        for i in range(1, n_disk + 1) ]
            
        #Create pegs (graphical objects)
        peg_color = (255, 255, 255)
        center_y = DISK_HEIGHT * ( n_disk + 1.0 ) / 2.0 + DISK_HEIGHT
        peg_center = lambda i : (FIRST_TOWER_X + i * DISTANCE_BETWEEN_TOWER, center_y)
        self.pegs = [ Rectangle( center = peg_center(i),
                                    w = RADIUS_MULT * 0.5,
                                    h = (n_disk + 3.0 ) * DISK_HEIGHT ,
                                    color = peg_color ) for i in range(0,3) ]

    
    def get_top_for_peg(self, peg_number):
        """
        Return the top position for the peg. The top position is the first 
        empty position. If the tower is full, NDISK is returned.
        Arguments:
            peg_number: index of the peg for which we want to know the top position
        Returns:
            index of the top position (non-occupied by a disk) for the given peg
        """
        #Look for the first zero-entry of the self.towers array for a given
        #peg number
        index_for_empty_disk = np.where( self.towers[ peg_number ] == 0)
        
        #If the index is empty, the peg is full of disks, otherwise
        #return top available position on the peg
        if index_for_empty_disk[0].size == 0:
            return self.n_disk
        else:
            return index_for_empty_disk[0][0]
            
    def move_disk_to_peg(self, disk, destination_peg):
        """
        Move a disk to a given peg, placing in on the top of the peg
        Update internal data of both the Disk and the Tower of Hanoi object
        to keep track of every position in the game
        Arguments
            disk: disk object to be moved
            destination_peg: index with the peg where the disk will
            be moved. It should be an integer within the range [0,2]
        Returns:
            None, internal states updated
        """
        #Update screen and Insert a pause before next movement
        print( self )
        time.sleep( DELTA_TIME_SECONDS )
        
        #Get the position on the destination peg
        position_on_destination = self.get_top_for_peg( destination_peg )
        
        #Get initial position for the disk
        (init_tower, init_position ) = disk.get_position_on_game()
        
        #Update the disks positions
        self.towers[ init_tower ][ init_position ] = 0
        self.towers[ destination_peg ][ position_on_destination ] = disk.size
        
        #Update disk internal state
        disk.move(destination_peg, position_on_destination)  
        
    def move_tower(self, disk, source, destination, spare):
        """
        Recursive algorithm for the Hanoi Tower
        Arguments:
            disk: disk object representing the disk to be moved
            source: source peg, index 0 on the initial solution
            destination: destination peg, index 1 initial solution
            spare: spare peg, index 2 on the initial solution
        """                
        if self.thread_running == False:
            raise Exception('Thread aborted')
        
        if disk.size == 1:
            self.move_disk_to_peg(disk, destination)  
        else:
            next_disk_to_move = self.disks[ disk.size - 2]
            self.move_tower( next_disk_to_move, source, spare, destination )
            self.move_disk_to_peg(disk, destination)
            self.move_tower( next_disk_to_move, spare, destination, source )
        
    def __repr__(self):
        """
        String representation for the play board
        """
        out = "#\n"

        #For each column, print the disk
        for i in range(0, 3):
            column = self.towers[i]
            disks_str = "-".join( [ '{:d}'.format( i ) for i in column.tolist() ] )
            out += r"#|" + disks_str + "\n"

        out += "#\n"
        return out    
    
    def on_key_press(self, symbol, modifiers):
        """
        Method derived from window class
        End the game when we press ESC key
        """
        if symbol == HanoiTower.key.ESCAPE: # [ESC]
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
        
    def render(self):     
        """
        Render the Hanoi Tower play set on the screen
        """
        #Clean the screen
        self.clear()

        #Draw pegs
        for c in self.pegs:
            c.draw()
            
        #Draw each disk
        for d in self.disks:
            d.draw()

    def stop(self):
        """
        Signal the thread to stop
        """
        self.thread_running = False
        
    def run(self):
        """
        Main loop method for the Tower of Hanoi Thread
        """
        #Signal the thread as running
        self.thread_running = True
  
        #Print Initial position
        print( self )
        
        #Next step in the game
        self.move_tower(self.disks[N_DISK - 1], 0, 1, 2)
        
    
# main function
if __name__ == '__main__':
    """
    Create a game and let it play.
    Application exits when pressing ESC key or closing window
    """
    #Create Game
    game = HanoiTower( N_DISK )
    
    #Force rendering of screen at start up
    game.dispatch_events()
    game.dispatch_event('on_draw')
    time.sleep( DELTA_TIME_SECONDS )
    
    #Start game, spwaning the game thread
    game.start()
    
    #Pyglet manual Event loop
    while True:
        pyglet.clock.tick()
    
        for window in pyglet.app.windows:
            window.switch_to()
            window.dispatch_events()
            window.dispatch_event('on_draw')
            window.flip()
        
    
         
    