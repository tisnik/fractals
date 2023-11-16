#!/usr/bin/env python

"""Renderer of the classic Julia fractal."""

from PIL import Image

# textura by mela byt ctvercova a jeji sirka i vyska by mela byt
# mocninou cisla 2
IMAGE_WIDTH = 512
IMAGE_HEIGHT = 512


def julia(zx0, zy0, cx, cy, maxiter):
    """Calculate number of iterations for given complex numbers Z and C to escape from set."""
    c = complex(cx, cy)
    z = complex(zx0, zy0)
    for i in range(0, maxiter):
        if abs(z) > 2:
            return i
        z = z * z + c
    return 0


def recalc_fractal(image, palette, xmin, ymin, xmax, ymax, cx, cy, maxiter=1000):
    """Recalculate the whole fractal and render the set into given image."""
    width, height = image.size  # rozmery obrazku
    stepx = (xmax - xmin) / width
    stepy = (ymax - ymin) / height

    y1 = ymin
    for y in range(0, height):
        x1 = xmin
        for x in range(0, width):
            i = julia(x1, y1, cx, cy, maxiter)
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

    recalc_fractal(image, palette_blues.palette, -2.0, -2.0, 2.0, 2.0, 0.0, 1.0, 1000)
    image.save("julia1.png")

    recalc_fractal(image, palette_mandmap.palette, -2.0, -2.0, 2.0, 2.0, -1.0, 0.0, 1000)
    image.save("julia2.png")

    recalc_fractal(image, palette_gold.palette, -1.5, -1.5, 1.5, 1.5, 0.285, 0.01, 255)
    image.save("julia3.png")


if __name__ == "__main__":
    main()
