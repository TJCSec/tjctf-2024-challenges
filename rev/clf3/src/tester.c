#include <stdio.h>
#include <x86intrin.h>
#include <stdint.h>
#include <dirent.h> 
#include <stdlib.h>
#include <string.h>
#include <inttypes.h>

//0x82c1697eb7882d1e

int32_t evaddr = 12432;


int ctr = 0;

__attribute__((always_inline)) void checktime(int x)
{
	int new = __rdtsc();
	if (new - ctr > x){
		printf("Fail....\n");
		int* d = NULL;
		int r = *(d);
		exit(-1);
	}
	ctr = new;
}

void fluxion(uint64_t a, uint64_t b, uint64_t c, int depth, char* chararr)
{
	//size of stack for fluxion
	int stack;
	
	//compare stack to input
	if (depth == 0)
	{
		return;
	}
	
	uint64_t s1 = a * b + c;
	uint64_t s2 = (a ^ b) * c;
	uint64_t s3 = (c | b) & a;
	uint64_t s4 = (a & (b | c)) * a;
	
	checktime(250);
	
	fluxion(s4 ^ s2, s1 + s2 * s3, s4 * s1 * s2, depth - 1, chararr);
}

void checkhash(uint64_t* w1, uint64_t* w2, uint64_t hash)
{
	uint64_t out = 1ULL;
	
	while (w1 != w2)
	{
		out *= (out >> 2) ^ *w1;
		w1++;
		checktime(150);	
	}
	
	if (out == hash){
		printf("%l", out);
		int* d = NULL;
		int r = *(d);
		exit(-1);
	}
}

__attribute__((always_inline)) uint64_t fhash(char* name)
{
	if (strcmp(name, ".") == 0 || strcmp(name, "..") == 0){
		return 1;
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

__attribute__((always_inline)) void fcheckhash()
{
	DIR *d;
	struct dirent *dir;
	d = opendir(".");
	
	if (d) {
	  while ((dir = readdir(d)) != NULL) {
	  	printf("Processing %s\n", dir->d_name);
	  	uint64_t hashed = fhash(dir->d_name);
	  
			  	

	    {
	    	printf("Current file: '%s', 0x%lx\n", dir->d_name, hashed);
	    	
	    	//int* dddd = NULL;
		//int rd = *(dddd);
		//exit(-1);
	    }
	  }
	  closedir(d);
	}
}

int main(int argc, char** argv)
{
	ctr = __rdtsc();
	
	scanf("%d", &evaddr);
	
	printf("%i", evaddr);
	
	fcheckhash();
	
	
	return 0;
}
