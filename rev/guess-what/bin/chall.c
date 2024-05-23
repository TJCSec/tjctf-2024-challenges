#include <stdio.h>
#include <string.h>

int main()
{
    setbuf(stdout, NULL);

    puts("welcome to the guessing game!");

    puts("guess what I'm thinking");

    char guess_buf[64];
    fgets(guess_buf, sizeof(guess_buf), stdin);

    if (strcmp(guess_buf, "nuh uh pls nolfjdl\n") != 0)
    {
        puts("nuh uh!");
        return 1;
    }

    puts("please guess a number between 0 and 100:");

    int guess;
    scanf("%d", &guess);

    if (guess == 42 * 9 / guess + 3)
    {
        puts("congratulations! you guessed the correct number!");
    }
    else
    {
        puts("sorry, you guessed the wrong number!");
    }

    FILE *flag = fopen("flag.txt", "r");

    if (flag == NULL)
    {
        puts("flag.txt not found - ping us on discord if you are running this on the server");
        return 1;
    }

    char flag_buf[64];
    fgets(flag_buf, sizeof(flag_buf), flag);

    puts(flag_buf);
}
