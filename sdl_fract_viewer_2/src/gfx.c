/*
  SDL Fractal Viewer

   Copyright (C) 2019  Pavel Tisnovsky

SDL Fractal Viewer is free software; you can redistribute it
and/or modify it under the terms of the GNU General Public License as
published by the Free Software Foundation; either version 2, or (at your
option) any later version.

SDL Fractal Viewer is distributed in the hope that it will be
useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License along
with SDL Fractal Viewer; see the file COPYING.  If not, write
to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
Boston, MA 02110-1301 USA.

Linking this library statically or dynamically with other modules is
making a combined work based on this library.  Thus, the terms and
conditions of the GNU General Public License cover the whole
combination.

As a special exception, the copyright holders of this library give you
permission to link this library with independent modules to produce an
executable, regardless of the license terms of these independent
modules, and to copy and distribute the resulting executable under
terms of your choice, provided that you also meet, for each linked
independent module, the terms and conditions of the license of that
module.  An independent module is a module which is not derived from
or based on this library.  If you modify this library, you may extend
this exception to your version of the library, but you are not
obligated to do so.  If you do not wish to do so, delete this
exception statement from your version.
*/

#include <math.h>

#include <SDL2/SDL.h>

#include "gfx.h"

#define ABS(a) ((a)<0 ? -(a) : (a) )
#define MAX(a,b) ((a)>(b) ? (a) : (b))
#define MIN(a,b) ((a)<(b) ? (a) : (b))

static SDL_Surface *screen_surface = NULL;
static SDL_Surface *bitmap_font_surface = NULL;
static SDL_Window *window = NULL;

/*
TTF_Font *font24pt = NULL;
TTF_Font *font36pt = NULL;
TTF_Font *font48pt = NULL;
*/

/*
 *
 */
int gfx_initialize(int fullscreen, int width, int height, int bpp)
{
    window = NULL;
    if (SDL_Init(SDL_INIT_VIDEO) < 0) {
        fprintf(stderr, "Error initializing SDL: %s\n", SDL_GetError());
        return 1;
    } else {
        puts("SDL_Init ok");
    }

    window = SDL_CreateWindow( "Example", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, width, height, SDL_WINDOW_SHOWN );
    if (!window) {
        puts("Error creating window");
        puts(SDL_GetError());
        return 1;
    } else {
        puts("SDL_CreateWindow ok");
    }

    screen_surface = SDL_GetWindowSurface(window);

    if (!screen_surface) {
        fprintf(stderr, "Error setting video mode: %s\n", SDL_GetError());
        return 1;
    } else {
        puts("SDL_GetWindowSurface ok");
    }
    /*
    if (TTF_Init() < 0)
    {
        gfx_finalize();
        fprintf(stderr, "Error initializing TTF moduler");
        return 1;
    }*/
    /*
    font24pt = TTF_OpenFont("data/handwritten.ttf", 24);
    font36pt = TTF_OpenFont("data/handwritten.ttf", 36);
    font48pt = TTF_OpenFont("data/handwritten.ttf", 48);
    */
    return 0;
}

/*
 *
 */
void gfx_finalize(void)
{
    SDL_FreeSurface(screen_surface);
    SDL_DestroyWindow(window);
}

/*
 *
 */
void gfx_set_screen_surface(SDL_Surface *screen)
{
    screen_surface = screen;
}

/*
 *
 */
SDL_Surface* gfx_get_screen_surface(void)
{
    return screen_surface;
}

/*
 *
 */
SDL_Surface* gfx_create_surface(int width, int height)
{
    return SDL_CreateRGBSurface(SDL_SWSURFACE, width, height, 32, 0x00ff0000, 0x0000ff00, 0x000000ff, 0x00000000);
}

/*
 *
 */
void gfx_bitblt(SDL_Surface *surface, const int x, const int y)
{
    SDL_Rect dst;
    dst.x=x;
    dst.y=y;
    dst.w=0;
    dst.h=0;
    SDL_BlitSurface(surface, NULL, screen_surface, &dst);
}

/*
 *
 */
void gfx_flip()
{
    SDL_UpdateWindowSurface(window);
}

/*
 *
 */
void gfx_clear_screen(Uint32 color)
{
    SDL_FillRect(screen_surface, NULL, color);
}

void gfx_getpixel(SDL_Surface *surface, int x, int y, unsigned char *r, unsigned char *g, unsigned char *b) {
    if (x>=0 && x< surface->w && y>=0 && y < surface->h) {
        if (surface->format->BitsPerPixel == 24) {
            Uint8 *pixel = (Uint8 *)surface->pixels;
            pixel += x*3;
            pixel += y*surface->pitch;
            *b = *pixel++;
            *g = *pixel++;
            *r = *pixel;
        }
        if (surface->format->BitsPerPixel == 32) {
            Uint8 *pixel = (Uint8 *)surface->pixels;
            pixel += x*4;
            pixel += y*surface->pitch;
            *b = *pixel++;
            *g = *pixel++;
            *r = *pixel;
        }
    }
}

/*
 *
 */
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

/*
 *
 */
void gfx_putpixel_screen(int x, int y, unsigned char r, unsigned char g, unsigned char b)
{
    gfx_putpixel(screen_surface, x, y, r, g, b);
}

/*
 *
 */
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

/*
 *
 */
void gfx_vline(SDL_Surface *surface, int x,  int y1, int y2, unsigned char r, unsigned char g, unsigned char b)
{
    int y;
    int fromY = MIN(y1, y2);
    int toY = MAX(y1, y2);
    for (y = fromY; y <= toY; y++)
    {
        gfx_putpixel(surface, x, y, r, g, b);
    }
}

/*
 *
 */
void gfx_line(SDL_Surface *surface, int x1, int y1, int x2, int y2, unsigned char r, unsigned char g, unsigned char b)
{
    int dx = ABS(x2-x1), sx = x1<x2 ? 1 : -1;
    int dy = ABS(y2-y1), sy = y1<y2 ? 1 : -1;
    int err = (dx>dy ? dx : -dy)/2, e2;
    
    while (1){
        gfx_putpixel(surface, x1, y1, r, g, b);
        if (x1 == x2 && y1 == y2)
        {
            break;
        }
        e2 = err;
        if (e2 > -dx)
        {
             err -= dy;
             x1 += sx;
        }
        if (e2 < dy)
        {
            err += dx;
            y1 += sy;
        }
    }
}

/*
 *
 */
void gfx_aa_line(SDL_Surface *surface, int x1, int y1, int x2, int y2, unsigned char r, unsigned char g, unsigned char b)
{
    int dx=x2-x1;
    int dy=y2-y1;
    double s, p, e=255.0;
    int x, y, xdelta, ydelta, xpdelta, ypdelta, xp, yp;
    int i, imin, imax;

    if (x1==x2)
    {
        gfx_vline(surface, x1, y1, y2, r, g, b);
        return;
    }

    if (y1==y2)
    {
        gfx_hline(surface, x1, x2, y1, r, g, b);
        return;
    }

    if (x1>x2)
    {
        x1=x1^x2; x2=x1^x2; x1=x1^x2;
        y1=y1^y2; y2=y1^y2; y1=y1^y2;
    }

    if (ABS(dx)>ABS(dy))
    {
        s=(double)dy/(double)dx;
        imin=x1;  imax=x2;
        x=x1;     y=y1;
        xdelta=1; ydelta=0;
        xpdelta=0;
        xp=0;
        if (y2>y1)
        {
            ypdelta=1;
            yp=1;
        }
        else
        {
            s=-s;
            ypdelta=-1;
            yp=-1;
        }
    }
    else
    {
        s=(double)dx/(double)dy;
        xdelta=0; ydelta=1;
        ypdelta=0;
        yp=0;
        if (y2>y1)
        {
            imin=y1;    imax=y2;
            x=x1;       y=y1;
            xpdelta=1;
            xp=1;
        }
        else
        {
            s=-s;
            imin=y2;    imax=y1;
            x=x2;       y=y2;
            xpdelta=-1;
            xp=-1;
        }
    }
    p=s*256.0;
    for (i=imin; i<=imax; i++) {
        int c1 = (int)e;
        int c2 = 255-c1;
        int r1 = r == 255 ? 255 : c1;
        int r2 = r == 255 ? 255 : c2;
        int g1 = g == 255 ? 255 : c1;
        int g2 = g == 255 ? 255 : c2;
        int b1 = b == 255 ? 255 : c1;
        int b2 = b == 255 ? 255 : c2;
        gfx_putpixel(surface, x+xp, y+yp, r1, g1, b1);
        gfx_putpixel(surface, x, y, r2, g2, b2);
        e=e-p;
        x+=xdelta;
        y+=ydelta;
        if (e<0.0) {
            e+=256.0;
            x+=xpdelta;
            y+=ypdelta;
        }
    }
}

/*
 *
 */
void gfx_hline_screen(int x1, int x2, int y, unsigned char r, unsigned char g, unsigned char b)
{
    gfx_hline(screen_surface, x1, x2, y, r, g, b);
}

/*
 *
 */
void gfx_vline_screen(int x, int y1, int y2, unsigned char r, unsigned char g, unsigned char b)
{
    gfx_vline(screen_surface, x, y1, y2, r, g, b);
}

/*
 *
 */
void gfx_line_screen(int x1, int y1, int x2, int y2, unsigned char r, unsigned char g, unsigned char b)
{
    gfx_line(screen_surface, x1, y1, x2, y2, r, g, b);
}

/*
 *
 */
void gfx_aa_line_screen(int x1, int y1, int x2, int y2, unsigned char r, unsigned char g, unsigned char b)
{
    gfx_aa_line(screen_surface, x1, y1, x2, y2, r, g, b);
}

/*
 *
 */
void gfx_set_bitmap_font_surface(SDL_Surface *surface)
{
    bitmap_font_surface = surface;
}

/*
 *
 */
void gfx_print_char_bitmap_font(SDL_Surface *surface, int x, int y, char ch)
{
    SDL_Rect src_rect;
    SDL_Rect dst_rect;
    ch-=32;
    if (ch <= 0)
    {
        return;
    }
    dst_rect.x = x;
    dst_rect.y = y;
    src_rect.x = 0;
    src_rect.y = BITMAP_FONT_CHARACTER_HEIGHT * ch;
    src_rect.w = BITMAP_FONT_CHARACTER_WIDTH;
    src_rect.h = BITMAP_FONT_CHARACTER_HEIGHT;
    SDL_BlitSurface(bitmap_font_surface, &src_rect, surface, &dst_rect);
}

/*
 *
 */
void gfx_print_string_bitmap_font(SDL_Surface *surface, int x, int y, char *str)
{
    char *p;
    for (p = str; *p; p++)
    {
        gfx_print_char_bitmap_font(surface, x, y, *p);
        x += BITMAP_FONT_CHARACTER_WIDTH;
    }
}

/*
 *
 */
void gfx_print_string_bitmap_font_screen(int x, int y, char *str)
{
    gfx_print_string_bitmap_font(screen_surface, x, y, str);
}

/*
 *
 */
/*
void gfx_print_string_ttf(SDL_Surface *surface, TTF_Font *font, int x, int y, char *str)
{
    SDL_Rect dst_rect;
    SDL_Color color;
    SDL_Surface *font_surface;
    dst_rect.x = x;
    dst_rect.y = y;
    color.r = 0x00;
    color.g = 0x00;
    color.b = 0x00;
    font_surface = TTF_RenderText_Blended(font, str, color);
    SDL_BlitSurface(font_surface, NULL, surface, &dst_rect);
    SDL_FreeSurface(font_surface);
}*/

/*
 *
 */
/*
void gfx_print_string_ttf_screen(TTF_Font *font, int x, int y, char *str){
    gfx_print_string_ttf(screen_surface, font, x, y, str);
}*/

