
#include <cmath>
#include "Vector.hpp"

Vector2D::~Vector2D(){
	
}

Vector2D::Vector2D() : x(0.0), y(0.0){
	
}

Vector2D::Vector2D(double _x, double _y) : x(_x), y(_y){
	
}

double Vector2D::norm(){
	return sqrt( x*x + y*y );
}

double Vector2D::polarAngle(){
	return atan( x / y);
}

Vector2D Vector2D::operator+(const Vector2D& b){
	return Vector2D( x + b.x, y + b.y );
}

Vector2D Vector2D::operator-(const Vector2D& b){
	return Vector2D( x - b.x, y - b.y );
}

Vector2D Vector2D::operator*(const double b){
	return Vector2D( x*b, y*b );
}

Vector2D Vector2D::operator/(const double b){
	return Vector2D( x / b, y / b );
}

Vector2D& Vector2D::operator+=(const Vector2D& b){
   x += b.x;
   y += b.y;
   return *this;
}

Vector2D& Vector2D::operator-=(const Vector2D& b){
   x -= b.x;
   y -= b.y;
   return *this;
}

Vector2D& Vector2D::operator*=(double b){
   x *= b;
   y *= b;
   return *this;
}

Vector2D& Vector2D::operator/=(double b){
   x /= b;
   y /= b;
   return *this;
}
	
std::ostream& operator<<(std::ostream &strm, const Vector2D &v){
  return strm << "(" << v.x << ", " << v.y << ")";
}

