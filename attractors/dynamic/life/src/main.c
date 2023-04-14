#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <SDL2/SDL.h>

#include "smooth.c"

#include "gfx.h"

#define WIDTH 640
#define HEIGHT 480

#define BORDER 50

#define RED    0
#define GREEN  1
#define YELLOW 2
#define BLUE   3

#define MAX_RED    5000
#define MAX_GREEN  50
#define MAX_BLUE   50
#define MAX_YELLOW 10

#define MAX_DISTANCE 2000

#define SMOOTH

static void init_sdl(void)
{
    int result = gfx_initialize(0, WIDTH, HEIGHT, 32);
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

const int factor = 2;

typedef struct {
    float x;
    float y;
    float vx;
    float vy;
    int   type;
} Point;

typedef struct Color {
    unsigned char r;
    unsigned char g;
    unsigned char b;
} Color;

typedef struct {
    Point *points;
    int    max;
    Color  colors[4];
} Atoms;

typedef struct {
    float rules[4][4];
    Atoms atoms;
} State;

void initRules(State *state) {
    int i, j;

    for (j=0; j<4; j++) {
        for (i=0; i<4; i++) {
            state->rules[i][j] = 2.0*(float)rand()/RAND_MAX-1.0;
        }
    }
}

float randomX() {
    return (WIDTH-BORDER*2)*(float)rand()/RAND_MAX+BORDER;
}

float randomY() {
    return (HEIGHT-BORDER*2)*(float)rand()/RAND_MAX+BORDER;
}

void createPoints(int max, Point *points, int type) {
    int i;
    for (i=0; i<max; i++) {
        points[i].x = randomX();
        points[i].y = randomY();
        points[i].vx = 0.0;
        points[i].vy = 0.0;
        points[i].type = type;
    }
}

void redraw(SDL_Surface *pixmap, State *state) {
    int i;

    Atoms atoms = state->atoms;

    SDL_FillRect(pixmap, NULL, 0x00);
    for (i=0; i<atoms.max; i++) {
        Point point = atoms.points[i];
        Color color = atoms.colors[point.type];
        gfx_putpixel(pixmap, point.x, point.y, color.r, color.g, color.b);
        gfx_putpixel(pixmap, point.x-1, point.y, color.r, color.g, color.b);
        gfx_putpixel(pixmap, point.x+1, point.y, color.r, color.g, color.b);
        gfx_putpixel(pixmap, point.x, point.y-1, color.r, color.g, color.b);
        gfx_putpixel(pixmap, point.x, point.y+1, color.r, color.g, color.b);
    }

#ifdef SMOOTH
    smooth_scene(pixmap);
#endif
    show_scene(pixmap);
}

void applyRules(State *state) {
    int i, j;

    for (i=0; i<state->atoms.max; i++) {
        float fx = 0.0;
        float fy = 0.0;
        Point *a = &state->atoms.points[i];
        for (j=0; j<state->atoms.max; j++) {
            if (i != j) {
                Point *b = &state->atoms.points[j];
                float g = state->rules[a->type][b->type];   /* *factor */
                float dx = a->x - b->x;
                float dy = a->y - b->y;
                if (dx != 0.0 || dy != 0.0) {
                    float d = dx*dx + dy*dy;
                    if (d < MAX_DISTANCE) {
                        float f = g/sqrt(d);
                        fx += f*dx;
                        fy += f*dy;
                    }
                }
            }
        }

        a->vx = (a->vx + fx) * 0.5;
        a->vy = (a->vy + fy) * 0.5;
        a->x += a->vx;
        a->y += a->vy;

        if (a->x <=0) {
            a->vx = -a->vx;
            a->x = 0;
        }
        if (a->x > WIDTH) {
            a->vx = -a->vx;
            a->x = WIDTH-1;
        }
        if (a->y <=0) {
            a->vy = -a->vy;
            a->y = 0;
        }
        if (a->y > HEIGHT) {
            a->vy = -a->vy;
            a->y = HEIGHT-1;
        }
    }
}

static void main_event_loop(SDL_Surface *pixmap) {
    SDL_Event event;
    int done = 0;

    int maxPoints = MAX_RED+MAX_GREEN+MAX_BLUE+MAX_YELLOW;

    Color redColor = {255, 80, 80};
    Color greenColor = {80, 255, 80};
    Color blueColor = {80, 80, 255};
    Color yellowColor = {255, 255, 80};

    State state;

    initRules(&state);
    state.atoms.colors[RED] = redColor;
    state.atoms.colors[GREEN] = greenColor;
    state.atoms.colors[BLUE] = blueColor;
    state.atoms.colors[YELLOW] = yellowColor;

    state.atoms.points = (Point*)malloc(maxPoints*sizeof(Point));
    state.atoms.max = maxPoints;

    createPoints(MAX_RED, state.atoms.points, RED);
    createPoints(MAX_GREEN, state.atoms.points+MAX_RED, GREEN);
    createPoints(MAX_BLUE, state.atoms.points+MAX_RED+MAX_GREEN, BLUE);
    createPoints(MAX_YELLOW, state.atoms.points+MAX_RED+MAX_GREEN+MAX_BLUE, YELLOW);

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
        applyRules(&state);
        redraw(pixmap, &state);
        SDL_Delay(10);
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
