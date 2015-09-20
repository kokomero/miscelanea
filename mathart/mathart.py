import Image
import ImageDraw
import colour
import argparse
from math import *

#TODO:
#Measure execution time
#Be able to especify the formulas from command line or from a configuration file


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
	return parser
		
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
	
	if antialiasing:
		super_size = image_size*supersampling
	else:
		super_size = image_size
	
	#Create the bitmap which will contain the resulting image
	img = Image.new( 'RGB', (super_size, super_size), "white")
	
	#Get drawer object
	drawer = ImageDraw.Draw(img) 
	
	#Create range of colors
	nColors = 256
	init_color = colour.Color(init_color)
	end_color = colour.Color(end_color)	
	rainbow = list( init_color.range_to(end_color, nColors) )
	
	if base_element == "line":
		#If the base element are lines
		for k in range(0, n_elements):
			
			#Get initial and end point of the segment
			X1 = sin(108.0*pi*k/n_elements)*sin(4.0*pi*k/n_elements)
			Y1 = cos(106.0*pi*k/n_elements)*sin(4.0*pi*k/n_elements)
			X2 = sin(104.0*pi*k/n_elements)*sin(4.0*pi*k/n_elements)
			Y2 = cos(102.0*pi*k/n_elements)*sin(4.0*pi*k/n_elements)
			
			#Transform coordenates to the image coordenate system
			coord = (X1, Y1, X2, Y2)
			coord_adjusted = [ (coord[j] + 1.0)/2.0*super_size for j in range(0,4) ]
			
			#Get a color from the color degrade
			colorIndex = int( float(k) / n_elements * nColors )
			color = color = tuple( [ int(j*255) for j in rainbow[colorIndex].rgb ] )
			
			#Draw the line
			drawer.line(coord_adjusted, fill=color, width=1)	
			
	elif base_element == "circle":
		#If the base elements are circles
		for k in range(0, n_elements):
			#Get center and radius of the circle
			X = sin(14.0*pi*k/n_elements)
			Y = cos(26.0*pi*k/n_elements)**3
			r = 1.0/4.0*cos(40.0*pi*k/n_elements)**2
			
			#Transform coordenates of the bounding box
			box = (X-r, Y-r, X+r, Y+r)
			box_adjusted = [ (box[j] + 1.0)/2.0*super_size for j in range(0,4) ]
			
			#Get a color from the color degrade
			colorIndex = int( float(k) / n_elements * nColors )
			color = tuple( [ int(j*255) for j in rainbow[colorIndex].rgb ] )
			
			#Draw the line
			drawer.ellipse(box_adjusted, outline=color)	
	else:
		parser.print_help()
		raise("Base element argument should be either [line|circle]")
		sys.exit(2)
			
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
