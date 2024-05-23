#include <x86intrin.h>
#include <stdio.h>
#include <inttypes.h>

void lasso()
{
	uint64_t i = -10;
	uint64_t* ptr = &i;
	
	while (i-- > -1000)
	{
		ptr[i] = 0x420420420420420ULL;
		//printf("asdasd\n");
	}
	//printf("lassoed\n");
}
int tester(int* a, int d)
{
	int my=0x6969696969696969;
	int* myptr = &my;
	if (d==0)
	{
		if (myptr < a){
			printf("Less\n");
			for (int i = -100; i < 100; i++)
			{
				if (i == 0)
					printf("We are here!\n");
				printf("Two: %lx\n", myptr[i]);
			}
		}
		else
		{		
		printf("More\n");
		}
	        return;
	}
	tester(myptr, d-1);
}

int ctr = 0;
__attribute__((always_inline)) void checktime(int x)
{
	int new = __rdtsc();
	if ((new - ctr) > 5 * x){
		//printf("Fail....\n");
		int* d = 0;
		int r = *(d);
		exit(-1);
	}
	ctr = new;
	new = 0;
}

int main()
{
ctr =  __rdtsc();
	uint64_t i = -10;
	uint8_t a;
	uint8_t* ptr = &a;
	
	while (i-- > -11000)
	{
		ptr[i] = 0x69ULL;
		//printf("asdasd\n");
	}
	
	checktime(100000000);
	
	int my=0x6969696969696969;
	int* myptr = &my;
	for (int i = -50; i < 0; i++)
			{
				if (i == 0)
					printf("We are here!\n");
				printf("%lx\n", myptr[i]);
			}
	//tester(0, 1);
}
