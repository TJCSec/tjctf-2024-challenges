#include <stdio.h>
#include <inttypes.h>
#define add 0xff
#define sub 0xaa
#define inc_ptr 0x11
#define dec_ptr 0x22
#define stacksize 1024
#define load_rax 0xcc
#define read_rax 0xca
#define set_stack 0xdc
#define go 0xdd
#define kill 0x00
#define num_instr 1000
int rax = 0;
int rsp = 0;
int dir = 0;
//tjctf{Not_2_c0mplic2ted1ffaa1191099q221}
uint8_t stack[stacksize]; //tjctf{Not_2_c0mplic2ted1ffaa1191099q221}
char arr[stacksize] = "\x02vlevh}Pqva4ae2ornke4vgf3hhcc33;32;;q221}";
uint8_t instructions[num_instr] = {read_rax, inc_ptr, add, inc_ptr, add, inc_ptr, add, inc_ptr, add, inc_ptr, add, inc_ptr, add, inc_ptr, add, inc_ptr, add, inc_ptr, add, inc_ptr, add, inc_ptr, add, inc_ptr, add, inc_ptr, add, inc_ptr, add, inc_ptr, add, inc_ptr, add, inc_ptr, add, inc_ptr, add, inc_ptr, add, inc_ptr, add, inc_ptr, add, inc_ptr, add, inc_ptr, add, inc_ptr, add, inc_ptr, add, inc_ptr, add, inc_ptr, add, inc_ptr, add, inc_ptr, add, inc_ptr, add, inc_ptr, add, inc_ptr, add, inc_ptr, add, inc_ptr, add, inc_ptr, add};

int compute()
{
	
	uint8_t i = instructions[dir];
	//printf("%i %i %i %i\n",rax, rsp, dir, i);
	if (i == add)
	{
		stack[rsp] += rax;
	}
	if (i == sub)
	{
		stack[rsp] -= rax;
	}
	if (i == inc_ptr)
	{
		rsp++;
	}
	if (i == dec_ptr)
	{
		rsp--;
	}
	if (i == load_rax)
	{
		stack[rsp] = rax;
	}
	if (i == read_rax)
	{
		//printf("reading rax...\n");
		rax = stack[rsp];
	}
	if (i == set_stack)
	{
		rsp = rax;
	}
	if (i == kill)
	{
		return 0;
	}
	
	if (i == go)
	{
		dir = rax;
	}
	else{
		dir++;
	}
	return 1;
}

int main()
{
	for (int i = 0; i < stacksize; i++)
	{
		stack[i] = 0;
	}
	
	for (int i = 0; i < stacksize; i++)
	{
		stack[i] = arr[i];
	}
	
	while (compute())
	{
	}
	
	for (int i = 0; i < stacksize; i++)
	{
		arr[i] = stack[i];
	}
	
	printf("%s\n",&arr[1]);
	
	
	
	return 0;
}
