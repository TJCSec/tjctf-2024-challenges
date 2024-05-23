#include "common.hpp"
#include <vector>

class Updater
{
public:
	virtual bool update_mesh(std::vector<Vertex>& vbuf, std::vector<uint32_t>& ibuf);
};

class DummyUpdater : public Updater
{
public:
	bool update_mesh(std::vector<Vertex>& vbuf, std::vector<uint32_t>& ibuf);
};
