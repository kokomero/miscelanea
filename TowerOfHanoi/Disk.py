from Rectangle import Rectangle
import Hanoi

class Disk(Rectangle):
    """
    This class models a disk in the Hanoi Tower game
    Global variables for size and initial positioning are defined in the
    Hanoi package
    """
        
    def get_center_position( peg, position_on_peg):
        """
        Given the peg number and the position on that peg, get the 
        position of the center of the disk for graphical representation
        purpose
        Arguments:
            peg: peg number from 0 to 2 where the disk is located
            position_on_peg: position where the disk stays, 0 means the base
            of the playset, N_DISK is the top position on the peg
        """
        x = Hanoi.FIRST_TOWER_X + peg * Hanoi.DISTANCE_BETWEEN_TOWER
        y = position_on_peg * Hanoi.DISK_HEIGHT + 0.5 * Hanoi.DISK_HEIGHT
        return (x, y)
    
    def __init__(self, size, color):
        """
        Create a disk
        Arguments:
            size: size of the disk from 1 to n
            color: (R, G, B) 3-tuple with the color
        """        
        #Define dimensions for the disk
        self.size = size
        height = Hanoi.DISK_HEIGHT
        wide = size * Hanoi.RADIUS_MULT
        
        #Initially we place all disks in peg 1, ordered by their size
        #Position 0 means the base of the play set
        self.peg = 0
        self.position_on_peg = Hanoi.N_DISK - size        
        center = Disk.get_center_position( self.peg, self.position_on_peg)        
        
        #Create the graphic object calling Rectangle constructor
        super().__init__(center, wide, height, color)    
        
    def get_position_on_game(self):
        """
        Return a tuple (peg_number, position_on_peg) where the disk is 
        staying on the game. 
        """
        return (self.peg, self.position_on_peg)
        
    def move(self, num_tower, position):
        """
        Move the disk to the given tower, and set it in a given position
        """
        #Keep track of the location of the disk
        self.peg = num_tower
        self.position_on_peg = position
        
        #Change coordenates in graphical representation of the disk
        #Calling base clase move method
        super().move( Disk.get_center_position( num_tower, position) )
        
    def __repr__(self):        
        """
        String representation for the play board
        """
        out = f"Disk: peg: {self.peg} size: {self.size} "
        out += f"position on peg: {self.position_on_peg}"
        return out   