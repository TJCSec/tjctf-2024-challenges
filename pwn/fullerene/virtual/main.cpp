#include <iostream>
#include <cstdint>

void win()
{
	std::cout << "Hello world! Win!!!\n";
}

class Parent
{
	public:
	uint64_t i = 0;

	Parent()
	{
		i = 0xdeadbeef;
	}
	
	virtual void test()
	{
		std::cout << "Parent test...\n";
	}
};

class Child : public Parent
{
	public:
	
	Child()
	{
		this->i = 0xdeadbeef;
	}
	
	void test()
	{
		std::cout << "Child test...\n";
	}
};

static int a = 0;

int main()
{	

	int* heap = new int[1];
	std::cout << sizeof(Parent) << " " << sizeof(Child) << " " << &a << " " << heap << "\n";
	Parent old = Parent();
	std::cout << "0x" << std::hex << *(uint64_t*) &old << "\n";
	std::cout << std::dec <<  (uint64_t)heap - (uint64_t)(*(uint64_t*) &old) << "\n";
	Child oldish = Child();
	Parent* ptr = &oldish;

	Parent* heaped = new Parent[1];

	std::cout << &old << " " << &oldish << "\n";

	uint64_t* idr = (uint64_t*)win;

	*(uint64_t***)(heaped) = &idr;

	heaped->test();
	ptr->test();
}
