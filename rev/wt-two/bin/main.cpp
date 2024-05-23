#include <iostream>
#include <cstring>
#include <string>

constexpr int calc_fib = 3;


int main(int argc, char* argv[])
{	
		
	//base case
	if (argc == 1)
	{
		std::string input;
	
		std::cout<<"Guess my flag!!\n";
	
		std::cin >> input;
		
		if (input.size() < 30)
		{
			goto nope;
		}
	
		char* strs[1];
		strs[0] = new char[4];

		int message[] = {117, 107, 97, 119, 99, 115, 122, 97, 15, 67, 49, 245, 196, 269, 533, 948, 1618, 2679, 4154, 6658, 10915, 17756, 28613, 46360, 75060, 121457, 196390, 317717, 514246, 832085};
		for (int i = 0; i < 30; i++)
		{
			std::memcpy(strs[0], &i, 4);
			if (input[i] != (char)(message[i] ^ main(calc_fib, strs)))
			{
				goto nope;
			}
		}
		
		std::cout<<"Nice!!!";
		
		return 1;
	}
	
	//calculate fibonacci
	if (argc == calc_fib)
	{
	
		int curr;
		//std::cout<<argv[0]<<"\n";
		std::memcpy(&curr, argv[0], 4);
		
		//std::cout << "Curr: "<<curr << "\n";
		
		if (curr == 0 || curr == 1) {
			return 1;
		}
		
		char* strs[1];
		strs[0] = new char[4];
		
		int temp = curr - 1;
		
		std::memcpy(strs[0], &temp, 4); 
		
		int output = 0;
		output += main(calc_fib, strs);
		
		temp--;
		
		std::memcpy(strs[0], &temp, 4); 

		output += main(calc_fib, strs);
		
		return output;
	}
	
	
	nope:
	std::cout<<"Wrong...\n";
	return -1;

	return 0;
}
