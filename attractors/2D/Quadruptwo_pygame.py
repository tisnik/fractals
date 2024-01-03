# vim: set fileencoding=utf-8

import sys
from enum import Enum
from math import copysign, sin, atan
from math import log as ln

import pygame
import pygame.locals

# window settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Quadruptwo dynamical system"


class Colors(Enum):
    """Named colors used everywhere on demo screens."""

    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)
    CYAN = (0, 255, 255)
    GREEN = (0, 255, 0)
    YELLOW = (255, 255, 0)
    RED = (255, 0, 0)
    MAGENTA = (255, 0, 255)
    WHITE = (255, 255, 255)


def sqr(x):
    """Square calculation."""
    return x * x


def redraw_system(surface):
    """Redraw the whole dynamical system."""
    surface.fill(Colors.BLACK.value)

    a = 3.1
    b = 1.8
    c = -0.9

    x = 0
    y = 0

    max_points = 1000000
    scale = 9.0

    for i in range(max_points):
        xi = WINDOW_WIDTH//2 + int(scale*x)
        yi = WINDOW_HEIGHT//2 + int(scale*y)
        # try to draw pixel
        if xi >=0 and yi >=0 and xi < WINDOW_WIDTH and yi < WINDOW_HEIGHT:
            surface.set_at((xi, yi), i*10)

        # next point calculation
        x_dot = y - copysign(1, x) * sin(ln(abs(b * x - c))) * atan(sqr(ln(abs(c * x - b))))
        y_dot = a - x
        x, y = x_dot, y_dot


def event_loop(display, surface, clock):
    """Event loop that just waits for keypress or window close operation."""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.locals.KEYDOWN:
                if event.key == pygame.locals.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.locals.K_RETURN:
                    pygame.quit()
                    sys.exit()

        # all events has been processed - update scene and redraw the screen
        display.blit(surface, (0, 0))
        pygame.display.update()
        clock.tick(25)


def main():
    # set window title
    pygame.display.set_caption(WINDOW_TITLE)

    # initialize window
    display = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
    display.fill(Colors.BLACK.value)

    # create all required Pygame objects
    surface = pygame.Surface([WINDOW_WIDTH, WINDOW_HEIGHT])
    clock = pygame.time.Clock()

    # redraw the whole dynamical system
    redraw_system(surface)

    # and enter the event loop
    event_loop(display, surface, clock)


if __name__ == "__main__":
    main()
