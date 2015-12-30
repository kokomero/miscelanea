from PIL import Image, ImageDraw
import math
import argparse
import random
import numpy as np

#Create parser for command line arguments
def getCommandLineParser():
 parser = argparse.ArgumentParser(description='Paint simulations of the Buffon Needle problem.')
 parser.add_argument('-t', default='200', help='Distance between lines', type=int)
 parser.add_argument('-l', default='100', help='Length of the needle', type=int)
 parser.add_argument('-n', default='300', help='Number of needles thrown in each simulation', type=int)
 parser.add_argument('-m', default='1', help='Number of simulations', type=int)
 parser.add_argument('-o', help='File name to save the simulation into a GIF animation (.gif)', type=str, required=False)	
 return parser

def paintBars(image, t, l):
 """Draw the vertical bars on the image"""
 
 #Define color for the bars
 white = (255, 255, 255)

 #Draw object to draw lines
 draw = ImageDraw.Draw(image)

 #Effectively draw the vertical lines
 size = image.size[0]
 draw.line([(l,0), (l, size)], white)
 draw.line([(l + t,0), (l + t, size)], white)
 draw.line([(l + 2 * t,0), (l + 2 * t, size)], white)
 
def throwNeedle(image, n, t, l):
 """Throw n needle in the simulation board"""
 """Paint in red needles touching one of the bars"""
 
 #Define color for the bars
 green = (0, 255, 0)
 red = (255, 0, 0)
 
 #x coordenate of bar positions
 bar_pos = [l, l + t, l + 2 * t]
 size = image.size[0]
 
 #Count the number of touchs
 touch_count = 0
 
 #Draw object to draw lines
 draw = ImageDraw.Draw(image)
  
 #Create the n simulations
 for i in range(0, n):  
  #Generate the alpha angle and the position of the center of the needle 
  y = random.randint(0, size)
  x = random.randint(0, size)
  alpha = random.uniform(0, math.pi / 2.0 )
 
  #Points of the needle
  pointB = (x + l / 2 * math.sin( alpha ), y + l / 2 * math.cos( alpha ) )
  pointA = (x - l / 2 * math.sin( alpha ), y - l / 2 * math.cos( alpha ) )
 
  #Check if the needle touch a line
  (xA, xB) = (pointA[0], pointB[0])
  touch = ( xA < bar_pos[0] and xB > bar_pos[0] ) or \
      ( xA < bar_pos[1] and xB > bar_pos[1] ) or \
      ( xA < bar_pos[2] and xB > bar_pos[2] )

  #Draw the needle
  if touch:
   draw.line( (pointA, pointB), red)
   touch_count += 1
  else:
   draw.line( (pointA, pointB), green)
  
 pi_estimate = float( 2.0 * l * n) / float(t * touch_count)
 
 return pi_estimate
 
def main():
 #Parse command line arguments
 parser = getCommandLineParser()
 #parser.print_help()
 args = vars( parser.parse_args() )

 #Parse geometric parameters
 t = args['t']
 l = args['l']
 n = args['n']
 m = args['m']

 if args['o'] is None:
  None
 else: 
  None

 #Description of the simulation
 print "Starting simulation for ", n, " needles."
 print "Distance between lines: ", t, " Needle Length: ", l

 #Create the bitmap containing the DLA result
 image_size = t * 2 + 2 * l #Draw three vertical lines, plus allow margin for the borders
 img = Image.new( 'RGB', (image_size, image_size), "black")

 #Array with estimates of pi for each simulation
 estimates = np.zeros(m)
 
 #Draw the vertical lines
 paintBars(img, t, l)

 #Simulate m times
 for i in range(0, m):
  #Throw needle n times
  estimates[i] = throwNeedle(img, n, t, l)
     
 print "Mean: ", np.mean( estimates )
 print "Std: ", np.std( estimates )
 
 #Show the result
 img = img.transpose(Image.FLIP_TOP_BOTTOM)
 img.show()
  
if __name__ == "__main__":
 main()
