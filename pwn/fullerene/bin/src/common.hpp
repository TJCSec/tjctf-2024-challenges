#pragma once

#include "glm/glm.hpp"
#define _USE_MATH_DEFINES
#include <cmath>
#include <iostream>


//resolution of a voxel
constexpr double voxel_res = 1.;

//LMFAO go jump in a lake
using namespace glm;

//I don't want accidental arthimetic w/ the glm library types
struct svec3
{
	double rho;
	double phi;
	double theta;

	svec3()
	{}

	svec3(double r, double p, double t);

};

struct Vertex
{
	vec3 pos;
};

svec3 operator+(const svec3& a, const svec3& b);
svec3 operator*(const svec3& a, double b);
svec3 operator/(const svec3& a, double b);

std::ostream& operator<<(std::ostream& s, const svec3& a);

vec3 spherical_to_cartesian(const svec3& spher);

bool close(const vec3& a, const vec3& b);

svec3 cartesian_to_spherical(const vec3& cart);

void test_coords();

//point + differential
double approx_volume_section(const svec3& pt, const svec3& d);

struct Voxel
{
	uint8_t type = 0;
};
 
void* smalloc(int l);