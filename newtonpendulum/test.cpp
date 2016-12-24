#include <iostream>
#include <cmath>
using namespace std;

#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
using namespace cv;

#include "Vector.hpp"
#include "Body.hpp"

int main( int argc, const char* argv[] )
{
	cout << "Test functions for Vector class: " << endl;
	Vector2D v1(2.0, 3.4);
	Vector2D v2(5.2, 6.7);

	cout << "Vector1: " << v1 << endl;
	cout << "Vector2: " << v2 << endl;

	cout << "Vector1 + Vector2: " << v1 + v2 << endl;
	cout << "Vector1 - Vector2: " << v1 - v2 << endl;
	cout << "Vector1*2.5: " << v1*2.5 << endl;
	cout << "Vector2/2.5: " << v1/2.5 << endl;
	cout << "Vector1 norm: " << v1.norm() << endl;
	cout << "Vector1 polar angle: " << v1.polarAngle() << endl;

	cout << "Test functions for Body class: " << endl;

	Body b(1.0);
	const double g = 9.11;
	const double mass = 1.0;
	Vector2D v0(1.0, 10.0);
	b.setVelocity( v0 );
	b.setForce( Vector2D(0.0, -mass*g) );

	const double deltaTime = 0.03;
	for(int i = 0; i < 10; i++) {

		b.updateStatus(deltaTime);
		cout << "Body: " << b << endl;
	}

	//Pendulum test
	cout << "Test functions for Pendulum class: " << endl;
	const double bobMass = 1.0;
	const double stringLength = 175.0;
	const unsigned int x_dim = 400;
	const unsigned int y_dim = 400;

	//Initial Conditions
	double alpha = 30.0 * 2 * M_PI / 360.0; //angle between the string and the vertical
	Vector2D p0(x_dim / 2.0 + stringLength*sin(alpha), stringLength*cos(alpha));
	Vector2D gravityForce = Vector2D(0.0, -bobMass*g);
	double tangencialVel = 0.0;
	double tangencialForce;
	double tangencialAcc;
	Body bob(bobMass, p0);

	// Create black empty images
	Mat image = Mat::zeros( 400, 400, CV_8UC3 );

	//Simulation Loop
	for(unsigned int i = 0; i < 1000; i ++) {
		//Tangencial force and acceleration
		tangencialForce = gravityForce.norm() * sin( alpha );
		tangencialAcc = tangencialForce / bobMass;
		tangencialVel += tangencialAcc * deltaTime;
		alpha -= tangencialVel * deltaTime;
		bob.setPosition( Vector2D( x_dim / 2.0 + stringLength*sin( alpha ), stringLength*cos( alpha )) );
		Vector2D p = bob.getPosition();

		// Draw the string and bob
		line( image, Point( x_dim / 2.0, 0.0), Point( p.getX(), p.getY() ), Scalar( 110, 220, 0 ),  2, 8 );
		circle( image, Point( p.getX(), p.getY() ), 16.0, Scalar( 0, 0, 255 ), 1, 8 );
		imshow("Image",image);
		image = Scalar(0,0,0);
		waitKey( 2500 );
	}

	//g++ Body.cpp test.cpp Vector.cpp `pkg-config --libs --cflags opencv`


}
