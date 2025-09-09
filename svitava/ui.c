#include <SDL2/SDL.h>

/* graphics options */
#define SCREEN_WIDTH 600
#define SCREEN_HEIGHT 300
#define IMAGE_WIDTH 256
#define IMAGE_HEIGHT 256
#define TITLE "Svitava"

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

    main_event_loop(&graphicsState);

    finalize(&graphicsState);

    return 0;
}
