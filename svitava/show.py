import sys
from ctypes import CDLL, c_int, c_double, create_string_buffer

import pygame
import pygame.locals

from palette_mandmap import palette
from enum import Enum

TITLE = "Svitava GUI: classic Mandelbrot + Julia  [T] to change fractal type"
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 300
IMAGE_WIDTH = 256
IMAGE_HEIGHT = 256

# Mandelbrot fractal parameters
XMIN = -2.0
XMAX = 1.0
YMIN = -1.5
YMAX = 1.5
MAXITER = 100

XSTART = 30
YSTART = 20

# Barnsley M1 and J1
XMIN = -2.0
XMAX = 2.0
YMIN = -2.0
YMAX = 2.0

fractal_types = ()


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


def initialize_ui(title, width, height):
    """Initialize Pygame display, drawing surface, and clocks."""
    # set window title
    pygame.display.set_caption(title)

    # initialize window
    display = pygame.display.set_mode([width, height])
    display.fill(Colors.BLACK.value)

    clock = pygame.time.Clock()

    return display, clock


def render_m_set(image_width, image_height, palette, renderer, buffer):
    renderer.render_barnsley_m1(
        c_int(image_width), c_int(image_height), palette, buffer
    )


def render_j_set(image_width, image_height, palette, renderer, buffer, cx, cy):
    renderer.render_barnsley_j1(
        c_int(image_width),
        c_int(image_height),
        palette,
        buffer,
        c_double(cx),
        c_double(cy),
    )


def event_loop(display, image1, image2, clock, pal, renderer, buffer):
    cx_scr = image1.get_width() / 2 - 1 + 32
    cy_scr = image1.get_width() / 2 - 1 - 42 * 2
    cx_scr_delta = 0
    cy_scr_delta = 0
    first_draw = True

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
                if event.key == pygame.locals.K_t:
                    print("Change type")
                if event.key == pygame.locals.K_LEFT:
                    cx_scr_delta = -1
                if event.key == pygame.locals.K_RIGHT:
                    cx_scr_delta = 1
                if event.key == pygame.locals.K_UP:
                    cy_scr_delta = -1
                if event.key == pygame.locals.K_DOWN:
                    cy_scr_delta = 1
            if event.type == pygame.locals.KEYUP:
                if event.key == pygame.locals.K_LEFT:
                    cx_scr_delta = 0
                if event.key == pygame.locals.K_RIGHT:
                    cx_scr_delta = 0
                if event.key == pygame.locals.K_UP:
                    cy_scr_delta = 0
                if event.key == pygame.locals.K_DOWN:
                    cy_scr_delta = 0

        # all events has been processed - update scene and redraw the screen

        # keep moving C
        cx_scr += cx_scr_delta
        cy_scr += cy_scr_delta

        # check for limits
        if cx_scr < 0:
            cx_scr = 0
        if cx_scr > image1.get_width() - 1:
            cx_scr = image1.get_width() - 1
        if cy_scr < 0:
            cy_scr = 0
        if cy_scr > image1.get_height() - 1:
            cy_scr = image1.get_height() - 1

        # recalculate Julia set if needed
        if cx_scr_delta != 0 or cy_scr_delta != 0 or first_draw:
            first_draw = False
            scale_x = (XMAX - XMIN) / image1.get_width()
            scale_y = (YMAX - YMIN) / image1.get_height()

            cx = cx_scr * scale_x + XMIN
            cy = cy_scr * scale_y + YMIN

            render_j_set(IMAGE_WIDTH, IMAGE_HEIGHT, pal, renderer, buffer, cx, cy)
            image2 = image_from_buffer(buffer, IMAGE_WIDTH, IMAGE_HEIGHT, "RGBX")

        # display Mandelbrot set and Julia se
        display.blit(image1, (XSTART, YSTART))
        display.blit(image2, (60 + image1.get_width(), YSTART))

        # display C coordinates
        pygame.draw.line(
            display,
            Colors.WHITE.value,
            (XSTART + cx_scr, YSTART),
            (XSTART + cx_scr, YSTART + image1.get_height() - 1),
        )
        pygame.draw.line(
            display,
            Colors.WHITE.value,
            (XSTART, YSTART + cy_scr),
            (XSTART + image1.get_width() - 1, YSTART + cy_scr),
        )

        # and update the whole display
        pygame.display.update()
        clock.tick(25)


def palette_to_buffer(p):
    s = create_string_buffer(len(p) * 3)
    i = 0
    for color in p:
        s[i] = color[0]
        s[i + 1] = color[1]
        s[i + 2] = color[2]
        i += 3
    return s


def image_from_buffer(buffer, width, height, fmt):
    return pygame.image.frombytes(bytes(buffer), (width, height), fmt)


def main():
    pal = palette_to_buffer(palette)

    display, clock = initialize_ui(TITLE, SCREEN_WIDTH, SCREEN_HEIGHT)

    svitava = CDLL("./svitava.so")

    buffer = create_string_buffer(4 * IMAGE_WIDTH * IMAGE_HEIGHT)

    render_m_set(IMAGE_WIDTH, IMAGE_HEIGHT, pal, svitava, buffer)
    image1 = image_from_buffer(buffer, IMAGE_WIDTH, IMAGE_HEIGHT, "RGBX")

    image2 = pygame.Surface([IMAGE_WIDTH, IMAGE_HEIGHT])

    event_loop(display, image1, image2, clock, pal, svitava, buffer)


if __name__ == "__main__":
    main()


# finito