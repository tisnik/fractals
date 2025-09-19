#!/usr/bin/env python

"""Renderer of the Phoenix fractal, Julia version."""

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
BAILOUT = 4

def recalc_fractal(image, palette, xmin, ymin, xmax, ymax, cx, cy, maxiter=1000):
    """Recalculate the whole fractal and render the set into given image."""
    width, height = image.size  # rozmery obrazku
    stepx = (xmax - xmin) / width
    stepy = (ymax - ymin) / height

    zy0 = ymin
    for y in range(height):
        zx0 = xmin
        for x in range(width):
            zx = zx0
            zy = zy0
            ynx = 0.0
            yny = 0.0
            for i in range(maxiter):
                zx2 = zx*zx
                zy2 = zy*zy
                zxn = zx2 - zy2 + cx + cy * ynx
                zyn = 2.0 * zx * zy + cy * yny
                ynx = zx
                yny = zy
                zx = zxn
                zy = zyn
                if zx2 + zy2 > BAILOUT:
                    break
            i = 3 * i % 256
            color = (palette[i][0], palette[i][1], palette[i][2])
            image.putpixel((x, y), color)
            zx0 += stepx
        zy0 += stepy


def main():
    """Function called after the script initialization."""
    import palette_blues

    # construct new image
    image = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT))

    print("Calculation started")
    t1 = time()
    recalc_fractal(image, palette_blues.palette, -2.0, -2.0, 2.0, 2.0, 0.0, 1.0, 1000)
    t2 = time()
    difftime = t2 - t1
    print(f"Calculation finished in {difftime:4.1f} seconds")

    # save image with fractal
    image.save("phoenix_j.png")

    print("Calculation started")
    t1 = time()
    recalc_fractal(image, palette_blues.palette, -2.0, -2.0, 2.0, 2.0, -0.4, -1.2, 1000)
    t2 = time()
    difftime = t2 - t1
    print(f"Calculation finished in {difftime:4.1f} seconds")

    # save image with fractal
    image.save("phoenix_j_2.png")


if __name__ == "__main__":
    # call the main function
    main()
