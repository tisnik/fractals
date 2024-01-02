#!/usr/bin/env python

"""Renderer of Mandelbrot fractal variant z^4."""

from PIL import Image
import palette_mandmap

# textura by mela byt ctvercova a jeji sirka i vyska by mela byt
# mocninou cisla 2
IMAGE_WIDTH = 512
IMAGE_HEIGHT = 512


def mandelbrot(cx, cy, maxiter):
    """Calculate number of iterations for given complex number to escape from set."""
    c = complex(cx, cy)
    z = 0
    for i in range(0, maxiter):
        if abs(z) > 2:
            return i
        z = z**4 + c
    return 0


def recalc_fractal(image, palette, xmin, ymin, xmax, ymax, maxiter=1000):
    """Recalculate the whole fractal and render the set into given image."""
    width, height = image.size  # rozmery obrazku
    stepx = (xmax - xmin) / width
    stepy = (ymax - ymin) / height

    y1 = ymin
    for y in range(0, height):
        x1 = xmin
        for x in range(0, width):
            i = mandelbrot(x1, y1, maxiter)
            i = 3 * i % 256
            color = (palette[i][0], palette[i][1], palette[i][2])
            image.putpixel((x, y), color)
            x1 += stepx
        y1 += stepy


image = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT))

recalc_fractal(image, palette_mandmap.palette, -1.5, -1.5, 1.5, 1.5, 1000)
image.save("mandelbrot_z^4.png")
