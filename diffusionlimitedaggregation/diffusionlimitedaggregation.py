import Image
import colour
import random
import argparse
from progressbar import *

#TODO:
#See other nice ideas at http://bit-player.org/
#Define adjacency matrix for the next move and for neighbourhood check
#so that we can generate different brownian tree configuration

#the adjacency matrix for movements and neighbourhood check
adjacency = [(i,j) for i in (-1,0,1) for j in (-1,0,1) if not (i == j == 0)] 

#Number of colors for the image
nColors = 100

#Number of steps in the progress bar
steps = 100

#Create parser for command line arguments
def getCommandLineParser():
	parser = argparse.ArgumentParser(description='Paint a brownian tree using Diffusion Limited Aggregtion simulation.')
	parser.add_argument('-s', default='200', help='Create an image of size x size pixels', type=int)
	parser.add_argument('-n', default='2000', help='Number of particles to simulate', type=int)
	parser.add_argument('-p', help='Fraction of particles of the total number of pixel on the image', type=float, required=False)
	parser.add_argument('-o', help='File name to save the image (.png)', type=str, required=False)	
	parser.add_argument('-f', default='bottom', help='Frame shape where particles can stick: [bottom|square|circle|origin]', type=str, required=False)	
	return parser
  
#Move randomly a particle in a given position
#Do not bounce on image limits
def moveParticle(position, size):
	(x, y) = position
	(dx, dy) = adjacency[ random.randrange(0, 8) ]
	if( 0 <= x + dx < size ):
		x = x + dx
	if( 0 <= y + dy < size ): 
		y = y + dy
	return (x, y)	

#Define initial frame where particle can stick 
def paintFrame(pixels, size, frame):
	
	blank = (255, 255, 255)
	if frame == 'bottom':
		for i in range(0, size):
			pixels[i, 0] = blank
						
	elif frame == 'square':
		for i in range(0, size):
			pixels[i, 0] = blank
			pixels[i, size - 1] = blank
			pixels[0, i] = blank
			pixels[size - 1, i] = blank
			
	elif frame == 'circle':
		for i in range(0, size):
			for j in range(0, size):
				if (i - size/2)**2 + (j - size/2)**2 >= (size / 2)**2:
					pixels[i, j] = blank
	
	elif frame == 'origin':
		origin_size = 10
		for i in range(0, origin_size):
			for j in range(0, origin_size):
				if (i - size/2)**2 + (j - size/2)**2 <= (origin_size / 2)**2:
					pixels[i, j] = blank
	else:
		raise Exception("Frame type parameter [bottom|square|circle|origin]")

#Check if there is an adjacent particle where we can stick
def adjacentParticle(pixels, size, position):	
	x = position[0]
	y = position[1]
	
	#If are already on a particle, we cannot stick on the same place
	if pixels[x, y] != (0,0,0):
		return False
	
	#Look for adjacent pixels to see if they are non-black
	for dx, dy in adjacency:
		if (0 <= x + dx < size) and (0 <= y + dy < size):
			if pixels[x + dx, y + dy] != (0,0,0):
				return  True
	
	return False	
	
#Simulation of DLA by randomly creating a new particle in free positions
#and then apply a brownian motion on it until hitting another particle
def normalSimulation(pixels, n_particles, image_size, colors):
	
	nColors = len( colors )
	void_pixel = (0,0,0)

	#List of free positions where new particles can start the random walk
	free_points = set()
	for x in range(0, image_size):
		for y in range(0, image_size):
			if pixels[x,y] == void_pixel:
				free_points.add( (x, y) ) 
							
	#Set up a progress bar to show calculations
	bar = ProgressBar(maxval=steps, widgets=[Bar('=', '[', ']'), ' ', Percentage()])
	bar.start()
	
	#Iterate over all n particles
	for i in range(1, n_particles):
		
		#Get initial position from an empty point
		position = random.sample( free_points, 1)[0]
		
		#Color index depending on the time particle was created
		colorIndex = int( float(i) / n_particles * nColors )
		color = tuple( [ int(j*255) for j in colors[colorIndex].rgb ] )
		
		#Apply brownian motion until we hit another particle
		while not adjacentParticle(pixels, image_size, position): 
			position = moveParticle(position, image_size)
		else:
			pixels[ position[0], position[1] ] = color
			
		#Remove this new position from the set of empty points
		free_points.remove( position )
		
		#Update progress bar
		if i % (n_particles / steps) == 0:
			bar.update( int( float(i) / n_particles * steps) )
		
	#Close the progress bar	
	bar.finish()
							
	
def main():
	#Parse command line arguments
	parser = getCommandLineParser()
	#parser.print_help()
	args = vars( parser.parse_args() )

	image_size = args['s']
	if args['p'] is None:
		n_particles = args['n']
	else:
		n_particles = int(image_size**2 * args['p'])
	
	frame_shape = args['f']	
	output_file = args['o'] 
		
	#Description of the simulation
	print "Starting simulation for a ", image_size, "x", image_size, " image"
	print "Number of particles: ", n_particles
	print "Frame shape: ", frame_shape
	
	#Create the bitmap containing the DLA result
	img = Image.new( 'RGB', (image_size, image_size), "black")
	pixels = img.load()
	
	#Create range of colors
	red = colour.Color("red")
	blue = colour.Color("blue")	
	rangeColor = list( red.range_to(blue, nColors) )
	
	#Paint the initial frame where particles can stick
	paintFrame(pixels, image_size, frame_shape)
	
	#Simulate the DLA
	normalSimulation(pixels, n_particles, image_size, rangeColor)
				
	#Show the result
	img = img.transpose(Image.FLIP_TOP_BOTTOM)
	img.show()
	
	#Save the image if we specified an output file	
	if output_file is not None:
		img.save(output_file)
		

if __name__ == "__main__":
  main()

