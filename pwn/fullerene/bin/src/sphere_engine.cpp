#include "sphere_engine.hpp"

#include <cstring>

#define GLM_ENABLE_EXPERIMENTAL

#include "glm/gtx/string_cast.hpp"

SphereChunk::SphereChunk()
{
	corner = { 0, 0, 0 };
	dimensions = { 0, 0, 0 };
	vol = 0;
	rho_len = 0;
	phi_len = 0;
	theta_len = 0;
	verts = nullptr;
}

void make_SphereChunk(SphereChunk* in)
{
	in->corner = { 0, 0, 0 };
	in->dimensions = { 0, 0, 0 };
	in->vol = 0;
	in->rho_len = 0;
	in->phi_len = 0;
	in->theta_len = 0;
	in->verts = nullptr;
}

bool isClean(float a, float b)
{
	return std::abs((a / b) - ((int) (a / b))) < 0.0001;
}

void make_SphereChunk(SphereChunk* in, svec3 corn, svec3 d, siv::PerlinNoise* noise_gen_ptr_in, Updater* updater_in)
{
	in->corner = corn;
	in->dimensions = d;
	in->noise_gen = noise_gen_ptr_in;
	in->updater = updater_in;

	auto center_slice = in->corner + in->dimensions / 2;

	//approx dimensions of a 1x1x1 voxel...
	in->rho_stride = 1;
	in->phi_stride = 1 / (center_slice.rho);
	in->theta_stride = 1 / (center_slice.rho * sin(center_slice.phi));

	if (! (isClean(d.rho, in->rho_stride) && isClean(d.phi, in->phi_stride) && isClean(d.theta, in->theta_stride))){
		//anneal to force stride to actually fit the chunk bounds 
		in->rho_stride = d.rho / (float)((int) (.5 + (d.rho)));
		in->phi_stride = d.phi / (float)((int) (.5 + (d.phi / in->phi_stride)));
		in->theta_stride = d.theta / (float)((int) (.5 + (d.theta / in->theta_stride)));
	}

	in->rho_len = d.rho / in->rho_stride;
	in->phi_len = d.phi / in->phi_stride;
	in->theta_len = d.theta / in->theta_stride;


	//voxel vol	
	in->voxel_vol = center_slice.rho * center_slice.rho * in->rho_stride * sin(center_slice.phi) * in->phi_stride * in->theta_stride;

	in->vol = in->voxel_vol * in->rho_len * in->phi_len * in->theta_len;
	
	in->verts = (Voxel*)smalloc(in->vol);
	memset(in->verts, 0, in->vol);
	
	//Add in YOUR worldgen code here :D :D :D
	
	for (int u = 0; u < in->rho_len; u++)
	{
		for (int i = 0; i < in->phi_len; i++)
		{
			for (int j = 0; j < in->theta_len; j++)
			{
				double max_rho = 10 + 5 * in->noise_gen->noise2D_01(i * in->phi_stride + corn.phi, j * in->theta_stride + in->corner.theta);
				
				double m_rho = u * in->rho_stride + in->corner.rho;
				
				char type = 0;
				if (std::abs(m_rho - max_rho) < .5){
					type = 1;
				}
				
				in->ref(u,i,j).type = type;
			}	
		}
	}
}

void SphereChunk::clear()
{
	std::memset(this, 0, sizeof(SphereChunk));
	verts = nullptr;
}

SphereChunk::~SphereChunk()
{
	if (verts != nullptr){
		std::memset(verts, 0, vol);
	}

	free(verts);
	verts = nullptr;

	clear();
	/*
	Do not go gentle into that good night, 
	Old age should burn and rave at close of day; 
	Rage, rage against the dying of the light.
	*/
}


Voxel& SphereChunk::ref(int rho_idx, int phi_idx, int theta_idx)
{
	auto idx = rho_idx * phi_len * theta_len + phi_idx * theta_len + theta_idx;
	
	if (idx < 0 || idx >= vol){
		std::cout << "Yeet. " << idx << " " << vol << "\n";
		return verts[0];
	}
	
	return verts[idx];
}


svec3 SphereChunk::ref_pos(int rho_idx, int phi_idx, int theta_idx)
{
	return corner + svec3(rho_idx * rho_stride, phi_idx * phi_stride, theta_idx * theta_stride);
}

void SphereChunk::mesh(std::vector<Vertex>& vbuf, std::vector<uint32_t>& ibuf)
{
	for (int r = 0; r < rho_len - 1; r++)
	{
		for (int p = 0; p < phi_len - 1; p++)
		{
			for (int t = 0; t < theta_len - 1; t++)
			{
				if (ref(r, p, t).type == 1){
					int s = vbuf.size();
					
					//face pointing in ->
					vbuf.push_back({spherical_to_cartesian(ref_pos(r, p, t))});
					vbuf.push_back({spherical_to_cartesian(ref_pos(r, p + 1, t))});
					vbuf.push_back({spherical_to_cartesian(ref_pos(r, p, t + 1))});
					vbuf.push_back({spherical_to_cartesian(ref_pos(r, p + 1, t + 1))});
					
					ibuf.push_back(s);
					ibuf.push_back(s + 1);
					ibuf.push_back(s + 2);
					
					ibuf.push_back(s + 1);
					ibuf.push_back(s + 2);
					ibuf.push_back(s + 3);
					
					//face pointing out <--
					vbuf.push_back({spherical_to_cartesian(ref_pos(r + 1, p, t))});
					vbuf.push_back({spherical_to_cartesian(ref_pos(r + 1, p + 1, t))});
					vbuf.push_back({spherical_to_cartesian(ref_pos(r + 1, p, t + 1))});
					vbuf.push_back({spherical_to_cartesian(ref_pos(r + 1, p + 1, t + 1))});
					
					ibuf.push_back(s + 4);
					ibuf.push_back(s + 1 + 4);
					ibuf.push_back(s + 2 + 4);
			
					ibuf.push_back(s + 1 + 4);
					ibuf.push_back(s + 2 + 4);
					ibuf.push_back(s + 3 + 4);	
				}
			}
		}
	}
}

void SphereChunk::update_mesh()
{
	std::vector<Vertex> vbuf;
	std::vector<uint32_t> ibuf;
	mesh(vbuf, ibuf);
	updater->update_mesh(vbuf, ibuf);
}

svec3 SphereChunk::get_corner() const
{
	return corner;
}
	
svec3 SphereChunk::get_dimensions() const
{
	return dimensions;
}
	
svec3 SphereChunk::get_strides() const
{
	return {rho_stride, phi_stride, theta_stride};
}

ivec3 SphereChunk::get_lens() const
{
	return ivec3(rho_len, phi_len, theta_len);	
}

double SphereChunk::get_volume() const
{
	return vol;
}

siv::PerlinNoise* SphereChunk::get_noise() const
{
	return noise_gen;
}

std::ostream& operator<<(std::ostream& s, const SphereChunk& temp)
{
	s << "Volume: " << temp.get_volume() << " Corner: " << temp.get_corner() << " Dimensions: " << temp.get_dimensions() << " Strides: " << temp.get_strides();
	s << " Lens: " << glm::to_string(temp.get_lens());
	return s;
}
