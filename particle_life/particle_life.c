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

/* number of particles of different colors/attributes */
#define MAX_RED    3000
#define MAX_GREEN  400
#define MAX_BLUE   400
#define MAX_YELLOW 1000

/* total number of particles */
#define MAX_PARTICLES (MAX_RED+MAX_GREEN+MAX_BLUE+MAX_YELLOW)

#define MAX_DISTANCE 50

#define DAMPING_FACTOR 0.5

#define SLOW_DOWN_FACTOR 0.1

#define SCALE_FACTOR 1

/* integration constant */
#define DT 1.0

/* enable scene smoothing */
int smooth_enabled = 0;

/* enable gravity */
int gravity_enabled = 0;

typedef struct GraphicsState {
    SDL_Window *window;
    SDL_Surface *screen_surface;
} GraphicsState;

static void init_sdl(GraphicsState * graphicsState, const char *title, const int width, const int height)
{
    graphicsState->window = NULL;
    graphicsState->screen_surface = NULL;

    if (SDL_Init(SDL_INIT_VIDEO) < 0) {
        fprintf(stderr, "Error initializing SDL: %s\n", SDL_GetError());
        exit(1);
    } else {
        puts("SDL_Init ok");
    }

    graphicsState->window =
        SDL_CreateWindow(TITLE, SDL_WINDOWPOS_UNDEFINED,
                         SDL_WINDOWPOS_UNDEFINED, width, height,
                         SDL_WINDOW_SHOWN);

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

static void finalize(GraphicsState * graphicsState, SDL_Surface * pixmap)
{
    SDL_FreeSurface(pixmap);
    SDL_FreeSurface(graphicsState->screen_surface);
    SDL_DestroyWindow(graphicsState->window);
    SDL_Quit();
}

static void show_pixmap(GraphicsState * graphicsState, SDL_Surface * surface)
{
    SDL_BlitSurface(surface, NULL, graphicsState->screen_surface, NULL);
    SDL_UpdateWindowSurface(graphicsState->window);
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

void putpixel(SDL_Surface * surface,
              int x, int y,
              unsigned char r, unsigned char g, unsigned char b)
{
    if (x >= 0 && x < surface->w && y >= 0 && y < surface->h) {
        if (surface->format->BitsPerPixel == 24) {
            Uint8 *pixel = (Uint8 *) surface->pixels;
            pixel += x * 3;
            pixel += y * surface->pitch;
            *pixel++ = b;
            *pixel++ = g;
            *pixel = r;
            return;
        }
        if (surface->format->BitsPerPixel == 32) {
            Uint8 *pixel = (Uint8 *) surface->pixels;
            pixel += x * 4;
            pixel += y * surface->pitch;
            *pixel++ = b;
            *pixel++ = g;
            *pixel = r;
            return;
        }
    }
}

void smooth_scene(SDL_Surface * pixmap)
{
    SDL_Surface *tmp =
        SDL_ConvertSurface(pixmap, pixmap->format, SDL_SWSURFACE);
    Uint8 *src;
    Uint8 *dst;
    int x, y;
    int srcc_offset;

    SDL_FillRect(pixmap, NULL, 0x00);
    dst = (Uint8 *) pixmap->pixels + 1 * pixmap->pitch + 1 * pixmap->format->BytesPerPixel;
    src = (Uint8 *) tmp->pixels;

    srcc_offset = tmp->pitch - 3 * tmp->format->BytesPerPixel;

    for (y = 1; y < tmp->h; y++) {
        for (x = 1; x < tmp->w - 1; x++) {
            Uint8 *srcc = src + (x - 1) * tmp->format->BytesPerPixel;
            int rr = 0, gg = 0, bb = 0;
            int dx, dy;
            for (dy = -1; dy <= 1; dy++) {
                for (dx = -1; dx <= 1; dx++) {
                    bb += *srcc++;
                    gg += *srcc++;
                    rr += *srcc++;
                    if (tmp->format->BytesPerPixel == 4) {
                        srcc++;
                    }
                }
                srcc += srcc_offset;
            }
            rr /= 9;
            gg /= 9;
            bb /= 9;
            *dst++ = bb;
            *dst++ = gg;
            *dst++ = rr;
            if (pixmap->format->BitsPerPixel == 32) {
                dst++;
            }
        }
        dst += 2 * pixmap->format->BytesPerPixel;
        src += tmp->pitch;
    }
}

typedef struct {
    float x;
    float y;
    float vx;
    float vy;
    int type;
} Particle;

typedef struct Color {
    unsigned char r;
    unsigned char g;
    unsigned char b;
} Color;

typedef struct {
    Particle *particles;
    int max;
    Color colors[4];
} Atoms;

typedef struct {
    float rules[4][4];
    Atoms atoms;
} Model;

void initRules(Model * model)
{
    int i, j;

    for (j = 0; j < 4; j++) {
        for (i = 0; i < 4; i++) {
            model->rules[i][j] = 2.0 * (float) rand() / RAND_MAX - 1.0;
        }
    }
}

float randomX()
{
    return (WIDTH - BORDER * 2) * (float) rand() / RAND_MAX + BORDER;
}

float randomY()
{
    return (HEIGHT - BORDER * 2) * (float) rand() / RAND_MAX + BORDER;
}

void createParticles(int max, Particle * particles, int type)
{
    int i;
    for (i = 0; i < max; i++) {
        particles[i].x = randomX();
        particles[i].y = randomY();
        particles[i].vx = (float)rand() / RAND_MAX - 0.5;
        particles[i].vy = (float)rand() / RAND_MAX - 0.5;
        particles[i].type = type;
    }
}

void createParticlesOfAllColors(Model *model) {
    createParticles(MAX_RED, model->atoms.particles, RED);
    createParticles(MAX_GREEN, model->atoms.particles + MAX_RED, GREEN);
    createParticles(MAX_BLUE, model->atoms.particles + MAX_RED + MAX_GREEN, BLUE);
    createParticles(MAX_YELLOW, model->atoms.particles + MAX_RED + MAX_GREEN + MAX_BLUE, YELLOW);
}

void redraw(GraphicsState * graphicsState, SDL_Surface * pixmap, Model * model)
{
    int i;

    Atoms atoms = model->atoms;

    SDL_FillRect(pixmap, NULL, 0x00);
    for (i = 0; i < atoms.max; i++) {
        Particle particle = atoms.particles[i];
        Color color = atoms.colors[particle.type];
        putpixel(pixmap, particle.x, particle.y, color.r, color.g, color.b);
        putpixel(pixmap, particle.x - 1, particle.y, color.r, color.g, color.b);
        putpixel(pixmap, particle.x + 1, particle.y, color.r, color.g, color.b);
        putpixel(pixmap, particle.x, particle.y - 1, color.r, color.g, color.b);
        putpixel(pixmap, particle.x, particle.y + 1, color.r, color.g, color.b);
    }

    if (smooth_enabled) {
        smooth_scene(pixmap);
    }
    show_pixmap(graphicsState, pixmap);
}

void applyRules(Model * model)
{
    int i, j;

    for (i = 0; i < model->atoms.max; i++) {
        float fx = 0.0;
        float fy = 0.0;
        Particle *a = &model->atoms.particles[i];

        /* compute force for selected particle */
        for (j = 0; j < model->atoms.max; j++) {
            if (i != j) {
                Particle *b = &model->atoms.particles[j];
                float g = model->rules[a->type][b->type] * SCALE_FACTOR;
                float dx = a->x - b->x;
                float dy = a->y - b->y;
                if (dx != 0.0 || dy != 0.0) {
                    float d = dx * dx + dy * dy;
                    if (d < MAX_DISTANCE*MAX_DISTANCE) {
                        /* repel force */
                        float f = g / sqrt(d);
                        fx += f * dx;
                        fy += f * dy;
                    } else if (gravity_enabled) {
                        float f = 0.0001;
                        fx -= f * dx;
                        fy -= f * dy;
                    }
                }
            }
        }

        /* apply force to selected particle */
        a->vx = (a->vx + fx * DT) * DAMPING_FACTOR;
        a->vy = (a->vy + fy * DT) * DAMPING_FACTOR;

        /* move particle */
        a->x += a->vx;
        a->y += a->vy;

        /* check if particle touches scene boundary */
        if (a->x <= 0) {
            a->vx = -a->vx;
            a->x = 0;
        }
        if (a->x > WIDTH) {
            a->vx = -a->vx;
            a->x = WIDTH - 1;
        }
        if (a->y <= 0) {
            a->vy = -a->vy;
            a->y = 0;
        }
        if (a->y > HEIGHT) {
            a->vy = -a->vy;
            a->y = HEIGHT - 1;
        }
    }
}

void slowDown(Model * model)
{
    int i;
    for (i = 0; i < model->atoms.max; i++) {
        Particle *p = &model->atoms.particles[i];
        p->vx *= SLOW_DOWN_FACTOR;
        p->vy *= SLOW_DOWN_FACTOR;
    }
}

static void main_event_loop(GraphicsState * graphicsState, SDL_Surface * pixmap, Model * model) {
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
                case 'd':
                    slowDown(model);
                    break;
                case 'i':
                    initRules(model);
                    break;
                case 'c':
                    createParticlesOfAllColors(model);
                    break;
                case 's':
                    smooth_enabled = !smooth_enabled;
                    break;
                case 'g':
                    gravity_enabled = !gravity_enabled;
                    break;
                case SDLK_ESCAPE:
                case SDLK_q:
                    done = 1;
                    break;
                default:
                    break;
                }
                break;
            case SDL_KEYUP:
                switch (event.key.keysym.sym) {
                default:
                    break;
                }
            default:
                break;
            }
        }
        applyRules(model);
        redraw(graphicsState, pixmap, model);
        SDL_Delay(10);
    } while (!done);
}

Model init_model(void) {
    Color redColor = { 255, 80, 80 };
    Color greenColor = { 80, 255, 80 };
    Color blueColor = { 80, 80, 255 };
    Color yellowColor = { 255, 255, 80 };

    Model model;

    initRules(&model);
    model.atoms.colors[RED] = redColor;
    model.atoms.colors[GREEN] = greenColor;
    model.atoms.colors[BLUE] = blueColor;
    model.atoms.colors[YELLOW] = yellowColor;

    model.atoms.particles = (Particle *) malloc(MAX_PARTICLES * sizeof(Particle));
    model.atoms.max = MAX_PARTICLES;

    createParticlesOfAllColors(&model);

    return model;
}

int main(int argc, char **argv)
{
    GraphicsState graphicsState;
    Model model;
    SDL_Surface *pixmap;

    init_sdl(&graphicsState, TITLE, WIDTH, HEIGHT);

    pixmap = create_pixmap(WIDTH, HEIGHT);

    model = init_model();

    main_event_loop(&graphicsState, pixmap, &model);

    finalize(&graphicsState, pixmap);

    return 0;
}
