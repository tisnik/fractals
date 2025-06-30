#!/usr/bin/env python

"""Renderer of the classic Julia fractal."""

from time import time

from PIL import Image

# image size specified in pixels
# the size of the image should be square, and its height and width
# should be an integer power of 2
IMAGE_WIDTH = 512
IMAGE_HEIGHT = 512

# bailout value
BAILOUT = 2

def julia(zx0, zy0, cx, cy, maxiter):
    """Calculate number of iterations for given complex numbers Z and C to escape from set."""
    c = complex(cx, cy)
    z = complex(zx0, zy0)
    for i in range(maxiter):
        if abs(z) > BAILOUT:
            return i
        z = z * z + c
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
            i = julia(x1, y1, cx, cy, maxiter)
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

    print("Calculation started")
    t1 = time()
    recalc_fractal(image, palette_blues.palette, -2.0, -2.0, 2.0, 2.0, 0.0, 1.0, 1000)
    image.save("julia1.png")
    t2 = time()
    difftime = t2 - t1
    print(f"Calculation finished in {difftime:4.1f} seconds")

    print("Calculation started")
    t1 = time()
    recalc_fractal(
        image, palette_mandmap.palette, -2.0, -2.0, 2.0, 2.0, -1.0, 0.0, 1000
    )
    image.save("julia2.png")
    t2 = time()
    difftime = t2 - t1
    print(f"Calculation finished in {difftime:4.1f} seconds")

    print("Calculation started")
    t1 = time()
    recalc_fractal(image, palette_gold.palette, -1.5, -1.5, 1.5, 1.5, 0.285, 0.01, 255)
    image.save("julia3.png")
    t2 = time()
    difftime = t2 - t1
    print(f"Calculation finished in {difftime:4.1f} seconds")


if __name__ == "__main__":
    # call the main function
    main()
