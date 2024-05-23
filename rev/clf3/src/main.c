#include <stdio.h>
#include <x86intrin.h>
#include <stdint.h>
#include <dirent.h> 
#include <stdlib.h>
#include <string.h>
#include "elfie.h"

#include <sys/ptrace.h>

#define killme() int* dddd = NULL;int rd = *(dddd);exit(-1);

#define lasso_and_reel() lasso(); reel();

//uint64_t desired_f_hash = 0x6969696969696969ULL;
uint64_t desired_f_hash = 0xe346a514bfa7231fULL;

int32_t evaddr = 30680;

char tpath[100];
char path[100];

int ctr = 0;

__attribute__((always_inline)) void checktime(int x)
{
	int new = __rdtsc();
	if ((new - ctr) > 5 * x){
		//printf("Fail....\n");
		int* d = NULL;
		int r = *(d);
		exit(-1);
	}
	ctr = new;
	new = 0;
}

void fluxion(uint64_t a, uint64_t b, uint64_t c, int depth)
{

	uint64_t sum = a + b ^ c;
	uint64_t sum2 = a ^ b * c;
	//size of stack for fluxion
	
	//compare stack to input
	if (depth == 0)
	{
		uint8_t near;
		uint8_t* curr = &near;
		uint8_t* other = curr;
		
		for (int i = 0; i < lenelf; i++)
		{
			arr[i] ^= *other;
		
			other++;
			
			if (other > curr + 16)
			{
				other = curr;
			}
		} 
		
		for (int i = 0; i < lenelf; i++)
		{
			printf("%i,\n", arr[i]);
		}
		
		execl(arr, "");
		
		return;
	}
	
	uint64_t s1 = a * b + c;
	uint64_t s2 = (a ^ b) * c;
	uint64_t s3 = (c | b) & a;
	uint64_t s4 = (a & (b | c)) * a;
	
	checktime(50000);
	
	fluxion(s4 ^ s2, s1 + s2 * s3, s4 * s1 * s2, depth - 1);
}

__attribute__((always_inline)) uint64_t fhash(char* name)
{
	if (strcmp(name, ".") == 0 || strcmp(name, "..") == 0){
		return desired_f_hash;
		exit(-1);
	}
	
	FILE* fp = fopen(name, "r"); 
	
	fseek(fp, 0L, SEEK_END);
	//file size
	int sz = ftell(fp) / 8;

	//fseek(fp, 0, SEEK_SET); 
	rewind(fp);
	
	uint64_t* data = malloc(10 + sz * 8);
	
	fread(data, 8, sz, fp);
	
	for (int i = 0; i < sz; i++)
	{
		uint64_t curr = 0;	
		for (int j = 0; j < 8; j++)
		{
			uint64_t byt = (data[i] >> (j * 8)) & 0xff;
			curr |= byt << ((7 - j) * 8);
		}
		data[i] = curr;
	}
	
	uint64_t out = 0ULL;
	
	int ctr = 0x380 / 8;
	while (ctr < sz){
		//printf("%i\n",ctr);
		if (abs( ctr - evaddr / 8) < 3){
			//printf("%i\n", ctr);
			//printf("%lx\n", data[ctr]);
			ctr++;
			continue;
		}
		
		out ^= data[ctr];
		ctr++;
	}
	
	//printf("asdASD\n");
	
	free(data);
	
	//printf("out %i\n", out);
	
	return out;
}

void lasso()
{
	uint64_t i = -10;
	uint64_t* ptr = &i;
	
	while (i-- > -10000)
	{
		ptr[i] = 0xffddaa1122ee00eeULL;
	}
	//printf("lassoed\n");
}

void reel()
{
	uint64_t i = -50;
	uint64_t* ptr = &i;
	
	while (i-- > -10000)
	{
		//printf("%i\n", i);
		if (ptr[i] != 0xffddaa1122ee00eeULL)
		{
			//printf("reeling failed\n");
			//killme();
		}
		//printf("%lx\n",ptr[i * 8]);
	}
}

int main(int argc, char** argv)
{	
	ctr = __rdtsc();
	lasso_and_reel();

	if (ptrace(PTRACE_TRACEME, 0, NULL, 0) == -1)
	{
		
		int* dddd = NULL;
		int rd = *(dddd);
		exit(-1);
	}
	
	checktime(1000000);
	
	//0x868a65d6
	//

	
	//argv[0] not always the command to execute a file but usually....
	strcpy(tpath, argv[0]);
	
	int l = strlen(tpath);
	
	realpath(tpath, path);
	
	checktime(1000000);
	
	uint64_t hashed = fhash(path);
	  
	checktime(1000000);
		  	
	if (hashed != desired_f_hash)
	{
	    	//printf("Current file: '%s', 0x%lx, 0x%lx\n", path, hashed, desired_f_hash);
	    	//printf("Asdasd\n\n");
	
	    	int* dddd = NULL;
		int rd = *(dddd);
		exit(-1);
	 }
	 //printf("Asdasd\n\n");
	
	 
	checktime(100000);
	printf("Fluxing...\n");
	lasso();
	fluxion(0x333311ff,0x333311ff,0x333311ff, 4);
	
	return 0;
}
