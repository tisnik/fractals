#!/usr/bin/env python

"""Renderer of the Phoenix fractal, Julia version."""

from PIL import Image

# textura by mela byt ctvercova a jeji sirka i vyska by mela byt
# mocninou cisla 2
IMAGE_WIDTH = 512
IMAGE_HEIGHT = 512


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
                if zx2 + zy2 > 4:
                    break
            i = 3 * i % 256
            color = (palette[i][0], palette[i][1], palette[i][2])
            image.putpixel((x, y), color)
            zx0 += stepx
        zy0 += stepy


def main():
    import palette_blues

    image = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT))

    recalc_fractal(image, palette_blues.palette, -2.0, -2.0, 2.0, 2.0, 0.0, 1.0, 1000)
    image.save("phoenix_j.png")


if __name__ == "__main__":
    main()
