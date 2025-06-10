import sys
from ctypes import CDLL, c_double, c_int, create_string_buffer
from enum import Enum

import pygame
import pygame.locals
from palette_blues import palette as blues
from palette_gold import palette as gold
from palette_greens import palette as greens
from palette_ice import palette as ice
from palette_juteblue import palette as juteblue
from palette_jutemap import palette as jutemap
from palette_jutes import palette as jutes
from palette_mandmap import palette as mandmap
from palette_phong import palette as phong
from palette_rose import palette as rose
from palette_volcano import palette as volcano
from palette_chroma import palette as chroma

DISPLAY_C_COORDINATES = True

TITLE = "Svitava GUI: {name} + Julia variant  [T]ype  [P]alette  [+/-]iter   [H]elp"
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 300
IMAGE_WIDTH = 256
IMAGE_HEIGHT = 256

# Mandelbrot fractal parameters
M_XMIN = -2.0
M_XMAX = 1.0
M_YMIN = -1.5
M_YMAX = 1.5
MAXITER = 100

# Mandelbrot^3 fractal parameters
M3_XMIN = -1.5
M3_XMAX = 1.5
M3_YMIN = -1.5
M3_YMAX = 1.5

XSTART = 30
YSTART = 20

# Barnsley M1 and J1
B_XMIN = -2.0
B_XMAX = 2.0
B_YMIN = -2.0
B_YMAX = 2.0

# Magnet M1 and J1
M_XMIN = -2.0
M_XMAX = 2.0
M_YMIN = -2.0
M_YMAX = 2.0

fractal_type_index = 0
fractal_limits = {
    "Mandelbrot": (M_XMIN, M_XMAX, M_YMIN, M_YMAX),
    "Mandelbrot3": (M3_XMIN, M3_XMAX, M3_YMIN, M3_YMAX),
    "Barnsley M1": (B_XMIN, B_XMAX, B_YMIN, B_YMAX),
    "Barnsley M2": (B_XMIN, B_XMAX, B_YMIN, B_YMAX),
    "Barnsley M3": (B_XMIN, B_XMAX, B_YMIN, B_YMAX),
    "Magnet M1": (B_XMIN, B_XMAX, B_YMIN, B_YMAX),
    "Magnet M2": (B_XMIN, B_XMAX, B_YMIN, B_YMAX),
    "Phoenix": (M_XMIN, M_XMAX, M_YMIN, M_YMAX),
    "Newton": (M_XMIN, M_XMAX, M_YMIN, M_YMAX),
}
fractal_types = list(fractal_limits.keys())
maxiter = 150


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


def set_window_title(fractal_types, fractal_type_index):
    """Set the window title."""
    name = fractal_types[fractal_type_index]
    title = TITLE.format(name=name)
    pygame.display.set_caption(title)


def initialize_ui(title, width, height):
    """Initialize Pygame display, drawing surface, and clocks."""
    # set window title
    set_window_title(fractal_types, fractal_type_index)

    # initialize window
    display = pygame.display.set_mode([width, height])
    display.fill(Colors.BLACK.value)

    clock = pygame.time.Clock()

    return display, clock


def render_m_set(
    fractal_renderers,
    fractal_type_index,
    image_width,
    image_height,
    palette,
    buffer,
    maxiter,
):
    fractal_type = fractal_types[fractal_type_index]
    renderer = fractal_renderers[fractal_type][0]
    renderer(c_int(image_width), c_int(image_height), palette, buffer, c_int(maxiter))


def render_j_set(
    fractal_renderers,
    fractal_type_index,
    image_width,
    image_height,
    palette,
    buffer,
    cx,
    cy,
    maxiter,
):
    fractal_type = fractal_types[fractal_type_index]
    renderer = fractal_renderers[fractal_type][1]
    renderer(
        c_int(image_width),
        c_int(image_height),
        palette,
        buffer,
        c_double(cx),
        c_double(cy),
        c_int(maxiter),
    )


def event_loop(display, image1, image2, clock, palettes, fractal_renderers, buffer):
    global fractal_type_index
    global maxiter
    palette_index = 0

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
                    fractal_type_index += 1
                    if fractal_type_index >= len(fractal_types):
                        fractal_type_index = 0
                    set_window_title(fractal_types, fractal_type_index)
                    first_draw = True
                if event.key == pygame.locals.K_p:
                    palette_index += 1
                    if palette_index >= len(palettes):
                        palette_index = 0
                    first_draw = True
                if event.key == pygame.locals.K_LEFT:
                    cx_scr_delta = -1
                if event.key == pygame.locals.K_RIGHT:
                    cx_scr_delta = 1
                if event.key == pygame.locals.K_UP:
                    cy_scr_delta = -1
                if event.key == pygame.locals.K_DOWN:
                    cy_scr_delta = 1
                if event.key == pygame.locals.K_EQUALS:
                    maxiter += 10
                    first_draw = True
                    print("Maxiter:", maxiter)
                if event.key == pygame.locals.K_MINUS:
                    maxiter -= 10
                    first_draw = True
                    print("Maxiter:", maxiter)
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

        pal = palettes[palette_index]

        xmin, xmax, ymin, ymax = fractal_limits[fractal_types[fractal_type_index]]
        if first_draw:
            render_m_set(
                fractal_renderers,
                fractal_type_index,
                IMAGE_WIDTH,
                IMAGE_HEIGHT,
                pal,
                buffer,
                maxiter,
            )
            image1 = image_from_buffer(buffer, IMAGE_WIDTH, IMAGE_HEIGHT, "RGBX")

        # recalculate Julia set if needed
        if cx_scr_delta != 0 or cy_scr_delta != 0 or first_draw:
            first_draw = False
            scale_x = (xmax - xmin) / image1.get_width()
            scale_y = (ymax - ymin) / image1.get_height()

            cx = cx_scr * scale_x + xmin
            cy = cy_scr * scale_y + ymin

            if DISPLAY_C_COORDINATES:
                print(cx, cy)

            render_j_set(
                fractal_renderers,
                fractal_type_index,
                IMAGE_WIDTH,
                IMAGE_HEIGHT,
                pal,
                buffer,
                cx,
                cy,
                maxiter,
            )
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


def fill_in_fractal_renderers(renderer):
    fractal_renderers = {
        "Mandelbrot": (renderer.render_mandelbrot, renderer.render_julia),
        "Mandelbrot3": (renderer.render_mandelbrot_3, renderer.render_julia_3),
        "Barnsley M1": (renderer.render_barnsley_m1, renderer.render_barnsley_j1),
        "Barnsley M2": (renderer.render_barnsley_m2, renderer.render_barnsley_j2),
        "Barnsley M3": (renderer.render_barnsley_m3, renderer.render_barnsley_j3),
        "Magnet M1": (renderer.render_magnet_m1, renderer.render_magnet_j1),
        "Magnet M2": (renderer.render_magnet_m2, renderer.render_magnet_j2),
        "Phoenix": (renderer.render_phoenix_m, renderer.render_phoenix_j),
        "Newton": (renderer.render_newton_m, renderer.render_newton_j),
    }
    return fractal_renderers


def main():
    palettes = [
        palette_to_buffer(mandmap),
        palette_to_buffer(blues),
        palette_to_buffer(gold),
        palette_to_buffer(greens),
        palette_to_buffer(ice),
        palette_to_buffer(juteblue),
        palette_to_buffer(jutemap),
        palette_to_buffer(jutes),
        palette_to_buffer(phong),
        palette_to_buffer(rose),
        palette_to_buffer(volcano),
        palette_to_buffer(chroma),
    ]

    display, clock = initialize_ui(TITLE, SCREEN_WIDTH, SCREEN_HEIGHT)

    svitava = CDLL("./svitava.so")
    fractal_renderers = fill_in_fractal_renderers(svitava)

    buffer = create_string_buffer(4 * IMAGE_WIDTH * IMAGE_HEIGHT)

    image1 = pygame.Surface([IMAGE_WIDTH, IMAGE_HEIGHT])
    image2 = pygame.Surface([IMAGE_WIDTH, IMAGE_HEIGHT])

    event_loop(display, image1, image2, clock, palettes, fractal_renderers, buffer)


if __name__ == "__main__":
    main()


# finito
