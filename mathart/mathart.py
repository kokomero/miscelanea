from PIL import Image, ImageDraw
import colour
import argparse
from math import *
from progressbar import *

"""A note on the parametrizations:
On the script.sh file, we can find some examples for executing this program.

The parametrization use k as the index for each iteration and n as the 
number of lines or circles we will be draw on the image.

The parametrization is read directly by the eval() python function, so, it 
should be a correct python expression.

"""

#Number of steps of the bar status
steps = 100

def getCommandLineParser():
	"""Parse command line argument parameters.
	Return a dictionary with the parameters parsed.
    """
	parser = argparse.ArgumentParser(description='Paint Math Art images composed of lines and circles.')
	parser.add_argument('-s', default='1024', help='Create an image of size x size pixels', type=int)
	parser.add_argument('-a', default=True, help='Apply antialiasing with subsampling: [True|False]', type=bool, required=False)
	parser.add_argument('-S', default='10', help='Supersampling factor to avoid antialiasing. <10', type=int)
	parser.add_argument('-n', default='10000', help='Number of lines/circles to draw', type=int)
	parser.add_argument('-o', help='File name to save the image (.png)', type=str, required=False)	
	parser.add_argument('-e', default='line', help='Base element: [line|circle]', type=str, required=False)
	parser.add_argument('-c', default="black", help='Init Color, for color degrade', type=str, required=False)	
	parser.add_argument('-C', default="black", help='End Color, for color degrade', type=str, required=False)	
	parser.add_argument('-v', default="True", help='Verbose mode', type=bool, required=False)	
	parser.add_argument('-X1', default="sin(108.0*pi*k/n)*sin(4.0*pi*k/n)", help='X1 formula for line elements', type=str, required=False)	
	parser.add_argument('-Y1', default="cos(106.0*pi*k/n)*sin(4.0*pi*k/n)", help='Y1 formula for line elements', type=str, required=False)	
	parser.add_argument('-X2', default="sin(104.0*pi*k/n)*sin(4.0*pi*k/n)", help='X2 formula for line elements', type=str, required=False)	
	parser.add_argument('-Y2', default="cos(102.0*pi*k/n)*sin(4.0*pi*k/n)", help='Y2 formula for line elements', type=str, required=False)	
	parser.add_argument('-Xc', default="sin(14.0*pi*k/n)", help='X coordenate formula for circle center', type=str, required=False)	
	parser.add_argument('-Yc', default="cos(26.0*pi*k/n)**3", help='Y coordenate formula for circle center', type=str, required=False)	
	parser.add_argument('-R', default="1.0/4.0*cos(40.0*pi*k/n)**2", help='Radius formula for circle', type=str, required=False)	
	return parser

def drawLines(image, parametrization, n, colorDegrade, statusBar):
	"""Draw the set of lines in the image according to a parametrization

    Keyword arguments:
    image -- The Image object where the lines will be drawn.
    parametrization -- The parametrization of each segment ((X1, Y1), (X2, Y2))
    n -- Number of lines to be drawn
    colorDegrade -- List with colors we will use to pain the lines
    statusBar -- Status bar to show progress of this function
    """
    
	#Get drawer object and image size
	drawer = ImageDraw.Draw(image) 
	size = image.size[0]
	
	#Number of colors for the color degrade
	nColors = len( colorDegrade )
	
	#Repeat for the n lines
	for k in range(0, n):			
		#Get initial and end point of the segment, according to parametrization
		X1 = eval(parametrization[0])
		Y1 = eval(parametrization[1])
		X2 = eval(parametrization[2])
		Y2 = eval(parametrization[3])
		
		#Transform coordenates [-1, 1] to the image coordenate system [0, size]
		coord = (X1, Y1, X2, Y2)
		coord_adjusted = [ (coord[j] + 1.0)/2.0*size for j in range(0,4) ]
		
		#Get a color from the color degrade
		colorIndex = int( float(k) / n * nColors )
		color = color = tuple( [ int(j*255) for j in colorDegrade[colorIndex].rgb ] )
		
		#Draw the line
		drawer.line(coord_adjusted, fill=color, width=1)	
		
		#Update progress bar
		if k % (n / steps) == 0:
			statusBar.update( int( float(k) / n * steps) )
			
				
def drawCircles(image, parametrization, n, colorDegrade, statusBar):
	"""Draw the set of circles in the image according to a parametrization

    Keyword arguments:
    image -- The Image object where the lines will be drawn.
    parametrization -- The parametrization of each circle ((Xc, Yc), Radius)
    n -- Number of circles to be drawn
    colorDegrade -- List with colors we will use to pain the lines
    statusBar -- Status bar to show progress of this function
    """
    
	#Get drawer object and the size of the image
	drawer = ImageDraw.Draw(image) 
	size = image.size[0]
	
	#Number of colors for colros degrade
	nColors = len( colorDegrade )
	
	#For each circle
	for k in range(0, n):
		#Get center and radius of the circle from parametrization
		X = eval(parametrization[0])
		Y = eval(parametrization[1])
		r = eval(parametrization[2])
		
		
		#Get coordenates of bounding box in [-1, 1] space
		box = (X-r, Y-r, X+r, Y+r)
		
		#Transform coordenates of the bounding box. Observe that 
		#to avoid cropping circles we have had to add 
		#an extra space on the image size.
		box_adjusted = [ (box[j] + 1.0 + 1.0/4.0)/(2.0 + 2.0 / 4.0)*size for j in range(0,4) ]
		
		#Get a color from the color degrade
		colorIndex = int( float(k) / n * nColors )
		color = tuple( [ int(j*255) for j in colorDegrade[colorIndex].rgb ] )
		
		#Draw the circle
		drawer.ellipse(box_adjusted, outline=color)	
		
		#Update progress bar
		if k % (n / steps) == 0:
			statusBar.update( int( float(k) / n * steps) )
	
	
def main():
	"""Main method of the program. Parse the command line argumen
	and draw the lines or circles on the image. Show the image and
	eventually save the result in an output file.
    """
    
	#Parse command line arguments
	parser = getCommandLineParser()
	#parser.print_help()
	#Get arguments as a hash table
	args = vars( parser.parse_args() )
		
	#Get command line parameters
	image_size = args['s']
	antialiasing = args['a']
	supersampling = args['S']
	
	#To avoid running out of memory, do not allow
	#big supersampling factors
	if supersampling > 10: 
		print "Supersampling factors is advised not to be greater than 10."
		supersampling = 10
		
	n_elements = args['n']
	base_element = args['e']
	output_file = args['o'] 	
	init_color = args['c']
	end_color = args['C']
	verbose = args['v']
	
	#To avoid cropping circles we have to add an extra space on the
	#image size.
	if base_element == "circle":
		image_size = image_size*(2)
		
	#If we use antialasing for better resolution, we create the plot
	#on a bigger image and then downsize the result
	if antialiasing:
		super_size = image_size*supersampling
	else:
		super_size = image_size
	
	#Print description if verbose is asked
	if verbose:
		print "Math art work with", base_element, "as base element."
		print "Number of elements:", n_elements
		print "Image size:", image_size, "x", image_size, "pixels."
		
		if antialiasing:
			print "Using antialiasing with downsizing factor of", supersampling
		
		print "Color degrade from", init_color, "to", end_color
		
		if output_file is not None:
			print "Saving result on file", output_file
	
	#Set up a progress bar to show calculations
	bar = ProgressBar(maxval=steps, widgets=[Bar('=', '[', ']'), ' ', Percentage()])
	bar.start()
	
	#Create the bitmap which will contain the resulting image
	img = Image.new( 'RGB', (super_size, super_size), "white")
		
	#Create range of colors
	nColors = 256
	init_color = colour.Color(init_color)
	end_color = colour.Color(end_color)	
	rainbow = list( init_color.range_to(end_color, nColors) )
	
	#For each kind of elements
	if base_element == "line":		
		#Get parametrization from command line
		parametrization = (args["X1"], args["Y1"], args["X2"], args["Y2"])
		
		if verbose:
			print "Parametrization:", parametrization
			
		#If the base element are lines
		drawLines(img, parametrization, n_elements, rainbow, bar)
			
	elif base_element == "circle":
		#Get parametrization from command line
		parametrization = (args["Xc"], args["Yc"], args["R"])
		
		if verbose:
			print "Parametrization:", parametrization
			
		#If the base element are circles
		drawCircles(img, parametrization, n_elements, rainbow, bar)
		
	else:
		parser.print_help()
		raise("Base element argument should be either [line|circle]")
		sys.exit(2)
	
	print ""
	
	#To avoid antialiasing, we downsample the image with an
	#Antialias filter
	if antialiasing:
		#In case of circle, we have to reduce to half the original size
		#since we created larger image to avoid circle cropping
		if base_element == "circle":
			image_size = image_size / 2	
			
		img = img.resize((image_size, image_size), Image.ANTIALIAS)			
		
	#Show the result
	img.show()
	
	#Save the image if we specified an output file	
	if output_file is not None:
		img.save(output_file)


if __name__ == "__main__":
  main()
