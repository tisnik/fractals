#!/usr/bin/env python

"""Renderer of the classic Mandelbrot fractal: spiral forms."""

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

import palette_mandmap
from PIL import Image

# image size specified in pixels
# the size of the image should be square, and its height and width
# should be an integer power of 2
IMAGE_WIDTH = 512
IMAGE_HEIGHT = 384

# bailout value
BAILOUT = 2


def mandelbrot(cx, cy, maxiter):
    """Calculate number of iterations for given complex number to escape from set."""
    c = complex(cx, cy)
    z = 0
    for i in range(maxiter):
        if abs(z) > BAILOUT:
            return i
        z = z * z + c
    return 0


def recalc_fractal(image, palette, xmin, ymin, xmax, ymax, maxiter=1000):
    """Recalculate the whole fractal and render the set into given image."""
    width, height = image.size  # image size in pixels
    stepx = (xmax - xmin) / width
    stepy = (ymax - ymin) / height

    y1 = ymin
    for y in range(height):
        x1 = xmin
        for x in range(width):
            i = mandelbrot(x1, y1, maxiter)
            i = 3 * i % 256
            color = (palette[i][0], palette[i][1], palette[i][2])
            image.putpixel((x, y), color)
            x1 += stepx
        y1 += stepy


def main():
    """Function called after the script initialization."""
    image = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT))

    print("Fractal 1 of 4: calculation started")
    t1 = time()
    recalc_fractal(
        image,
        palette_mandmap.palette,
        -0.769824999999999998320,
        -0.109270000000000000000,
        -0.766247499999999998426,
        -0.106570000000000000000,
        1000,
    )
    t2 = time()
    difftime = t2 - t1
    print(f"Fractal 1 of 4: calculation finished in {difftime:4.1f} seconds")
    image.save("spiral_1.png")

    print("Fractal 2 of 4: calculation started")
    t1 = time()
    recalc_fractal(
        image,
        palette_mandmap.palette,
        -0.171119200000000013445,
        0.657309400000000000000,
        -0.169318975000000013445,
        0.658660750000000000000,
        1000,
    )
    t2 = time()
    difftime = t2 - t1
    print(f"Fractal 2 of 4: calculation finished in {difftime:4.1f} seconds")
    image.save("spiral_2.png")

    print("Fractal 3 of 4: calculation started")
    t1 = time()
    recalc_fractal(
        image,
        palette_mandmap.palette,
        -0.207190825000000012496,
        0.676656624999999999983,
        -0.206107925000000012496,
        0.677468799999999999983,
        1000,
    )
    t2 = time()
    difftime = t2 - t1
    print(f"Fractal 3 of 4: calculation finished in {difftime:4.1f} seconds")
    image.save("spiral_3.png")

    print("Fractal 3 of 4: calculation started")
    t1 = time()
    recalc_fractal(
        image,
        palette_mandmap.palette,
        -0.540623850000000003876,
        0.523798050000000000019,
        -0.532306600000000003876,
        0.530031950000000000019,
        1000,
    )
    t2 = time()
    difftime = t2 - t1
    print(f"Fractal 4 of 4: calculation finished in {difftime:4.1f} seconds")
    image.save("spiral_4.png")


if __name__ == "__main__":
    # call the main function
    main()
