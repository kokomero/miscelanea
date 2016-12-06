
#ifndef BODY_HPP
#define BODY_HPP

#include <iostream> 
#include "Vector.hpp"

class Body {
	
public:
	~Body();
	Body();
	Body(double mass);
	Body(double mass, const Vector2D& pos);
	
	inline void setMass(double m){ mass = m; };
	inline double getMass(){ return mass; };
	
	inline void setPosition(const Vector2D& pos) { position = pos; };
	inline Vector2D getPosition(){ return position; };
	
	inline void setVelocity(const Vector2D& vel) { velocity = vel; };
	inline Vector2D getVelocity(){ return velocity; };

	inline void setAcceleration(const Vector2D& acc) { acceleration = acc; };
	inline Vector2D getAcceleration(){ return acceleration; };	
	
	inline void setForce(const Vector2D& f) { force = f; };
	inline Vector2D getForce(){ return force; };
	
	void applyForce(const Vector2D& force);
	void clearForces();
	
	void updateStatus(double time);
	
	friend std::ostream& operator<<(std::ostream &strm, const Body &b); 
	
private:
	Vector2D position;
	Vector2D velocity;
	Vector2D acceleration;
	Vector2D force;
	double mass;

};

#endif
