#!/usr/bin/env python

import palette_blues
import palette_greens
import palette_mandmap
from PIL import Image

IMAGE_WIDTH = 512
IMAGE_HEIGHT = 384


def mandelbrot(cx, cy, maxiter):
    """Výpočet, kolik iterací je nutné pro opuštění jednotkového kruhu."""
    c = complex(cx, cy)
    z = 0
    for i in range(maxiter):
        if abs(z) > 2:
            return i
        z = z * z + c
    return 0


def recalc_fractal(image, palette, xmin, ymin, xmax, ymax, maxiter=1000):
    """Přepočet celého fraktálu."""
    width, height = image.size  # rozměry obrázku
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
    image1 = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT))
    image2 = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT))

    recalc_fractal(
        image1,
        palette_blues.palette,
        -0.769824999999999998320,
        -0.109270000000000000000,
        -0.766247499999999998426,
        -0.106570000000000000000,
        1000,
    )

    recalc_fractal(
        image2,
        palette_greens.palette,
        -0.207190825000000012496,
        0.676656624999999999983,
        -0.206107925000000012496,
        0.677468799999999999983,
        1000,
    )

    image3 = Image.blend(image1, image2, 0.5)
    image3.save("blended.png")


if __name__ == "__main__":
    main()
