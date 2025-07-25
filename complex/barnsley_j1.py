#!/usr/bin/env python

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



"""Renderer of the classic Barnsley J1 fractal."""

from PIL import Image

# textura by mela byt ctvercova a jeji sirka i vyska by mela byt
# mocninou cisla 2
IMAGE_WIDTH = 512
IMAGE_HEIGHT = 512


def barnsley_j1(zx0, zy0, cx, cy, maxiter):
    """Calculate number of iterations for given complex number to escape from set."""
    c = complex(cx, cy)
    z = complex(zx0, zy0)
    for i in range(maxiter):
        if abs(z) > 2:
            return i
        if z.real >= 0:
            z = (z - 1) * c
        else:
            z = (z + 1) * c

    return 0


def recalc_fractal(image, palette, xmin, ymin, xmax, ymax, cx, cy, maxiter=1000):
    """Recalculate the whole fractal and render the set into given image."""
    width, height = image.size  # rozmery obrazku
    stepx = (xmax - xmin) / width
    stepy = (ymax - ymin) / height

    y1 = ymin
    for y in range(height):
        x1 = xmin
        for x in range(width):
            i = barnsley_j1(x1, y1, cx, cy, maxiter)
            i = 3 * i % 256
            color = (palette[i][0], palette[i][1], palette[i][2])
            image.putpixel((x, y), color)
            x1 += stepx
        y1 += stepy


def main():
    import palette_blues
    import palette_gold
    import palette_mandmap

    image = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT))

    recalc_fractal(image, palette_blues.palette, -2.0, -2.0, 2.0, 2.0, 0.4, 1.5, 500)
    image.save("barnsley_j1_1.png")

    recalc_fractal(image, palette_blues.palette, -2.0, -2.0, 2.0, 2.0, 1.2, -0.6, 500)
    image.save("barnsley_j1_2.png")

    recalc_fractal(image, palette_gold.palette, -1.5, -1.5, 1.5, 1.5, 0.285, 1.31, 500)
    image.save("barnsley_j1_3.png")


if __name__ == "__main__":
    main()
