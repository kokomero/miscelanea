#include "Body.hpp"

Body::~Body(){
	
}

Body::Body() : mass(0.0){
	
}

Body::Body(double _mass) : mass(_mass){
	
}

Body::Body(double _mass, const Vector2D& _pos) : mass(_mass), position(_pos){
	
}

void Body::applyForce(const Vector2D& f){
	force += f;
}
void Body::clearForces(){
	force.set(0.0, 0.0);
}

void Body::updateStatus(double dt){
	
	acceleration = force / mass;
	velocity += acceleration * dt;
	position += velocity * dt;
	
}

std::ostream& operator<<(std::ostream &strm, const Body &b){
	return strm << "[ Position: " << b.position << ", Velocity: "  << b.velocity  << ", Accelarion: " << b.acceleration << ", Force: " << b.force  << "]";
}
