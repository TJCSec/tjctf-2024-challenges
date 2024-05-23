#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <malloc.h>
#include <assert.h>

#include "sphere_engine.hpp"

int main()
{
	std::cout << "Hello world!\n";

	std::cout << M_PI << "\n";

	test_coords();

	siv::PerlinNoise gen;
	
	gen.reseed(100);
	
	Updater* updater = new DummyUpdater(); 
	
	SphereChunk chunkList[64];
	
	//attack starts here
	chunkList[0] = (SphereChunk({120, 1.0451142178632642, -0.002405626121623441}, {240, 0.004166666666666667, 0.004811252243246882}, &gen, updater));
	chunkList[1] = (SphereChunk({120, 1.0451142178632642, -0.002405626121623441}, {240, 0.004166666666666667, 0.004811252243246882}, &gen, updater));
	chunkList[2] = (SphereChunk({120, 1.0451142178632642, -0.002405626121623441}, {240, 0.004166666666666667, 0.004811252243246882}, &gen, updater));
	
	std::cout << chunkList[0].verts << " " << chunkList[0].vol << "\n";
	std::cout << chunkList[1].verts << " " << chunkList[1].vol << "\n";
	std::cout << chunkList[2].verts << " " << chunkList[2].vol << "\n";
	
	std::cout << (uint8_t) chunkList[1].ref(0, 0, 240).type << "\n";
	
	chunkList[0].ref(0, 0, 240).type = 0x51;
	
	std::cout << (int)chunkList[1].ref(0, 0, 240).type << "\n";
	chunkList[1].~SphereChunk();	
}
