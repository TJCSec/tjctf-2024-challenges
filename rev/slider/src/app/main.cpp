#define NUM_CHANNELS 3

#include <SDL2/SDL.h>
#include <iostream>
#include <vector>
#include <algorithm>
#include <string>

using std::string;
using std::vector;

SDL_Window *window = NULL;
SDL_Renderer *renderer = NULL;
SDL_Texture *texture = NULL;

SDL_MouseButtonEvent mouseDownEvent;

uint8_t *pixels = NULL;

struct SliderBlock
{
    int r;
    int c;
    int correctR;
    int correctC;
    int width;
    int height;
    uint8_t *data;
};

void render(vector<SliderBlock> &puzzle, int windowWidth, int windowHeight);
void readSaveFile(string filename, vector<SliderBlock> &puzzle, int &blockWidth, int &blockHeight, int &puzzleWidth, int &puzzleHeight);
void writeSaveFile(string filename, vector<SliderBlock> &puzzle, int blockWidth, int blockHeight, int puzzleWidth, int puzzleHeight);
int signum(int x);
void swapBlock(SliderBlock &a, SliderBlock &b);
void shuffle(vector<SliderBlock> &puzzle, int &puzzleWidth, int &puzzleHeight);
bool isSolved(vector<SliderBlock> &puzzle);
bool moveEmpty(vector<SliderBlock> &puzzle, int puzzleHeight, int puzzleWidth, int dr, int dc);

SliderBlock *emptyBlock;

int main(int argc, char *argv[])
{
    srand(time(NULL));

    int blockWidth, blockHeight;
    int puzzleWidth, puzzleHeight;
    vector<SliderBlock> puzzle;

    string filename = argc >= 2 ? argv[1] : "save.dat";
    readSaveFile(filename, puzzle, blockWidth, blockHeight, puzzleWidth, puzzleHeight);

    int windowWidth = puzzleWidth * blockWidth;
    int windowHeight = puzzleHeight * blockHeight;

    if (isSolved(puzzle))
        shuffle(puzzle, puzzleWidth, puzzleHeight);

    if (SDL_Init(SDL_INIT_VIDEO) < 0)
    {
        std::cout << "SDL could not initialize! SDL_Error: " << SDL_GetError() << std::endl;
        return 1;
    }

    SDL_CreateWindowAndRenderer(windowWidth, windowHeight, SDL_WINDOW_SHOWN, &window, &renderer);

    string title = "Slider - " + filename;
    SDL_SetWindowTitle(window, title.c_str());

    if (window == NULL || renderer == NULL)
    {
        std::cout << "Window could not be created! SDL_Error: " << SDL_GetError() << std::endl;
        return 1;
    }

    texture = SDL_CreateTexture(renderer, SDL_PIXELFORMAT_RGB24, SDL_TEXTUREACCESS_STREAMING, windowWidth, windowHeight);

    if (texture == NULL)
    {
        std::cout << "Texture could not be created! SDL_Error: " << SDL_GetError() << std::endl;
        return 1;
    }

    pixels = new uint8_t[windowWidth * windowHeight * NUM_CHANNELS];

    bool running = true;
    bool solved = false;

    while (running)
    {
        SDL_Event event;
        if (SDL_PollEvent(&event))
        {
            switch (event.type)
            {
            case SDL_QUIT:
                running = false;
                break;
            case SDL_KEYDOWN:
                switch (event.key.keysym.sym)
                {
                case SDLK_ESCAPE:
                    running = false;
                    break;
                case SDLK_l:
                    shuffle(puzzle, puzzleWidth, puzzleHeight);
                    break;
                case SDLK_p:
                    writeSaveFile("save.dat", puzzle, blockWidth, blockHeight, puzzleWidth, puzzleHeight);
                    break;
                case SDLK_w:
                case SDLK_UP:
                    moveEmpty(puzzle, puzzleHeight, puzzleWidth, -1, 0);
                    break;
                case SDLK_s:
                case SDLK_DOWN:
                    moveEmpty(puzzle, puzzleHeight, puzzleWidth, 1, 0);
                    break;
                case SDLK_a:
                case SDLK_LEFT:
                    moveEmpty(puzzle, puzzleHeight, puzzleWidth, 0, -1);
                    break;
                case SDLK_d:
                case SDLK_RIGHT:
                    moveEmpty(puzzle, puzzleHeight, puzzleWidth, 0, 1);
                    break;
                }
                break;
            case SDL_MOUSEBUTTONDOWN:
                if (event.button.button == SDL_BUTTON_LEFT)
                    mouseDownEvent = event.button;
                break;
            case SDL_MOUSEBUTTONUP:
                if (event.button.button == SDL_BUTTON_LEFT)
                {
                    // Switch row
                    int dr = signum(event.button.y - mouseDownEvent.y);
                    int dc = signum(event.button.x - mouseDownEvent.x);
                    if (abs(event.button.y - mouseDownEvent.y) > abs(event.button.x - mouseDownEvent.x))
                        dc = 0;
                    else
                        dr = 0;

                    moveEmpty(puzzle, puzzleHeight, puzzleWidth, dr, dc);
                }
                break;
            }
        }

        if (isSolved(puzzle) && !solved)
        {
            SliderBlock &lb = puzzle[puzzle.size() - 1];

            for (int i = 0; i < blockWidth * blockHeight * NUM_CHANNELS; i++)
            {
                for (auto &b : puzzle)
                {
                    if (b.r == lb.r && b.c == lb.c)
                        continue;

                    lb.data[i] ^= b.data[i];
                }

                if (i % (blockWidth * NUM_CHANNELS) == 0)
                {
                    SDL_Delay(5);
                    render(puzzle, windowWidth, windowHeight);
                }
            }

            solved = true;
        }
        else if (!isSolved(puzzle) && solved)
        {
            solved = false;
        }

        render(puzzle, windowWidth, windowHeight);
    }

    delete[] pixels;

    for (int i = 0; i < puzzle.size(); i++)
        free(puzzle[i].data);

    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();
}

void readSaveFile(string filename, vector<SliderBlock> &puzzle, int &blockWidth, int &blockHeight, int &puzzleWidth, int &puzzleHeight)
{
    FILE *saveFile = fopen(filename.c_str(), "rb");

    fread(&blockWidth, sizeof(int), 1, saveFile);
    fread(&blockHeight, sizeof(int), 1, saveFile);
    fread(&puzzleWidth, sizeof(int), 1, saveFile);
    fread(&puzzleHeight, sizeof(int), 1, saveFile);

    for (int i = 0; i < puzzleWidth * puzzleHeight; i++)
    {
        puzzle.push_back(SliderBlock());
        SliderBlock &block = puzzle[puzzle.size() - 1];
        fread(&block.r, sizeof(int), 1, saveFile);
        fread(&block.c, sizeof(int), 1, saveFile);
        fread(&block.correctR, sizeof(int), 1, saveFile);
        fread(&block.correctC, sizeof(int), 1, saveFile);
        block.width = blockWidth;
        block.height = blockHeight;
        uint8_t *data = (uint8_t *)malloc(block.width * block.height * NUM_CHANNELS);
        fread(data, sizeof(uint8_t), block.width * block.height * NUM_CHANNELS, saveFile);
        block.data = data;

        if (block.correctR == puzzleHeight - 1 && block.correctC == puzzleWidth - 1)
            emptyBlock = &puzzle[puzzle.size() - 1];
    }

    // sort by location
    sort(puzzle.begin(), puzzle.end(), [puzzleWidth = puzzleWidth](const SliderBlock &a, const SliderBlock &b)
         { return a.r * puzzleWidth + a.c < b.r * puzzleWidth + b.c; });

    fclose(saveFile);
}

void writeSaveFile(string filename, vector<SliderBlock> &puzzle, int blockWidth, int blockHeight, int puzzleWidth, int puzzleHeight)
{
    FILE *saveFile = fopen(filename.c_str(), "wb");

    fwrite(&blockWidth, sizeof(int), 1, saveFile);
    fwrite(&blockHeight, sizeof(int), 1, saveFile);
    fwrite(&puzzleWidth, sizeof(int), 1, saveFile);
    fwrite(&puzzleHeight, sizeof(int), 1, saveFile);

    for (int i = 0; i < puzzle.size(); i++)
    {
        SliderBlock &block = puzzle[i];
        fwrite(&block.r, sizeof(int), 1, saveFile);
        fwrite(&block.c, sizeof(int), 1, saveFile);
        fwrite(&block.correctR, sizeof(int), 1, saveFile);
        fwrite(&block.correctC, sizeof(int), 1, saveFile);
        fwrite(block.data, sizeof(uint8_t), block.width * block.height * NUM_CHANNELS, saveFile);
    }

    fclose(saveFile);
}

void shuffle(vector<SliderBlock> &puzzle, int &puzzleWidth, int &puzzleHeight)
{
    for (int i = 0; i < 100; i++)
    {
        int r = rand() % 4;
        int newR = emptyBlock->r;
        int newC = emptyBlock->c;

        switch (r)
        {
        case 0:
            newR--;
            break;
        case 1:
            newR++;
            break;
        case 2:
            newC--;
            break;
        case 3:
            newC++;
            break;
        }

        if (newR < 0 || newR >= puzzleHeight || newC < 0 || newC >= puzzleWidth)
        {
            continue;
        }

        swapBlock(puzzle[emptyBlock->r * puzzleWidth + emptyBlock->c], puzzle[newR * puzzleWidth + newC]);
        emptyBlock = &puzzle[newR * puzzleWidth + newC];
    }
}

bool isSolved(vector<SliderBlock> &puzzle)
{
    for (int i = 0; i < puzzle.size(); i++)
    {
        SliderBlock &block = puzzle[i];
        if (block.r != block.correctR || block.c != block.correctC)
            return false;
    }

    return true;
}

void render(vector<SliderBlock> &puzzle, int windowWidth, int windowHeight)
{
    SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
    SDL_RenderClear(renderer);

    for (int i = 0; i < puzzle.size(); i++)
    {
        SliderBlock &block = puzzle[i];
        for (int r = 0; r < block.height; r++)
        {
            uint8_t *pixel = &pixels[(block.r * block.width + r) * windowWidth * NUM_CHANNELS + (block.c * block.width + 0) * NUM_CHANNELS];
            uint8_t *data = block.data + r * block.width * NUM_CHANNELS;

            memcpy(pixel, data, block.width * NUM_CHANNELS);
        }
    }

    SDL_UpdateTexture(texture, NULL, pixels, windowWidth * NUM_CHANNELS);

    SDL_RenderCopy(renderer, texture, NULL, NULL);
    SDL_RenderPresent(renderer);
}

int signum(int x)
{
    return (x > 0) - (x < 0);
}

bool moveEmpty(vector<SliderBlock> &puzzle, int puzzleHeight, int puzzleWidth, int dr, int dc)
{
    int newR = emptyBlock->r - dr;
    int newC = emptyBlock->c - dc;

    if (newR < 0 || newR >= puzzleHeight || newC < 0 || newC >= puzzleWidth)
        return false;

    swapBlock(puzzle[emptyBlock->r * puzzleWidth + emptyBlock->c], puzzle[newR * puzzleWidth + newC]);
    emptyBlock = &puzzle[newR * puzzleWidth + newC];

    return true;
}

void swapBlock(SliderBlock &a, SliderBlock &b)
{
    int tmpR = a.r;
    int tmpC = a.c;
    a.r = b.r;
    a.c = b.c;
    b.r = tmpR;
    b.c = tmpC;
    std::swap(a, b);
}
