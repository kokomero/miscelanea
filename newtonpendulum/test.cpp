#include <iostream>
using namespace std;

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
	
	const double deltaTime = 0.1;	
	for(int i = 0; i < 100; i++){
		
		b.updateStatus(deltaTime);
		cout << "Body: " << b << endl;

	}
	

}
