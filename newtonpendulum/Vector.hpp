
#ifndef VECTOR_HPP
#define VECTOR_HPP

#include <iostream> 

class Vector2D {
	
public:
	~Vector2D();
	Vector2D();
	Vector2D(double x, double y);
	
	inline double getX(){ return x; };
	inline double getY(){ return y; };
	
	inline void set(double x, double y){
		x = x;
		y = y;		
	};
	
	double norm();
	double polarAngle();
	
	Vector2D operator+(const Vector2D& b);
	Vector2D operator-(const Vector2D& b);
	Vector2D operator*(const double b);
	Vector2D operator/(const double b);
	Vector2D& operator+=(const Vector2D& right);
	Vector2D& operator-=(const Vector2D& right);
	Vector2D& operator*=(double b);
	Vector2D& operator/=(double b);

	friend std::ostream& operator<<(std::ostream &strm, const Vector2D &v); 
	
private:
	double x;
	double y;
};


#endif
