#include <fstream>

#include "sphere_engine.hpp"

#define GLM_ENABLE_EXPERIMENTAL

#include "glm/gtx/string_cast.hpp"

void print_mesh(SphereChunk& slice)
{
	std::vector<Vertex> vbuf;
	std::vector<uint32_t> ibuf;
	
	slice.mesh(vbuf, ibuf);
	
	std::cout << "Begin VBUF\n";
	
	for (auto& vert : vbuf)
	{
		std::cout << glm::to_string(vert.pos) << "\n";
	}
	
	std::cout << "Begin IBUF\n";
	
	for (auto& idx : ibuf)
	{
		std::cout << idx << "\n";
	}
}

extern uint8_t* canary;


//So that you don't have to do the same thing 5x

// arr makes the Least Significant Byte of the address of file_name 0
// It may help you...
static char arr[0x70 + (0x100 - 0x40)] = "[garbo]";
static char file_name[64] = "oom.txt";
void win()
{
	std::cout << file_name << std::flush << " ";
	std::ifstream reader = std::ifstream(std::string(file_name));
	
	if (reader.is_open())
	{
		std::string data;
		getline(reader, data);
		std::cout << "Data: " << data << "\n";
	}
	
	reader.close();

	exit(-1);
}

size_t winptr;

int main()
{
	int loc;
	canary = (uint8_t*) &loc;
	
	setbuf(stdin, NULL);
	setbuf(stdout, NULL);
	std::cout << "Hello world!\n";
	std::cout << "SphereChunk size: " << sizeof(SphereChunk) << "\n";
	std::cout << "Verts offset; " << offsetof(SphereChunk, verts) << " noisegen offset: " <<  offsetof(SphereChunk, noise_gen)<< "\n";
	std::cout << M_PI << "\n";

	winptr = (size_t)win;

	// print memory addresses of winptr and file_name
	std::cout << (size_t) &winptr << "\n" << (size_t) file_name << "\n";

	test_coords();

	siv::PerlinNoise gen;
	
	gen.reseed(100);
	
	Updater* updater = new DummyUpdater(); 
	
	std::string cmd;
	
	int chunk_idx;
	int rho_idx;
	int phi_idx;
	int theta_idx;
	
	int chunk_pos = 0;
	SphereChunk chunk_list[64];
	
	SphereChunk* n = nullptr;
	
	for (int i = 0; i < 640; i++)
	{
		std::cin >> cmd;
		
		if (cmd == "read")
		{
			std::cin >> chunk_idx;
			std::cin >> rho_idx;
			std::cin >> phi_idx;
			std::cin >> theta_idx;

			assert((chunk_idx >= 0 && chunk_idx < 64));
			
			std::cout << "Voxel type is: " << (unsigned int) chunk_list[chunk_idx].ref(rho_idx, phi_idx, theta_idx).type << "\n";
		}
		else if (cmd == "write")
		{
			int typ;
			
			std::cin >> chunk_idx;
			std::cin >> rho_idx;
			std::cin >> phi_idx;
			std::cin >> theta_idx;
			std::cin >> typ;
			
			
			assert((chunk_idx >= 0 && chunk_idx < 64));
			
			//write
			chunk_list[chunk_idx].ref(rho_idx, phi_idx, theta_idx).type = (uint8_t) typ;
		}
		else if (cmd == "mkchunk")
		{
			float rho;
			float phi;
			float theta;
			
			float drho;
			float dphi;
			float dtheta;
			
			std::cin >> rho;
			
			assert((chunk_pos >= 0 && chunk_pos < 63));
			
			if (rho == -1)
			{
				make_SphereChunk(&chunk_list[chunk_pos++]);
			}
			else{
				assert((rho > 0));
				
				std::cin >> phi;
				
				assert((phi > 0));
				
				std::cin >> theta;
				std::cin >> drho;
				std::cin >> dphi;
				std::cin >> dtheta;
				
				make_SphereChunk(&chunk_list[chunk_pos], {rho, phi, theta}, {drho, dphi, dtheta}, &gen, updater);
			}
			std::cout << "New chunk made at idx: " << chunk_pos << "\n";
			chunk_pos++;
		}
		else if (cmd == "delchunk")
		{
			std::cin >> chunk_idx;
			
			assert((chunk_idx < chunk_pos));
			
			assert((chunk_idx >= 0 && chunk_idx < 64));
			
			chunk_list[chunk_idx].~SphereChunk();
		}
		else if (cmd == "meshchunk")
		{
			std::cin >> chunk_idx;	
						
			assert((chunk_idx >= 0 && chunk_idx < 64));
			
			print_mesh(chunk_list[chunk_idx]);
		}
		else if (cmd == "info")
		{
			std::cin >> chunk_idx;	
						
			assert((chunk_idx >= 0 && chunk_idx < 64));
			
			auto& temp = (chunk_list[chunk_idx]);
			std::cout << temp << "\n";
		}
		else if (cmd == "mupdate")
		{
			if (n != nullptr){
				n->update_mesh();
			}
			else
			{
				std::cout << "Nope..\n";
			}
		}
		else if (cmd == "heapChunk")
		{
			if (! n){
				n = (SphereChunk*)smalloc(sizeof(SphereChunk));
				make_SphereChunk(n, svec3(8,.982,-.0368), svec3(16, .0625, .0736), &gen, updater);
				std::cout << *n << "\n";
			}
		}
		else if (cmd == "freeChunk")
		{
			std::cout << *n << "\n";
			free(n);
			n = nullptr;
		}
		else
		{
			std::cout << "Couldn't parse command '" << cmd << "'...\n";
		}
	}
	
	return 0;
}
