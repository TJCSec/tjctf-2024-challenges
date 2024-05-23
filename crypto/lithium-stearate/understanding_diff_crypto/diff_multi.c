//Jon King
//Iterative Characteristics Tutorial
//#include <math.h>
#include <stdio.h>
#include <time.h>

int sbox[16] = {3, 14, 1, 10, 4, 9, 5, 6, 8, 11, 15, 2, 13, 12, 0, 7};
int sboxRev[16] = {14, 2, 11, 0, 4, 6, 7, 15, 8, 5, 3, 9, 13, 12, 1, 10};
int pbox[8] = {1, 6, 0, 7, 2, 3, 5, 4};
int pboxRev[8] = {2, 0, 4, 5, 7, 6, 1, 3};

int mySPBox[256];
int chars[256][256];

int revSPBox(int input)
{
    int c;
    for(c = 0; c < 256; c++)
    {
        if (mySPBox[c] == input) return c;    
    }    
}

int pow(int b, int e)
{
    int tot = 1;
    for (int i = 0; i < e; i++) {
        tot *= b;
    }
    return tot;
}

int spBox(int input)
{
    int lefthalf = input / 16;
    int righthalf = input & 15;
    lefthalf = sbox[lefthalf];
    righthalf = sbox[righthalf];
    int combined = lefthalf * 16 + righthalf;
    
    int total = 0;
    int c;
    for(c = 0; c < 8; c++)
    {
         int inBit = combined % (int)(pow(2, c + 1));
         inBit = inBit / (int)(pow(2, c));
         total += inBit * pow(2, pbox[c]);   
    }
    return total;  
}

void createSPBox()
{
    int c;
    for(c = 0; c < 256; c++)
        mySPBox[c] = spBox(c);    
}

int roundFunc(int input, int subkey)
{
    return mySPBox[input ^ subkey];    
}

int encrypt(int input, int k0, int k1, int k2, int k3)
{
    int r0 = roundFunc(input, k0);
    int r1 = roundFunc(r0, k1);  
    int r2 = roundFunc(r1, k2);
    return roundFunc(r2, k3);   
}

void genChars()
{
    printf("\nFinding good differential characteristics:\n");
    
    int c, d;
        
    for(c = 0; c < 256; c++)
        for(d = 0; d < 256; d++)
        {
            int indiff = c ^ d;
            int outdiff = mySPBox[c] ^ mySPBox[d];
            chars[indiff][outdiff]++;   
        }  
        
    for(c = 0; c < 256; c++)
    {
        for(d = 0; d < 256; d++)
        {
            if ((chars[c][d] >= 64) && (chars[c][d] < 256)) 
                printf("  %i:  %i --> %i\n", chars[c][d], c, d);    
        }    
    }  
}

int goodP0, goodP1, goodC0, goodC1;
int knownP[1000];
int knownC[1000];
int numPairs = 100;

int choosePairs(int indiff, int outdiff)
{
    printf("\nCreating chosen plaintext/ciphertext pairs:\n");
   
    int k0 = 102;// rand() % 256;
    int k1 = 83;// rand() % 256;
    int k2 = 171;// rand() % 256;
    int k3 = 186;// rand() % 256;
    
    printf("  REAL KEY = %i, %i, %i, %i\n", k0, k1, k2, k3);
    
    int c;
    for(c = 0; c < numPairs; c++)
    {
        knownP[c] = rand() % 256;
        knownC[c] = encrypt(knownP[c], k0, k1, k2, k3);
        knownC[c] = revSPBox(knownC[c]); 
    }
    
    printf("  Generated %i known pairs\n", numPairs);
    
    printf("  Searching for good pair...");
    int g;
    for(g = 0;g < 256; g++)
    {
        int testP0 = rand() % 256;
        int testP1 = testP0 ^ indiff;
        int testC0 = encrypt(testP0, k0, k1, k2, k3);
        testC0 = revSPBox(testC0);
        int testC1 = encrypt(testP1, k0, k1, k2, k3);
        testC1 = revSPBox(testC1);
        
        if ((testC0 ^ testC1) == outdiff)
        {
            goodP0 = testP0;
            goodP1 = testP1;
            goodC0 = testC0;
            goodC1 = testC1;

            printf("GOOD PAIR FOUND:  %i + %i --> P: %i + %i C: %i + %i\n", indiff, outdiff, goodP0, goodP1, goodC0, goodC1);

            return 1;    
        }
            
    } 
    return 0;
}

int box1x0[256], box1x1[256], box1y0[256], box1y1[256];
int box2x0[256], box2x1[256], box2y0[256], box2y1[256];
int box3x0[256], box3x1[256], box3y0[256], box3y1[256];
int box1max, box2max, box3max;

void genCharData()
{
    printf("\nFinding input/output values for path(176 --> 192):\n");
    
    box1max = 0;
    box2max = 0;
    box3max = 0;
    
    printf("  Finding the 64 values for 176 --> 4:\n");
    
    int c, d;
    for(c = 0; c < 256; c++)
    {
        int x0 = c;
        int x1 = x0 ^ 176;
        int y0 = mySPBox[x0];
        int y1 = mySPBox[x1];
        if ((y0 ^ y1) == 4)
        {
            box1x0[box1max] = x0;
            box1x1[box1max] = x1;
            box1y0[box1max] = y0;
            box1y1[box1max] = y1;
            box1max++;
       }    
    }    
   

    printf("  Finding the 64 values for 4 --> 3:\n");
    
    for(c = 0; c < 256; c++)
    {
        int x0 = c;
        int x1 = x0 ^ 4;
        int y0 = mySPBox[x0];
        int y1 = mySPBox[x1];
        if ((y0 ^ y1) == 3)
        {
            box2x0[box2max] = x0;
            box2x1[box2max] = x1;
            box2y0[box2max] = y0;
            box2y1[box2max] = y1;
            box2max++;
       }    
    } 
    
    printf("  Finding the 64 values for 3 --> 192:\n");
    
    for(c = 0; c < 256; c++)
    {
        int x0 = c;
        int x1 = x0 ^ 3;
        int y0 = mySPBox[x0];
        int y1 = mySPBox[x1];
        if ((y0 ^ y1) == 192)
        {
            box3x0[box3max] = x0;
            box3x1[box3max] = x1;
            box3y0[box3max] = y0;
            box3y1[box3max] = y1;
            box3max++;
       }    
    }    
}

int crack()
{
    int c, d, e;
    
    for (c = 0; c < box1max; c++)
    {
        printf("%i, ", box1x0[c]);
    }
    printf("\n");
    for (c = 0; c < box2max; c++)
    {
        printf("%i, ", box2x0[c]);
    }
    printf("\n");
    for (c = 0; c < box3max; c++)
    {
        printf("%i, ", box3x0[c]);
    }


    printf("\nTesting %i * %i * %i keys\n", box1max, box2max, box3max);


    for(c = 0; c < box1max; c++)
    {
        for(d = 0; d < box2max; d++)
        {
            for(e = 0; e < box3max; e++)
            {
                int testK0 = box1x0[c] ^ goodP0;
                int testK1 = box1y0[c] ^ box2x0[d];
                int testK2 = box2y0[d] ^ box3x0[e];
                int testK3 = box3y0[e] ^ goodC0;
                
                //printf("Testing key: %i %i %i %i\n", testK0, testK1, testK2, testK3);

                int f;
                int crap = 0;
                for(f = 0; f < numPairs; f++)
                    if (revSPBox(encrypt(knownP[f], testK0, testK1, testK2, testK3)) != knownC[f])
                    {
                        crap = 1;
                        break;    
                    }
                if (crap == 0)
                {
                    printf("  KEY FOUND!  %i, %i, %i, %i\n", testK0, testK1, testK2, testK3);
                    return 1;  
                }
            }    
        }    
    } 
    printf("  NO KEY FOUND!\n");   
    return 0;
}

int main()
{
    srand(time(NULL));
    
    printf("%i %i %i\n", pow(2, 0), pow(2, 1), pow(2, 4));

    createSPBox();

    for (int i = 0; i < 256; i++)
    {
        printf("%i,", mySPBox[i]);
    }
    printf("\n");

    printf("104: %i\n", encrypt(104, 102, 83, 171, 186));
    printf("216: %i\n", encrypt(216, 102, 83, 171, 186));

    genChars();
    genCharData();
    
   
    
    if (choosePairs(176, 192) == 0)
        printf("NO GOOD PAIR FOUND\n");
    else
        crack();

    while(1){}
    return 0;    
}
