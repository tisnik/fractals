#!/usr/bin/env python

"""Renderer of the classic Barnsley M3 fractal."""

from PIL import Image

# textura by mela byt ctvercova a jeji sirka i vyska by mela byt
# mocninou cisla 2
IMAGE_WIDTH = 512
IMAGE_HEIGHT = 512


def barnsley_m3(cx, cy, maxiter):
    """Calculate number of iterations for given complex number to escape from set."""
    c = complex(cx, cy)
    z = 0
    for i in range(maxiter):
        if abs(z) > 2:
            return i
        if z.real > 0:
            zx = z.real*z.real - z.imag*z.imag - 1
            zy = 2*z.real * z.imag
        else:
            zx = z.real*z.real - z.imag*z.imag - 1 + c.real*z.real
            zy = 2*z.real * z.imag + c.imag*z.real
        z = complex(zx, zy)

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
            i = barnsley_m3(x1, y1, maxiter)
            i = 3 * i % 256
            color = (palette[i][0], palette[i][1], palette[i][2])
            image.putpixel((x, y), color)
            x1 += stepx
        y1 += stepy


def main():
    import palette_blues

    image = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT))

    recalc_fractal(image, palette_blues.palette, -2.0, -2.0, 2.0, 2.0, 500)
    image.save("barnsley_m3.png")


if __name__ == "__main__":
    main()
