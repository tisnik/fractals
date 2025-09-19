#!/usr/bin/env python

"""Renderer of the classic Magnet M1 fractal."""

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

# image size specified in pixels
# the size of the image should be square, and its height and width
# should be an integer power of 2
IMAGE_WIDTH = 512
IMAGE_HEIGHT = 512

# bailout value
BAILOUT = 100


def magnet_m1(cx, cy, maxiter):
    """Calculate number of iterations for given complex number to escape from set."""
    c = complex(cx, cy)
    z = 0
    for i in range(maxiter):
        if abs(z) > BAILOUT:
            return i
        z = ((z**2 + (c-1)) / (2*z + (c-2)))**2

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
            i = magnet_m1(x1, y1, maxiter)
            i = 3 * i % 256
            color = (palette[i][0], palette[i][1], palette[i][2])
            image.putpixel((x, y), color)
            x1 += stepx
        y1 += stepy


def main():
    """Function called after the script initialization."""
    import palette_blues

    # construct new image
    image = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT))

    print("Calculation started")
    t1 = time()
    recalc_fractal(image, palette_blues.palette, -2.0, -2.0, 2.0, 2.0, 500)
    image.save("magnet_m1.png")
    t2 = time()
    difftime = t2 - t1
    print(f"Calculation finished in {difftime:4.1f} seconds")


if __name__ == "__main__":
    main()
