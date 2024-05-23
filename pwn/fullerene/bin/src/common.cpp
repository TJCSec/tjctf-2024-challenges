#include "common.hpp"

uint8_t* canary;
void* smalloc(int l)
{
	
	if (l > 0x1000)
	{
		return nullptr;
	}	
	

	void* ptr = malloc(l);
	
	size_t ptr_i = (size_t) ptr;

	//he protec
	size_t stackprotec = (size_t)(canary - 0x1000);

	if (ptr_i > stackprotec)
	{
		//but he also attac
		std::cout << "You suck!\n";
		return nullptr;
	}
	return ptr;
}

svec3::svec3(double r, double p, double t)
	: rho(r), phi(p), theta(t)
{

}

std::ostream& operator<<(std::ostream& s, const svec3& a)
{
	s << "Svec(" << std::to_string(a.rho) << ", " + std::to_string(a.phi) << ", " << std::to_string(a.theta) << ")";
	return s;
}

svec3 operator+(const svec3& a, const svec3& b)
{
	return svec3(a.rho + b.rho, a.phi + b.phi, a.theta + b.theta);
}

svec3 operator*(const svec3& a, double b)
{
	return svec3(a.rho * b, a.phi * b, a.theta * b);
}

svec3 operator/(const svec3& a, double b)
{
	return svec3(a.rho / b, a.phi / b, a.theta / b);
}


vec3 spherical_to_cartesian(const svec3& spher)
{
	vec3 out;

	//https://en.wikipedia.org/wiki/Spherical_coordinate_system#:~:text=In%20mathematics%2C%20a%20spherical%20coordinate,a%20fixed%20polar%20axis%2C%20or
	//I'm using the mathematical convention
	//first number is the radius
	//second number is the angle between the z axis and the vector
	//third number is the angle between the x axis and the *shadow* of the vector on the xy plane

	out.x = spher.rho * sin(spher.phi) * cos(spher.theta);
	out.y = spher.rho * sin(spher.phi) * sin(spher.theta);
	out.z = spher.rho * cos(spher.phi);

	return out;
}

bool close(const vec3& a, const vec3& b)
{
	return glm::length(a - b) < .00001;
}

svec3 cartesian_to_spherical(const vec3& cart)
{
	svec3 out;
	out.rho = glm::length(cart);

	if (out.rho == 0)
	{
		return { 0,0,0 };
	}

	out.phi = acos(cart.z / out.rho);
	out.theta = atan2(cart.y, cart.x);
	return out;
}

void test_coords()
{
	vec3 arr[10] = { vec3(1,1,1), vec3(0,0,0), vec3(1,2,3), vec3(100,23,03) };

	for (auto& a : arr)
	{
		svec3 sphr = cartesian_to_spherical(a);
		vec3 recons = spherical_to_cartesian(sphr);
		if (!close(a, recons))
		{
			std::cout << "Issue!!\n";
		}
	}
}

//point + differential
double approx_volume_section(const svec3& pt, const svec3& d)
{
	//return the volume of a spherical section
	//rho**2 drho, sin(phi) dphi, dtheta
	return pt.rho * pt.rho * d.rho * sin(pt.phi) * d.phi * d.theta;
}

