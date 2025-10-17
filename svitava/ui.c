#include <SDL2/SDL.h>

/* graphics options */
#define SCREEN_WIDTH 800
#define SCREEN_HEIGHT 600
#define IMAGE_WIDTH 256
#define IMAGE_HEIGHT 256
#define TITLE "Svitava"

#define ABS(a) ((a)<0 ? -(a) : (a) )
#define MAX(a,b) ((a)>(b) ? (a) : (b))
#define MIN(a,b) ((a)<(b) ? (a) : (b))

#include "font.h"

typedef struct GraphicsState {
    SDL_Window *window;
    SDL_Surface *screen_surface;
    SDL_Surface *mandelbrot_pixmap;
    SDL_Surface *julia_pixmap;
} GraphicsState;

static void init_sdl(GraphicsState *graphicsState, const char *title,
                     const int width, const int height) {
    graphicsState->window = NULL;
    graphicsState->screen_surface = NULL;

    if (SDL_Init(SDL_INIT_VIDEO) < 0) {
        fprintf(stderr, "Error initializing SDL: %s\n", SDL_GetError());
        exit(1);
    } else {
        puts("SDL_Init ok");
    }

    graphicsState->window = SDL_CreateWindow(TITLE, SDL_WINDOWPOS_UNDEFINED,
                                             SDL_WINDOWPOS_UNDEFINED, width,
                                             height, SDL_WINDOW_SHOWN);

    if (!graphicsState->window) {
        puts("Error creating window");
        puts(SDL_GetError());
        exit(1);
    } else {
        puts("SDL_CreateWindow ok");
    }

    graphicsState->screen_surface = SDL_GetWindowSurface(graphicsState->window);

    if (!graphicsState->screen_surface) {
        fprintf(stderr, "Error setting video mode: %s\n", SDL_GetError());
        exit(1);
    } else {
        puts("SDL_GetWindowSurface ok");
    }
}

static void finalize(GraphicsState *graphicsState) {
    if (graphicsState->mandelbrot_pixmap != NULL) {
        printf("Freeing pixmap (%p)\n", (void*)graphicsState->mandelbrot_pixmap);
        free(graphicsState->mandelbrot_pixmap);
    }
    if (graphicsState->julia_pixmap != NULL) {
        printf("Freeing pixmap (%p)\n", (void*)graphicsState->julia_pixmap);
        free(graphicsState->julia_pixmap);
    }

    SDL_FreeSurface(graphicsState->screen_surface);
    SDL_DestroyWindow(graphicsState->window);
    SDL_Quit();
}

static SDL_Surface *create_pixmap(const int width, const int height) {
    SDL_Surface *pixmap;
    pixmap = SDL_CreateRGBSurface(SDL_SWSURFACE, width, height, 32, 0x00ff0000,
                                  0x0000ff00, 0x000000ff, 0x00000000);
    if (!pixmap) {
        puts("Can not create pixmap");
        exit(1);
    } else {
        printf("Off screen pixmap created (%p)\n", (void*)pixmap);
    }
    return pixmap;
}

static void create_pixmaps(GraphicsState *graphicsState, const int width, const int height) {
    graphicsState->mandelbrot_pixmap=create_pixmap(width, height);
    graphicsState->julia_pixmap=create_pixmap(width, height);
}

void redraw(GraphicsState *graphicsState) {
    SDL_UpdateWindowSurface(graphicsState->window);
}

void gfx_putpixel(SDL_Surface *surface, int x, int y, unsigned char r, unsigned char g, unsigned char b)
{
    if (x>=0 && x< surface->w && y>=0 && y < surface->h)
    {
        if (surface->format->BitsPerPixel == 24)
        {
            Uint8 *pixel = (Uint8 *)surface->pixels;
            pixel += x*3;
            pixel += y*surface->pitch;
            *pixel++ = b;
            *pixel++ = g;
            *pixel   = r;
        }
        if (surface->format->BitsPerPixel == 32)
        {
            Uint8 *pixel = (Uint8 *)surface->pixels;
            pixel += x*4;
            pixel += y*surface->pitch;
            *pixel++ = b;
            *pixel++ = g;
            *pixel   = r;
        }
    }
}

void gfx_hline(SDL_Surface *surface, int x1, int x2, int y, unsigned char r, unsigned char g, unsigned char b)
{
    int x;
    int fromX = MIN(x1, x2);
    int toX = MAX(x1, x2);
    for (x = fromX; x <= toX; x++)
    {
        gfx_putpixel(surface, x, y, r, g, b);
    }
}

void gfx_vline(SDL_Surface *surface, int x, int y1, int y2, unsigned char r, unsigned char g, unsigned char b)
{
    int y;
    int fromY = MIN(y1, y2);
    int toY = MAX(y1, y2);
    for (y = fromY; y <= toY; y++)
    {
        gfx_putpixel(surface, x, y, r, g, b);
    }
}

void gfx_draw_char(SDL_Surface *surface, int x, int y, unsigned char r, unsigned char g, unsigned char b, char c)
{
    unsigned char *ptr = font + (c-' ')*16;
    int xx, yy;
    for (yy=0; yy<16; yy++) {
        unsigned char code = *ptr++;
        for (xx=0; xx<8; xx++) {
            if (code & 0x81) {
                gfx_putpixel(surface, x+xx, y+yy, r, g, b);
            }
            code <<= 1;
        }
    }
}

void draw_grid(GraphicsState *graphicsState) {
    SDL_Surface *surface = graphicsState->screen_surface;
    int width = surface->w;
    int height = surface->h;
    int x, y;
    SDL_FillRect(surface, NULL, 0xffffffff);

    for (x=0; x<width; x+=20)
    {
        gfx_vline(surface, x, 0, height-1, 191, 191, 255);
    }
    for (y=0; y<height; y+=20)
    {
        gfx_hline(surface, 0, width-1, y, 191, 191, 255);
    }
}

static void main_event_loop(GraphicsState *graphicsState) {
    SDL_Event event;
    int done = 0;

    do {
        while (SDL_PollEvent(&event)) {
            switch (event.type) {
            case SDL_QUIT:
                done = 1;
                break;
            case SDL_KEYDOWN:
                switch (event.key.keysym.sym) {
                case SDLK_ESCAPE:
                case SDLK_q:
                    done = 1;
                    break;
                default:
                    break;
                }
                break;
            default:
                break;
            }
        }
        redraw(graphicsState);
        SDL_Delay(10);
    } while (!done);
}

int main(int argc, char **argv) {
    GraphicsState graphicsState;

    init_sdl(&graphicsState, TITLE, SCREEN_WIDTH, SCREEN_HEIGHT);
    create_pixmaps(&graphicsState, IMAGE_WIDTH, IMAGE_HEIGHT);

    draw_grid(&graphicsState);
    main_event_loop(&graphicsState);

    finalize(&graphicsState);

    return 0;
}
