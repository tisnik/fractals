#!/usr/bin/env python

"""Renderer of the Lambda fractal based on selected function."""

import math

from PIL import Image

# textura by mela byt ctvercova a jeji sirka i vyska by mela byt
# mocninou cisla 2
IMAGE_WIDTH = 512
IMAGE_HEIGHT = 512


def mandel_fn(zx0, zy0, maxiter):
    """Calculate number of iterations for given complex numbers Z and C to escape from set."""
    c = complex(zx0, zy0)
    z = c
    for i in range(maxiter):
        if abs(z) > 64:
            return i
        # https://graphicmaths.com/pure/complex-numbers/complex-trig-functions/
        # sin(cx+icy) = sin(cx)cosh(y) + i*cos(cx)sinh(cy)
        x = z.real
        y = z.imag
        sx = math.sin(x)*math.cosh(y)
        sy = math.cos(x)*math.sinh(y)
        z = complex(c.real*sx - c.imag*sy, c.real*sy + c.imag*sx)
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
            i = mandel_fn(x1, y1, maxiter)
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

    recalc_fractal(image, palette_blues.palette, -3.0, -3.0, 3.0, 3.0, 255)
    image.save("mandel_fn_.png")

    #recalc_fractal(image, palette_mandmap.palette, -0.25, -0.7, 0.75, 0.3, 0.85, 0.6, 1000)
    #image.save("lambda_2.png")


if __name__ == "__main__":
    main()
