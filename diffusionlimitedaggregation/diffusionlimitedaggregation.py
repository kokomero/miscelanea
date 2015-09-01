import Image
import colour
import random
import argparse

#See ideas in http://bit-player.org/
#TODO:
#Define adjacency matrix for the next move and for neighbourhood check
#Define the contour where initially the particles can stick
#A possible more efficient algorithm will iterate across all current
#particles instead of simulating a random-walk over all the image


#the adjacency matrix for movements and neighbourhood check
adjacency = [(i,j) for i in (-1,0,1) for j in (-1,0,1) if not (i == j == 0)] 

#Create parser for command line arguments
def getCommandLineParser():
	parser = argparse.ArgumentParser(description='Paint a brownian tree using Diffusion Limited Aggregtion simulation.')
	parser.add_argument('-s', default='200', help='Create an image of size x size pixels', type=int)
	parser.add_argument('-n', default='2000', help='Number of particles to simulate', type=int)
	parser.add_argument('-f', help='Fraction of particles of the total number of pixel on the image', type=float, required=False)
	parser.add_argument('-o', help='File name to save the image (.png)', type=str, required=False)	
	return parser
  
#Get a random initial position for each new particle
def getRandomPosition(size):
	x = int( random.random() * size )
	y = int( random.random() * size )
	return (x, y)
	
#Move randomly a particle in a position
def moveParticle(position, size):
	(x, y) = position
	(dx, dy) = adjacency[ random.randrange(0, 8) ]
	if( 0 <= x + dx < size ):
		x = x + dx
	if( 0 <= y + dy < size ): 
		y = y + dy
	return (x, y)	

#Check if there is an adjacent particle where we can stick
def adjacentParticle(pixels, size, position):	
	x = position[0]
	y = position[1]
	
	#Particles can stick on the bottom line
	if (y == 0):
		return True
	
	#Look for adjacent pixels to see if they are non-black
	for dx, dy in adjacency:
		if (0 <= x + dx < size) and (0 <= y + dy < size):
			if pixels[x + dx, y + dy] != (0,0,0):
				return  True
	
	return False	
	
def main():
	#Parse command line arguments
	parser = getCommandLineParser()
	#parser.print_help()
	args = vars( parser.parse_args() )

	image_size = args['s']
	if args['f'] is None:
		n_particles = args['n']
	else:
		n_particles = int(image_size**2 * args['f'])
		
	output_file = args['o'] 
	
	#Description of the simulation
	print "Starting simulation for a ", image_size, "x", image_size, " image"
	print "Number of particles: ", n_particles
	
	#Create the bitmap containing the DLA result
	img = Image.new( 'RGB', (image_size, image_size), "black")
	pixels = img.load()
	
	#Create range of colors
	red = colour.Color("red")
	blue = colour.Color("blue")
	nColors = 100
	rangeColor = list( red.range_to(blue, nColors) )
	
	#Iterate over all n particles
	for i in range(1, n_particles):
		
		#Get initial position
		position = getRandomPosition(image_size)
		
		#Color index depending on the time particle was created
		colorIndex = int( float(i) / n_particles * nColors )
		color = tuple( [ int(j*255) for j in rangeColor[colorIndex].rgb ] )
		
		#Apply brownian motion until we hit another particle
		while not adjacentParticle(pixels, image_size, position): 
			position = moveParticle(position, image_size)
		else:
			pixels[ position[0], position[1] ] = color
			
		#Print indications
		if i % 100 == 0:
			print "Particle: ", i
			
	#Show the result
	img = img.transpose(Image.FLIP_TOP_BOTTOM)
	img.show()
	
	#Save the image if we specified an output file	
	if output_file is not None:
		img.save(output_file)
		

if __name__ == "__main__":
  main()

