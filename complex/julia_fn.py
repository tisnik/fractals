#!/usr/bin/env python

"""Renderer of the Lambda Julia fractal based on selected function."""

import cmath

from PIL import Image

# image size specified in pixels
# the size of the image should be square, and its height and width
# should be an integer power of 2
IMAGE_WIDTH = 512
IMAGE_HEIGHT = 512

# bailout value
BAILOUT = 64

def julia_fn(zx0, zy0, cx, cy, maxiter):
    """Calculate number of iterations for given complex numbers Z and C to escape from set."""
    c = complex(cx, cy)
    z = complex(zx0, zy0)
    for i in range(maxiter):
        if abs(z) > BAILOUT:
            return i
        z = c * cmath.sin(z)
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
            i = julia_fn(x1, y1, cx, cy, maxiter)
            i = 3 * i % 256
            color = (palette[i][0], palette[i][1], palette[i][2])
            image.putpixel((x, y), color)
            x1 += stepx
        y1 += stepy


def main():
    """Function called after the script initialization."""
    import palette_blues
    import palette_gold
    import palette_mandmap

    # construct new image
    image = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT))

    recalc_fractal(image, palette_blues.palette, -3.0, -3.0, 3.0, 3.0, 0.0, 1.0, 255)
    image.save("julia_fn.png")

    recalc_fractal(image, palette_mandmap.palette, -0.25, -0.7, 0.75, 0.3, 0.85, 0.6, 1000)
    image.save("julia_fn_2.png")


if __name__ == "__main__":
    # call the main function
    main()
