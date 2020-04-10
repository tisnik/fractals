#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <SDL/SDL.h>

#include "gfx.h"

#define WIDTH 320
#define HEIGHT 240

#define nil NULL

SDL_Surface *pixmap;

double xpos = 0.0;
/*double xpos = -0.75;*/
double ypos = 0.0;
double scale = 240.0;
double  uhel = 45.0;

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

static void show_fractal(SDL_Surface *surface)
{
    gfx_bitblt(surface, 0, 0);
    gfx_flip();
}

void calcCorner(double xpos, double ypos, double scale,
                double *xmin,  double *ymin,  double *xmax, double *ymax)
{
    *xmin=xpos-WIDTH/scale;
    *ymin=ypos-HEIGHT/scale;
    *xmax=xpos+WIDTH/scale;
    *ymax=ypos+HEIGHT/scale;
}

void draw_grid(SDL_Surface *surface)
{
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

void draw_fractal_(SDL_Surface *surface)
{
    int x, y;
    Uint8 *pixel = nil;
    double cx, cy;
    double xmin, ymin, xmax, ymax;

    calcCorner(xpos, ypos, scale, &xmin, &ymin, &xmax, &ymax);
    cy = ymin;
    for (y=0; y<240; y++)
    {
        cx = xmin;
        pixel = (Uint8 *)surface->pixels + (y + 128) * surface->pitch + 160*4;
        for (x=0; x<320; x++)
        {
            double zx = 0.0;
            double zy = 0.0;
            unsigned int i = 0;
            while (i < 150) {
                double zx2 = zx * zx;
                double zy2 = zy * zy;
                zx = -fabs(zx);
                if (zx2 + zy2 > 4.0) {
                    break;
                }
                zy = 2.0 * zx * zy + cy;
                zx = zx2 - zy2 + cx;
                i++;
            }
            {
                int r = i*2;
                int g = i*3;
                int b = i*5;

                *pixel++ = r;
                *pixel++ = g;
                *pixel++ = b;
                pixel++;
            }
            cx += (xmax-xmin)/WIDTH;
        }
        cy += (ymax-ymin)/HEIGHT;
    }
}

void draw_fractal_julia(SDL_Surface *surface)
{
    int x, y;
    Uint8 *pixel = nil;
    double cx, cy;
    double xmin, ymin, xmax, ymax;
    double ccx, ccy;

    calcCorner(xpos, ypos, scale, &xmin, &ymin, &xmax, &ymax);
    /*
    ccx = 0.0;
    ccy = 1.0;
    */
    ccx = 0.285;
    ccy = 0.01;
    cy = ymin;
    for (y=0; y<240; y++)
    {
        cx = xmin;
        pixel = (Uint8 *)surface->pixels + (y + 128) * surface->pitch + 160*4;
        for (x=0; x<320; x++)
        {
            double zx = cx;
            double zy = cy;
            unsigned int i = 0;
            while (i < 255) {
                double zx2 = zx * zx;
                double zy2 = zy * zy;
                /*zx = -fabs(zx);*/
                if (zx2 + zy2 > 4.0) {
                    break;
                }
                zy = 2.0 * zx * zy + ccy;
                zx = zx2 - zy2 + ccx;
                i++;
            }
            {
                int r = i*2;
                int g = i*3;
                int b = i*5;

                *pixel++ = r;
                *pixel++ = g;
                *pixel++ = b;
                pixel++;
            }
            cx += (xmax-xmin)/WIDTH;
        }
        cy += (ymax-ymin)/HEIGHT;
    }
}

void draw_fractal_julia_mandelbrot(SDL_Surface *surface)
{
    int x, y;
    Uint8 *pixel = nil;
    double cx, cy;
    double xmin, ymin, xmax, ymax;
    double ccx, ccy;

    calcCorner(xpos, ypos, scale, &xmin, &ymin, &xmax, &ymax);
    ccx = 0.285;
    ccy = 0.01;
    ccx = -0.7269;
    ccy = 0.1889;
    ccx = -1.0;
    ccy = 0.0;
    cy = ymin;
    for (y=0; y<240; y++)
    {
        cx = xmin;
        pixel = (Uint8 *)surface->pixels + (y + 128) * surface->pitch + 160*4;
        for (x=0; x<320; x++)
        {
            double zx = cx;
            double zy = cy;
            unsigned int i = 0;
            while (i < 255) {
                double zx2, zy2;

                zx2 = zx * zx;
                zy2 = zy * zy;
                if (zx2 + zy2 > 4.0) {
                    break;
                }
                zy = 2.0 * zx * zy + ccy;
                zx = zx2 - zy2 + ccx;
                i++;

                zx2 = zx * zx;
                zy2 = zy * zy;
                if (zx2 + zy2 > 4.0) {
                    break;
                }
                zy = 2.0 * zx * zy + cy;
                zx = zx2 - zy2 + cx;
                i++;
            }
            {
                int r = i*2;
                int g = i*3;
                int b = i*5;

                *pixel++ = r;
                *pixel++ = g;
                *pixel++ = b;
                pixel++;
            }
            cx += (xmax-xmin)/WIDTH;
        }
        cy += (ymax-ymin)/HEIGHT;
    }
}

void draw_multifractal_mandel_julia(SDL_Surface *surface)
{
    int x, y;
    Uint8 *pixel = nil;
    double cx, cy;
    double xmin, ymin, xmax, ymax;
    double ccx, ccy;

    calcCorner(xpos, ypos, scale, &xmin, &ymin, &xmax, &ymax);
    /*
    ccx = 0.0;
    ccy = 1.0;
    */
    ccx = 0.285;
    ccy = 0.01;
    ccx=-1.5;
    ccy=0.0;
    cy = ymin;
    for (y=0; y<240; y++)
    {
        cx = xmin;
        pixel = (Uint8 *)surface->pixels + (y + 128) * surface->pitch + 160*4;
        for (x=0; x<320; x++)
        {
            double zx = 0.0;
            double zy = 0.0;
            unsigned int i = 0;
            while (i < 255) {
                double zx2 = zx * zx;
                double zy2 = zy * zy;
                if (zx2 + zy2 > 4.0) {
                    break;
                }
                /*if (i%2==0) {*/
                if (i>50 /*&& i<30*/) {
                    zy = 2.0 * zx * zy + ccy;
                    zx = zx2 - zy2 + ccx;
                } else {
                    zy = 2.0 * zx * zy + cy;
                    zx = zx2 - zy2 + cx;
                }
                i++;
            }
            {
                int r = i*2;
                int g = i*3;
                int b = i*5;

                *pixel++ = r;
                *pixel++ = g;
                *pixel++ = b;
                pixel++;
            }
            cx += (xmax-xmin)/WIDTH;
        }
        cy += (ymax-ymin)/HEIGHT;
    }
}

void draw_mandeljulia(SDL_Surface *surface)
{
    double  zx,zy,zx2,zy2,cx,cy;
    double  cosu,sinu,ccxc,ccyc;
    int     x,y,i;
    Uint8 *pixel = nil;

    double ccx = 0.0;
    double ccy = 1.0;

    double xmin, ymin, xmax, ymax;
    double u;

    calcCorner(xpos, ypos, scale, &xmin, &ymin, &xmax, &ymax);

    u=uhel*3.1415/180.0;
    cosu=cos(u);
    sinu=sin(u);
    ccxc=ccx*cosu;
    ccyc=ccy*cosu;

    cy = ymin;

    for (y=0;y<240;y++) {
        cx=xmin;
        pixel = (Uint8 *)surface->pixels + (y + 128) * surface->pitch + 160*4;
        for (x=0;x<320;x++) {
            i=0;
            zx=cx*cosu;
            zy=cy*cosu;
            do {
                zx2=zx*zx;
                zy2=zy*zy;
                zy=2.0*zx*zy+ccyc+cy*sinu;
                zx=zx2-zy2+ccxc+cx*sinu;
                i++;
            } while (i<64 && zx2+zy2<4.0);
            {
                int r = i*2;
                int g = i*3;
                int b = i*5;

                *pixel++ = r;
                *pixel++ = g;
                *pixel++ = b;
                pixel++;
            }
            cx += (xmax-xmin)/WIDTH;
        }
        cy += (ymax-ymin)/HEIGHT;
    }
}

void draw_multifractal(SDL_Surface *surface)
{
    int x, y;
    Uint8 *pixel = nil;
    double cx, cy;
    double xmin, ymin, xmax, ymax;
    double ccx1, ccy1;
    double ccx2, ccy2;

    calcCorner(xpos, ypos, scale, &xmin, &ymin, &xmax, &ymax);
    ccx1 = 0.0;
    ccy1 = 1.0;
    ccx2 = -1.5;
    ccy2 = 0.0;
    cy = ymin;
    for (y=0; y<240; y++)
    {
        cx = xmin;
        pixel = (Uint8 *)surface->pixels + (y + 128) * surface->pitch + 160*4;
        for (x=0; x<320; x++)
        {
            double zx = cx;
            double zy = cy;
            unsigned int i = 0;
            while (i < 255) {
                double zx2 = zx * zx;
                double zy2 = zy * zy;
                if (zx2 + zy2 > 4.0) {
                    break;
                }
                if (i>20) {
                    zy = 2.0 * zx * zy + ccy1;
                    zx = zx2 - zy2 + ccx1;
                } else {
                    zy = 2.0 * zx * zy + ccy2;
                    zx = zx2 - zy2 + ccx2;
                }
                i++;
            }
            {
                int r = i*2;
                int g = i*3;
                int b = i*5;

                *pixel++ = r;
                *pixel++ = g;
                *pixel++ = b;
                pixel++;
            }
            cx += (xmax-xmin)/WIDTH;
        }
        cy += (ymax-ymin)/HEIGHT;
    }
}

void draw_fractal(SDL_Surface *surface)
{
    int x, y;
    Uint8 *pixel = nil;
    double cx, cy;
    double xmin, ymin, xmax, ymax;
    /* not used for Mandelbrot fractal types
    double ccx, ccy;
    */
    double ccx1, ccx2, ccy1, ccy2;

    calcCorner(xpos, ypos, scale, &xmin, &ymin, &xmax, &ymax);
    /* not used for Mandelbrot fractal types
    ccx = -0.7269;
    ccy = 0.1889;
    */
    ccx1 = 0.0;
    ccy1 = 1.0;
    ccx2 = 0.285;
    ccy2 = 0.01;
    cy = ymin;
    for (y=0; y<240; y++)
    {
        cx = xmin;
        pixel = (Uint8 *)surface->pixels + (y + 128) * surface->pitch + 160*4;
        for (x=0; x<320; x++)
        {
            double zx = cx;
            double zy = cy;
            unsigned int i = 0;
            while (i < 255) {
                double zx2, zy2;

                zx2 = zx * zx;
                zy2 = zy * zy;
                if (zx2 + zy2 > 4.0) {
                    break;
                }
                zy = 2.0 * zx * zy + ccy1;
                zx = zx2 - zy2 + ccx1;
                i++;

                zx2 = zx * zx;
                zy2 = zy * zy;
                if (zx2 + zy2 > 4.0) {
                    break;
                }
                zy = 2.0 * zx * zy + ccy2;
                zx = zx2 - zy2 + ccx2;
                i++;
            }
            {
                int r = i*2;
                int g = i*3;
                int b = i*5;

                *pixel++ = r;
                *pixel++ = g;
                *pixel++ = b;
                pixel++;
            }
            cx += (xmax-xmin)/WIDTH;
        }
        cy += (ymax-ymin)/HEIGHT;
    }
}

void redraw(SDL_Surface *pixmap)
{
    draw_grid(pixmap);
    /*draw_multifractal(pixmap);*/
    draw_mandeljulia(pixmap);
    show_fractal(pixmap);
}

static void main_event_loop(void)
{
    SDL_Event event;
    int done = 0;
    int left = 0, right = 0, up = 0, down = 0;
    int zoomin = 0, zoomout = 0;
    int perform_redraw;
    int angle_1 = 0, angle_2 = 0;

    do
    {
        /*SDL_WaitEvent(&event);*/
        while (SDL_PollEvent(&event))
        {
            switch (event.type)
            {
                case SDL_QUIT:
                    done = 1;
                    break;
                case SDL_KEYDOWN:
                    /* TODO - control: more speed */
                    /* TODO - shift: lower speed */
                    switch (event.key.keysym.sym)
                    {
                        case SDLK_ESCAPE:
                        case SDLK_q:
                            done = 1;
                            break;
                        case SDLK_LEFT:
                            left = 1;
                            break;
                        case SDLK_RIGHT:
                            right = 1;
                            break;
                        case SDLK_UP:
                            up = 1;
                            break;
                        case SDLK_DOWN:
                            down = 1;
                            break;
                        case SDLK_PAGEDOWN:
                            zoomin = 1;
                            break;
                        case SDLK_PAGEUP:
                            zoomout = 1;
                            break;
                        case SDLK_z:
                            angle_1 = 1;
                            break;
                        case SDLK_x:
                            angle_2 = 1;
                            break;
                        default:
                            break;
                    }
                    break;
                case SDL_KEYUP:
                    switch (event.key.keysym.sym)
                    {
                        case SDLK_LEFT:
                            left = 0;
                            break;
                        case SDLK_RIGHT:
                            right = 0;
                            break;
                        case SDLK_UP:
                            up = 0;
                            break;
                        case SDLK_DOWN:
                            down = 0;
                            break;
                        case SDLK_PAGEDOWN:
                            zoomin = 0;
                            break;
                        case SDLK_PAGEUP:
                            zoomout = 0;
                            break;
                        case SDLK_z:
                            angle_1 = 0;
                            break;
                        case SDLK_x:
                            angle_2 = 0;
                            break;
                        default:
                            break;
                    }
                default:
                    break;
            }
        }
        perform_redraw = 0;
        if (left) {
            xpos -= 10.0/scale;
            perform_redraw=1;
        }
        if (right) {
            xpos += 10.0/scale;
            perform_redraw=1;
        }
        if (up) {
            ypos -= 10.0/scale;
            perform_redraw=1;
        }
        if (down) {
            ypos += 10.0/scale;
            perform_redraw=1;
        }
        if (zoomin) {
            scale *= 0.9;
            perform_redraw=1;
        }
        if (zoomout) {
            scale *= 1.1;
            perform_redraw=1;
        }
        if (angle_1) {
            uhel--;
            perform_redraw=1;
        }
        if (angle_2) {
            uhel++;
            perform_redraw=1;
        }
        if (perform_redraw) {
            redraw(pixmap);
        }
    } while (!done);
}

int main(int argc, char **argv)
{
    /*SDL_Surface *font;*/
    SDL_Surface *screen;

    init_sdl();

    screen = gfx_get_screen_surface();
    pixmap = gfx_create_surface(screen->w, screen->h);

    draw_grid(pixmap);
    /*draw_multifractal(pixmap);*/
    draw_mandeljulia(pixmap);
    show_fractal(pixmap);
    main_event_loop();
    finalize();
    return 0;
}
