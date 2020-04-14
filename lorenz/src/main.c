#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <SDL2/SDL.h>

#include "gfx.h"

#define WIDTH 320
#define HEIGHT 240

#define nil NULL

static void init_sdl(void)
{
    int result = gfx_initialize(0, 640, 480, 32);
    if (result)
    {
        exit(1);
    }
}

void finalize(void)
{
    gfx_finalize();
    SDL_Quit();
}

static void show_scene(SDL_Surface *surface)
{
    gfx_bitblt(surface, 0, 0);
    gfx_flip();
}

void smooth_scene(SDL_Surface *pixmap) {
    SDL_Surface* tmp = SDL_ConvertSurface(pixmap, pixmap->format, SDL_SWSURFACE);
    Uint8 *src;
    Uint8 *dst;
    int x, y;
    int srcc_offset;

    SDL_FillRect(pixmap, nil, 0x00);
    dst = (Uint8*)pixmap->pixels + 1*pixmap->pitch + 1*pixmap->format->BytesPerPixel;
    src = (Uint8*)tmp->pixels;

    srcc_offset = tmp->pitch-3*tmp->format->BytesPerPixel;

    for (y=1; y<tmp->h; y++) {
        for (x=1; x<tmp->w-1; x++) {
            Uint8 *srcc=src + (x-1)*tmp->format->BytesPerPixel;
            int rr=0, gg=0, bb=0;
            int dx, dy;
            for (dy=-1; dy<=1; dy++) {
                for (dx=-1; dx<=1; dx++) {
                    bb+=*srcc++;
                    gg+=*srcc++;
                    rr+=*srcc++;
                    if (tmp->format->BytesPerPixel==4) {
                        srcc++;
                    }
                }
                srcc+=srcc_offset;
            }
            rr/=9;
            gg/=9;
            bb/=9;
            *dst++ = bb;
            *dst++ = gg;
            *dst++ = rr;
            if (pixmap->format->BitsPerPixel == 32) {
                dst++;
            }
        }
        dst+=2*pixmap->format->BytesPerPixel;
        src+=tmp->pitch;
    }
}

void redraw(SDL_Surface *pixmap) {
    int i = 0; 
    static double x0 = 0.1, y0=0.0, z0=0.0;
    double x1, y1, z1; 
    static double h = 0.01, a = 10.0, b = 18.0, c = 8.0 / 3.0; 
    int N = 1000;

    for (i = 0; i < N; i++) { 
        x1 = x0 + h * a * (y0 - x0); 
        y1 = y0 + h * (x0 * (b - z0) - y0); 
        z1 = z0 + h * (x0 * y0 - c * z0); 
        x0 = x1; 
        y0 = y1; 
        z0 = z1; 
        gfx_putpixel(pixmap, pixmap->w/2 + (int)8.0*x1, pixmap->h/2 + (int)8.0*y1, 255, 255, 255);
    }
    b += 0.1;
    smooth_scene(pixmap);
    show_scene(pixmap);
}

static void main_event_loop(SDL_Surface *pixmap) {
    SDL_Event event;
    int done = 0;

    do {
        /*SDL_WaitEvent(&event);*/
        while (SDL_PollEvent(&event)) {
            switch (event.type) {
                case SDL_QUIT:
                    done = 1;
                    break;
                case SDL_KEYDOWN:
                    switch (event.key.keysym.sym)
                    {
                        case SDLK_ESCAPE:
                        case SDLK_q:
                            done = 1;
                            break;
                        default:
                            break;
                    }
                    break;
                case SDL_KEYUP:
                    switch (event.key.keysym.sym)
                    {
                        default:
                            break;
                    }
                default:
                    break;
            }
        }
        redraw(pixmap);
        SDL_Delay(100);
    } while (!done);
}

void run() {
    SDL_Surface *screen;
    SDL_Surface *pixmap;

    screen = gfx_get_screen_surface();
    pixmap = gfx_create_surface(screen->w, screen->h);

    main_event_loop(pixmap);
}

int main(int argc, char **argv)
{
    init_sdl();
    run();
    finalize();
    return 0;
}
