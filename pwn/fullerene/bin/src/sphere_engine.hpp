#pragma once

#include "common.hpp"

#include "perlin.hpp"

#include <vector>

#include "updater.hpp"

struct SphereChunk
{
	//private:
	svec3 corner;
	svec3 dimensions;
	
	float rho_stride;
	float phi_stride;
	float theta_stride;
	
	int rho_len;
	int phi_len;
	int theta_len;
	
	Updater* updater;
	
	siv::PerlinNoise* noise_gen;
	
	Voxel* verts = nullptr;
	
	double voxel_vol = 0.0;

	double vol = 0.0;

	public:

	SphereChunk();

	~SphereChunk();

	void clear();
	
	Voxel& ref(int rho_idx, int phi_idx, int theta_idx);
	
	void mesh(std::vector<Vertex>& vbuf, std::vector<uint32_t>& ibuf);
	
	void update_mesh();
	
	svec3 ref_pos(int rho_idx, int phi_idx, int theta_idx);
	
	svec3 get_corner() const;
	
	svec3 get_dimensions() const;
	
	svec3 get_strides() const;
	
	ivec3 get_lens() const;
	
	siv::PerlinNoise* get_noise() const;
	
	double get_volume() const;
};
void make_SphereChunk(SphereChunk* in);
void make_SphereChunk(SphereChunk* in, svec3 corn, svec3 d, siv::PerlinNoise* noise_gen_ptr_in, Updater* updater_in);

std::ostream& operator<<(std::ostream& s, const SphereChunk& a);
