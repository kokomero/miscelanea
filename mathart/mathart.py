from PIL import Image, ImageDraw
import colour
import argparse
from math import *
from progressbar import *

#TODO:
#Be able to especify the formulas from command line or from a configuration file
#Comment the function correctly
steps = 100

#Create parser for command line arguments
def getCommandLineParser():
	parser = argparse.ArgumentParser(description='Paint Math Art images composed of lines and circles.')
	parser.add_argument('-s', default='1024', help='Create an image of size x size pixels', type=int)
	parser.add_argument('-a', default="true", help='Apply antialiasing with subsampling: [true|false]', type=bool, required=False)
	parser.add_argument('-S', default='10', help='Supersampling factor to avoid antialiasing. <10', type=int)
	parser.add_argument('-n', default='10000', help='Number of lines/circles to draw', type=int)
	parser.add_argument('-o', help='File name to save the image (.png)', type=str, required=False)	
	parser.add_argument('-e', default='line', help='Base element: [line|circle]', type=str, required=False)
	parser.add_argument('-c', default="black", help='Init Color, for color degrade', type=str, required=False)	
	parser.add_argument('-C', default="black", help='End Color, for color degrade', type=str, required=False)	
	parser.add_argument('-v', default="true", help='Verbose mode', type=bool, required=False)	
	return parser

def drawLines(image, n, colorDegrade, statusBar):
	
	#Get drawer object
	drawer = ImageDraw.Draw(image) 
	size = image.size[0]
	
	#Number of colors for colros degrade
	nColors = len( colorDegrade )
	
	for k in range(0, n):			
		#Get initial and end point of the segment
		X1 = sin(108.0*pi*k/n)*sin(4.0*pi*k/n)
		Y1 = cos(106.0*pi*k/n)*sin(4.0*pi*k/n)
		X2 = sin(104.0*pi*k/n)*sin(4.0*pi*k/n)
		Y2 = cos(102.0*pi*k/n)*sin(4.0*pi*k/n)
		
		#Transform coordenates to the image coordenate system
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
			
				
def drawCircles(image, n, colorDegrade, statusBar):
	
	#Get drawer object
	drawer = ImageDraw.Draw(image) 
	size = image.size[0]
	
	#Number of colors for colros degrade
	nColors = len( colorDegrade )
	
	#If the base elements are circles
	for k in range(0, n):
		#Get center and radius of the circle
		X = sin(14.0*pi*k/n)
		Y = cos(26.0*pi*k/n)**3
		r = 1.0/4.0*cos(40.0*pi*k/n)**2
		
		#Transform coordenates of the bounding box
		box = (X-r, Y-r, X+r, Y+r)
		box_adjusted = [ (box[j] + 1.0)/2.0*size for j in range(0,4) ]
		
		#Get a color from the color degrade
		colorIndex = int( float(k) / n * nColors )
		color = tuple( [ int(j*255) for j in colorDegrade[colorIndex].rgb ] )
		
		#Draw the line
		drawer.ellipse(box_adjusted, outline=color)	
		
		#Update progress bar
		if k % (n / steps) == 0:
			statusBar.update( int( float(k) / n * steps) )
	
	
def main():
	#Parse command line arguments
	parser = getCommandLineParser()
	#parser.print_help()
	args = vars( parser.parse_args() )
	
	#Get command line parameters
	image_size = args['s']
	antialiasing = args['a']
	supersampling = args['S']
	if supersampling > 10:
		supersampling = 10
		
	n_elements = args['n']
	base_element = args['e']
	output_file = args['o'] 	
	init_color = args['c']
	end_color = args['C']
	verbose = args['v']
	
	if antialiasing:
		super_size = image_size*supersampling
	else:
		super_size = image_size
	
	#Print description if verbose
	if verbose:
		print "Art work with", base_element, "as base element."
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
	
	if base_element == "line":		
		#If the base element are lines
		drawLines(img, n_elements, rainbow, bar)
			
	elif base_element == "circle":
		#If the base element are circles
		drawCircles(img, n_elements, rainbow, bar)
		
	else:
		parser.print_help()
		raise("Base element argument should be either [line|circle]")
		sys.exit(2)
	
	print ""
	
	#To avoid antialiasing, we downsample the image with an
	#Antialias filter
	if antialiasing:
		img = img.resize((image_size, image_size), Image.ANTIALIAS)
		
	#Show the result
	img.show()
	
	#Save the image if we specified an output file	
	if output_file is not None:
		img.save(output_file)



if __name__ == "__main__":
  main()
