/*
  SDL Fractal Viewer.

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

#ifndef _GFX_H_
#define _GFX_H_

#include <SDL/SDL.h>

#define BITMAP_FONT_CHARACTER_WIDTH 8
#define BITMAP_FONT_CHARACTER_HEIGHT 16

/*
extern TTF_Font *font24pt;
extern TTF_Font *font36pt;
extern TTF_Font *font48pt;
*/

int  gfx_initialize(int fullscreen, int width, int height, int bpp);
void gfx_finalize(void);
void gfx_set_screen_surface(SDL_Surface *screen);
SDL_Surface* gfx_get_screen_surface(void);
SDL_Surface* gfx_create_surface(int width, int height);

void gfx_bitblt(SDL_Surface *surface, const int x, const int y);
void gfx_flip(void);
void gfx_clear_screen(Uint32 color);

void gfx_putpixel(SDL_Surface *surface, int x, int y, unsigned char r, unsigned char g, unsigned char b);
void gfx_putpixel_screen(int x, int y, unsigned char r, unsigned char g, unsigned char b);

void gfx_hline(SDL_Surface *surface, int x1, int x2, int y, unsigned char r, unsigned char g, unsigned char b);
void gfx_vline(SDL_Surface *surface, int x,  int y1, int y2, unsigned char r, unsigned char g, unsigned char b);
void gfx_line (SDL_Surface *surface, int x1, int y1, int x2, int y2, unsigned char r, unsigned char g, unsigned char b);
void gfx_aa_line(SDL_Surface *surface, int x1, int y1, int x2, int y2, unsigned char r, unsigned char g, unsigned char b);
void gfx_hline_screen(int x1, int x2, int y, unsigned char r, unsigned char g, unsigned char b);
void gfx_vline_screen(int x,  int y1, int y2, unsigned char r, unsigned char g, unsigned char b);
void gfx_line_screen (int x1, int y1, int x2, int y2, unsigned char r, unsigned char g, unsigned char b);
void gfx_aa_line_screen (int x1, int y1, int x2, int y2, unsigned char r, unsigned char g, unsigned char b);

void gfx_set_bitmap_font_surface(SDL_Surface *surface);
void gfx_print_char_bitmap_font(SDL_Surface *surface, int x, int y, char ch);
void gfx_print_string_bitmap_font(SDL_Surface *surface, int x, int y, char *str);
void gfx_print_string_bitmap_font_screen(int x, int y, char *str);

/*
void gfx_print_string_ttf(SDL_Surface *surface, TTF_Font *font, int x, int y, char *str);
void gfx_print_string_ttf_screen(TTF_Font *font, int x, int y, char *str);
*/

#endif

