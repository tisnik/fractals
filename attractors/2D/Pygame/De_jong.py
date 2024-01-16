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


from math import cos, sin

from bitmap import create_bitmap, draw_bitmap
from ui import event_loop, initialize

# window settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "De jong strange attractor"


def de_jong(x, y, a, b, c, d):
    """Calculate next point in the strange attractor."""
    x_dot = sin(a * y) - cos(b * x)
    y_dot = sin(c * x) - cos(d * y)
    return x_dot, y_dot


def redraw_system(surface):
    """Redraw the whole dynamical system."""
    width, height = surface.get_size()
    bitmap = create_bitmap(width, height)

    A = -2.7
    B = -0.09
    C = -0.86
    D = -2.20

    max_points = 1000000
    settle_down_points = 10

    x = 0
    y = 0
    scale = 180.0
    x_offset = 120
    y_offset = -80

    for i in range(max_points):
        x_dot, y_dot = de_jong(x, y, A, B, C, D)
        xi = width//2 + int(scale*x_dot) + x_offset
        yi = height//2 + int(scale*y_dot) + y_offset

        # try to draw pixel
        if i > settle_down_points:
            if xi >=0 and yi >=0 and xi < width and yi < height:
                bitmap[yi][xi] += 1

        # next point calculation
        x, y = x_dot, y_dot

    draw_bitmap(bitmap, surface, 1/1000.0)


def main():
    # initialize user interface based on Pygame
    display, surface, clock = initialize(WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT)

    # redraw the whole dynamical system
    redraw_system(surface)

    # and enter the event loop
    event_loop(display, surface, clock)


if __name__ == "__main__":
    main()
