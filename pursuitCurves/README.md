# Pursuit Curve Problem

This snippet of code visualizes the [Pursuit Curves](https://en.wikipedia.org/wiki/Pursuit_curve) between different moving objects, either with an image or an animation.
Simulation method has been used instead of mathematical formulation, using the pyglet library for rendering the images.

You can check my blog entry on the problem:
[Rotpunkt Blog, Pursuit Curves](https://rotpunkt-programming.blogspot.com/2018/12/pursuit-curves.html)

## Getting Started

Clone this repository on your local disk by executing the line below. 
Be aware you will download other small projects as well

git clone https://github.com/kokomero/miscelanea/

### Prerequisites

Install numpy and pyglet packages, these are available in the Python pip repository

### Execution

Run the script passing as argument an input file with the description of the problem. Several files are provided for now
for different problems. See .cfg files for scenario examples. In the configuration file you can easily setup the initial position of each of the moving object as well as their speed.
Likewise, you choose whether you want an animated version of the problem of the resulting final image, as well as setting up parameters such as screen refreshing time.

python object_pursuit_curve.py -i four_body_problem.cfg

The result of the execution should be a windows like the following one, in case we execute the fixed image:
![Four Body Pursuing Problem](four_body_problem.png)

The simulation can be ended by pressing ESC key or closing the window.

### Deployment

Just copy the files in a local directory, make sure the required libraries are installed and execute the script following above instructions.

## TODOs
* Implement antialiasing
* Move line width and colors to the configuration file. Each moving object could have lines linking pursuers and leaders in different colors
* Define scenarios in 3D space, and be able to rotate the image in 3D
* Be able to define parametric velocity vector for a leader so that we can implement circular movements

## References
* Wikipedia: [Pursuit Curves, in English](https://en.wikipedia.org/wiki/Pursuit_curve)
* Wikipedia: [Pursuit Curves, in French](https://fr.wikipedia.org/wiki/Courbe_du_chien)
* Universidad Complutense de Madrid: [Page on Pursuit Curves, in Spanish](http://www.mat.ucm.es/cosasmdg/cdsmdg/modelizaciones/proyectos/proyecto2/index.htm)
* Wolfram Research: [entry for Pursuit Curves, in English](http://mathworld.wolfram.com/PursuitCurve.html)
* Wikipedia: [Envelope curves, in English](https://en.wikipedia.org/wiki/Envelope_(mathematics))
## Contributing

Feel free to contribute to this piece of code

## Authors
* **Victor Montiel** - *Initial work* - [Personal website](http://www.victormontielargaiz.net)

## License
No licence for this project

## Acknowledgments
* pyglet library


