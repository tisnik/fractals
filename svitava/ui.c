#include <SDL2/SDL.h>

/* graphics options */
#define WIDTH 640
#define HEIGHT 480
#define TITLE "Svitava"

typedef struct GraphicsState {
    SDL_Window *window;
    SDL_Surface *screen_surface;
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
    SDL_FreeSurface(graphicsState->screen_surface);
    SDL_DestroyWindow(graphicsState->window);
    SDL_Quit();
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

    init_sdl(&graphicsState, TITLE, WIDTH, HEIGHT);

    main_event_loop(&graphicsState);

    finalize(&graphicsState);

    return 0;
}
