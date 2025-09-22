#!/usr/bin/env python

"""Julia fractal - some spiral variants."""

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

from time import time

from PIL import Image

IMAGE_WIDTH = 512
IMAGE_HEIGHT = 384


def julia(cx, cy, zx, zy, maxiter):
    """Výpočet, kolik iterací je nutné pro opuštění jednotkového kruhu."""
    c = complex(cx, cy)
    z = complex(zx, zy)
    for i in range(maxiter):
        if abs(z) > 2:
            return i
        z = z * z + c
    return 0


def recalc_fractal(image, palette, cx, cy, maxiter=1000):
    """Přepočet celého fraktálu."""
    xmin = -2.0
    ymin = -1.5
    xmax = 2.0
    ymax = 1.5
    width, height = image.size  # rozměry obrázku
    stepx = (xmax - xmin) / width
    stepy = (ymax - ymin) / height

    y1 = ymin
    for y in range(height):
        x1 = xmin
        for x in range(width):
            i = julia(cx, cy, x1, y1, maxiter)
            i = 3 * i % 256
            color = (palette[i][0], palette[i][1], palette[i][2])
            image.putpixel((x, y), color)
            x1 += stepx
        y1 += stepy


def main():
    import palette_greens

    image = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT))

    recalc_fractal(
        image,
        palette_greens.palette,
        -0.769824999999999998320,
        -0.109270000000000000000,
        255,
    )
    image.save("spiral_1.png")

    recalc_fractal(
        image,
        palette_greens.palette,
        -0.171119200000000013445,
        0.657309400000000000000,
        255,
    )
    image.save("spiral_2.png")

    recalc_fractal(
        image,
        palette_greens.palette,
        -0.207190825000000012496,
        0.676656624999999999983,
        255,
    )
    image.save("spiral_3.png")

    recalc_fractal(
        image,
        palette_greens.palette,
        -0.540623850000000003876,
        0.523798050000000000019,
        255,
    )
    image.save("spiral_4.png")


if __name__ == "__main__":
    main()
