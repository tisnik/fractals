#ifndef _GFX_H_
#define _GFX_H_

#include <SDL2/SDL.h>

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
void gfx_getpixel(SDL_Surface *surface, int x, int y, unsigned char *r, unsigned char *g, unsigned char *b);

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

