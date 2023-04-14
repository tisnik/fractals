#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <SDL2/SDL.h>

/* graphics options */
#define WIDTH 640
#define HEIGHT 480
#define TITLE "Life simulator"

/* constants used by model */
#define RED    0
#define GREEN  1
#define YELLOW 2
#define BLUE   3

/* model options */
#define BORDER 50

#define MAX_RED    5000
#define MAX_GREEN  500
#define MAX_BLUE   50
#define MAX_YELLOW 10

#define MAX_DISTANCE 2000

#define DAMPING_FACTOR 0.5

#define SCALE_FACTOR 1

/* enable scene smoothing */
#define _SMOOTH

typedef struct State {
    SDL_Window *window;
    SDL_Surface *screen_surface;
} State;

static void init_sdl(State * state, const int width, const int height)
{
    state->window = NULL;
    state->screen_surface = NULL;

    if (SDL_Init(SDL_INIT_VIDEO) < 0) {
        fprintf(stderr, "Error initializing SDL: %s\n", SDL_GetError());
        exit(1);
    } else {
        puts("SDL_Init ok");
    }

    state->window =
        SDL_CreateWindow(TITLE, SDL_WINDOWPOS_UNDEFINED,
                         SDL_WINDOWPOS_UNDEFINED, width, height,
                         SDL_WINDOW_SHOWN);

    if (!state->window) {
        puts("Error creating window");
        puts(SDL_GetError());
        exit(1);
    } else {
        puts("SDL_CreateWindow ok");
    }

    state->screen_surface = SDL_GetWindowSurface(state->window);

    if (!state->screen_surface) {
        fprintf(stderr, "Error setting video mode: %s\n", SDL_GetError());
        exit(1);
    } else {
        puts("SDL_GetWindowSurface ok");
    }
}

static void finalize(State * state, SDL_Surface * pixmap)
{
    SDL_FreeSurface(pixmap);
    SDL_FreeSurface(state->screen_surface);
    SDL_DestroyWindow(state->window);
    SDL_Quit();
}

static void show_pixmap(State * state, SDL_Surface * surface)
{
    SDL_BlitSurface(surface, NULL, state->screen_surface, NULL);
    SDL_UpdateWindowSurface(state->window);
}

static SDL_Surface *create_pixmap(const int width, const int height)
{
    SDL_Surface *pixmap;
    pixmap =
        SDL_CreateRGBSurface(SDL_SWSURFACE, WIDTH, HEIGHT, 32, 0x00ff0000,
                             0x0000ff00, 0x000000ff, 0x00000000);
    if (!pixmap) {
        puts("Can not create pixmap");
        exit(1);
    } else {
        puts("Off screen pixmap created");
    }
    return pixmap;
}

void putpixel(SDL_Surface *surface, int x, int y, unsigned char r, unsigned char g, unsigned char b)
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
            return;
        }
        if (surface->format->BitsPerPixel == 32)
        {
            Uint8 *pixel = (Uint8 *)surface->pixels;
            pixel += x*4;
            pixel += y*surface->pitch;
            *pixel++ = b;
            *pixel++ = g;
            *pixel   = r;
            return;
        }
    }
}

void smooth_scene(SDL_Surface *pixmap) {
    SDL_Surface* tmp = SDL_ConvertSurface(pixmap, pixmap->format, SDL_SWSURFACE);
    Uint8 *src;
    Uint8 *dst;
    int x, y;
    int srcc_offset;

    SDL_FillRect(pixmap, NULL, 0x00);
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
} Model;

void initRules(Model *model) {
    int i, j;

    for (j=0; j<4; j++) {
        for (i=0; i<4; i++) {
            model->rules[i][j] = 2.0*(float)rand()/RAND_MAX-1.0;
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

void redraw(State *state, SDL_Surface *pixmap, Model *model) {
    int i;

    Atoms atoms = model->atoms;

    SDL_FillRect(pixmap, NULL, 0x00);
    for (i=0; i<atoms.max; i++) {
        Point point = atoms.points[i];
        Color color = atoms.colors[point.type];
        putpixel(pixmap, point.x, point.y, color.r, color.g, color.b);
        putpixel(pixmap, point.x-1, point.y, color.r, color.g, color.b);
        putpixel(pixmap, point.x+1, point.y, color.r, color.g, color.b);
        putpixel(pixmap, point.x, point.y-1, color.r, color.g, color.b);
        putpixel(pixmap, point.x, point.y+1, color.r, color.g, color.b);
    }

#ifdef SMOOTH
    smooth_scene(pixmap);
#endif
    show_pixmap(state, pixmap);
}

void applyRules(Model *model) {
    int i, j;

    for (i=0; i<model->atoms.max; i++) {
        float fx = 0.0;
        float fy = 0.0;
        Point *a = &model->atoms.points[i];
        for (j=0; j<model->atoms.max; j++) {
            if (i != j) {
                Point *b = &model->atoms.points[j];
                float g = model->rules[a->type][b->type] * SCALE_FACTOR;
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

        a->vx = (a->vx + fx) * DAMPING_FACTOR;
        a->vy = (a->vy + fy) * DAMPING_FACTOR;
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

static void main_event_loop(State * state, SDL_Surface * pixmap, Model *model) {
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
        applyRules(model);
        redraw(state, pixmap, model);
        SDL_Delay(10);
    } while (!done);
}

Model init_model(void) {
    int maxPoints = MAX_RED+MAX_GREEN+MAX_BLUE+MAX_YELLOW;

    Color redColor = {255, 80, 80};
    Color greenColor = {80, 255, 80};
    Color blueColor = {80, 80, 255};
    Color yellowColor = {255, 255, 80};

    Model model;

    initRules(&model);
    model.atoms.colors[RED] = redColor;
    model.atoms.colors[GREEN] = greenColor;
    model.atoms.colors[BLUE] = blueColor;
    model.atoms.colors[YELLOW] = yellowColor;

    model.atoms.points = (Point*)malloc(maxPoints*sizeof(Point));
    model.atoms.max = maxPoints;

    createPoints(MAX_RED, model.atoms.points, RED);
    createPoints(MAX_GREEN, model.atoms.points+MAX_RED, GREEN);
    createPoints(MAX_BLUE, model.atoms.points+MAX_RED+MAX_GREEN, BLUE);
    createPoints(MAX_YELLOW, model.atoms.points+MAX_RED+MAX_GREEN+MAX_BLUE, YELLOW);

    return model;
}

int main(int argc, char **argv)
{
    State state;
    Model model;
    SDL_Surface *pixmap;

    init_sdl(&state, WIDTH, HEIGHT);

    pixmap = create_pixmap(WIDTH, HEIGHT);

    model = init_model();

    main_event_loop(&state, pixmap, &model);

    finalize(&state, pixmap);

    return 0;
}
