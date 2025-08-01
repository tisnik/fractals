#
#  (C) Copyright 2024  Pavel Tisnovsky
#
#  All rights reserved. This program and the accompanying materials
#  are made available under the terms of the Eclipse Public License v1.0
#  which accompanies this distribution, and is available at
#  http://www.eclipse.org/legal/epl-v10.html
#
#  Contributors:
#      Pavel Tisnovsky
#


import sys

import palette_blues
import pygame
import pygame.locals
from colors import Colors

TITLE = "Interactive Barnsley Julia J3 renderer"
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 300
IMAGE_WIDTH = 256
IMAGE_HEIGHT = 256

# Mandelbrot fractal parameters
XMIN = -2.0
XMAX = 2.0
YMIN = -2.0
YMAX = 2.0
MAXITER = 100


def initialize_ui(title, width, height):
    """Initialize Pygame display, drawing surface, and clocks."""
    # set window title
    pygame.display.set_caption(title)

    # initialize window
    display = pygame.display.set_mode([width, height])
    display.fill(Colors.BLACK.value)

    clock = pygame.time.Clock()

    return display, clock


def event_loop(display, image1, image2, clock, renderer):
    cx_scr = image1.get_width() / 2 - 1 - 42 * 2
    cy_scr = image1.get_width() / 2 - 1 + 42 * 2
    cx_scr_delta = 0
    cy_scr_delta = 0
    first_draw = True
    maxiter = MAXITER

    while True:
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()

            # modification keys
            mods = pygame.key.get_mods()

            step_delta = 1
            if mods & pygame.locals.KMOD_SHIFT:
                step_delta = 10
            if mods & pygame.locals.KMOD_CTRL:
                step_delta = 5

            if event.type == pygame.locals.KEYDOWN:
                if event.key == pygame.locals.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.locals.K_RETURN:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.locals.K_LEFT:
                    cx_scr_delta = -step_delta
                if event.key == pygame.locals.K_RIGHT:
                    cx_scr_delta = step_delta
                if event.key == pygame.locals.K_UP:
                    cy_scr_delta = -step_delta
                if event.key == pygame.locals.K_DOWN:
                    cy_scr_delta = step_delta
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
        cx_scr = max(cx_scr, 0)
        cx_scr = min(cx_scr, image1.get_width() - 1)
        cy_scr = max(cy_scr, 0)
        cy_scr = min(cy_scr, image1.get_height() - 1)

        # recalculate Julia set if needed
        if cx_scr_delta != 0 or cy_scr_delta != 0 or first_draw:
            first_draw = False
            scale_x = (XMAX - XMIN) / image1.get_width()
            scale_y = (YMAX - YMIN) / image1.get_height()

            cx = cx_scr * scale_x + XMIN
            cy = cy_scr * scale_y + YMIN

            renderer(
                image2, palette_blues.palette, -2.0, -2.0, 2.0, 2.0, cx, cy, maxiter
            )

        # display Mandelbrot set and Julia se
        display.blit(image1, (0, 0))
        display.blit(image2, (10 + image1.get_width(), 0))

        # display C coordinates
        pygame.draw.line(
            display, Colors.WHITE.value, (cx_scr, 0), (cx_scr, image1.get_height() - 1)
        )
        pygame.draw.line(
            display, Colors.WHITE.value, (0, cy_scr), (image1.get_width() - 1, cy_scr)
        )

        # and update the whole display
        pygame.display.update()
        clock.tick(25)


def barnsley_m3(cx, cy, maxiter):
    """Calculate number of iterations for given complex number to escape from set."""
    c = complex(cx, cy)
    z = 0
    for i in range(maxiter):
        if abs(z) > 2:
            return i
        if z.real > 0:
            zx = z.real*z.real - z.imag*z.imag - 1
            zy = 2*z.real * z.imag
        else:
            zx = z.real*z.real - z.imag*z.imag - 1 + c.real*z.real
            zy = 2*z.real * z.imag + c.imag*z.real
        z = complex(zx, zy)

    return 0


def recalc_barnsley_m3(image, palette, xmin, ymin, xmax, ymax, maxiter=100):
    """Recalculate the whole fractal and render the set into given image."""
    width, height = image.get_size()  # rozmery obrazku
    stepx = (xmax - xmin) / width
    stepy = (ymax - ymin) / height

    y1 = ymin
    for y in range(height):
        x1 = xmin
        for x in range(width):
            i = barnsley_m3(x1, y1, maxiter)
            i = 3 * i % 256
            color = palette[i][2] + (palette[i][1] << 8) + (palette[i][0] << 16)
            image.set_at((x, y), color)
            x1 += stepx
        y1 += stepy


def barnsley_j3(zx0, zy0, cx, cy, maxiter):
    """Calculate number of iterations for given complex number to escape from set."""
    c = complex(cx, cy)
    z = complex(zx0, zy0)
    for i in range(maxiter):
        if abs(z) > 2:
            return i
        if z.real > 0:
            zx = z.real*z.real - z.imag*z.imag - 1
            zy = 2*z.real * z.imag
        else:
            zx = z.real*z.real - z.imag*z.imag - 1 + c.real*z.real
            zy = 2*z.real * z.imag + c.imag*z.real
        z = complex(zx, zy)

    return 0


def recalc_barnsley_j3(image, palette, xmin, ymin, xmax, ymax, cx, cy, maxiter=1000):
    """Recalculate the whole fractal and render the set into given image."""
    width, height = image.get_size()  # rozmery obrazku
    stepx = (xmax - xmin) / width
    stepy = (ymax - ymin) / height

    y1 = ymin
    for y in range(height):
        x1 = xmin
        for x in range(width):
            i = barnsley_j3(x1, y1, cx, cy, maxiter)
            i = 3 * i % 256
            color = palette[i][2] + (palette[i][1] << 8) + (palette[i][0] << 16)
            image.set_at((x, y), color)
            x1 += stepx
        y1 += stepy


def main():
    display, clock = initialize_ui(TITLE, SCREEN_WIDTH, SCREEN_HEIGHT)
    image1 = pygame.Surface([IMAGE_WIDTH, IMAGE_HEIGHT])
    image2 = pygame.Surface([IMAGE_WIDTH, IMAGE_HEIGHT])

    recalc_barnsley_m3(image1, palette_blues.palette, XMIN, YMIN, XMAX, YMAX, MAXITER)
    event_loop(display, image1, image2, clock, recalc_barnsley_j3)


if __name__ == "__main__":
    main()


# finito
