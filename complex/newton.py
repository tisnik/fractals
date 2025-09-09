#!/usr/bin/env python

"""Renderer of the classic Newton fractal."""

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


import math

from PIL import Image

# textura by mela byt ctvercova a jeji sirka i vyska by mela byt
# mocninou cisla 2
IMAGE_WIDTH = 512
IMAGE_HEIGHT = 512


def newton(cx, cy, maxiter):
    """Calculate number of iterations for given complex number to escape from set."""
    # avoid div by zero
    if cx == 0 and cy == 0:
        return 0
    z = complex(cx, cy)
    p = 3
    for i in range(maxiter):
        if abs(z - 1.0) < 0.01:
            return i
        if abs(z - complex(-0.5, math.sqrt(3)/2)) < 0.01:
            return i + 128
        if abs(z - complex(-0.5, -math.sqrt(3)/2)) < 0.01:
            return i + 192
        z = ((p-1)*z**p + 1) / (p*z**(p-1))

    return 0


def recalc_fractal(image, palette, xmin, ymin, xmax, ymax, maxiter=1000):
    """Recalculate the whole fractal and render the set into given image."""
    width, height = image.size  # rozmery obrazku
    stepx = (xmax - xmin) / width
    stepy = (ymax - ymin) / height

    y1 = ymin
    for y in range(height):
        x1 = xmin
        for x in range(width):
            i = newton(x1, y1, maxiter)
            i = 3 * i % 256
            color = (palette[i][0], palette[i][1], palette[i][2])
            image.putpixel((x, y), color)
            x1 += stepx
        y1 += stepy


def main():
    import palette_mandmap

    image = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT))

    recalc_fractal(image, palette_mandmap.palette, -2.0, -2.0, 2.0, 2.0, 200)
    image.save("newton.png")


if __name__ == "__main__":
    main()
