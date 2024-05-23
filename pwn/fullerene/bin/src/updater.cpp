#include "updater.hpp"

bool Updater::update_mesh(std::vector<Vertex>& vbuf, std::vector<uint32_t>& ibuf)
{
	std::cout << "Base Class Updater Update Called!\n";
	return false;
}


bool DummyUpdater::update_mesh(std::vector<Vertex>& vbuf, std::vector<uint32_t>& ibuf) 
{
	std::cout << "Dummy Updater Update Called!\n";
	return true;
}
