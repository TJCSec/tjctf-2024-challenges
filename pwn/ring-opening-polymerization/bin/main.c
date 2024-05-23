#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <malloc.h>
#include <assert.h>


void gadget1()
{
        __asm__("pop %rdi\n\t"
        "ret\n\t");
}


void win(uint64_t i)
{
        FILE* f = fopen("flag.txt", "r");
        char buf[100];
        fgets(buf, 35, f);
        
        printf("%i\n", i);

        if (i == 0xdeadbeef)
        {
                printf("%s\n",buf);
                fflush(stdout);
        }
        else{
                printf("Bad!\n");
        }
}


int main()
{       
        char buf[8];
        gets(buf);
        return 0;
}