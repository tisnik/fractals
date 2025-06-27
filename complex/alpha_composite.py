#!/usr/bin/env python

import palette_blues
import palette_greens
import palette_mandmap
from PIL import Image

# image size specified in pixels
IMAGE_WIDTH = 512
IMAGE_HEIGHT = 384


def mandelbrot(cx, cy, maxiter):
    """Calculate number of iterations for given complex number to escape from set."""
    c = complex(cx, cy)
    z = 0
    for i in range(maxiter):
        if abs(z) > 2:
            return i
        z = z * z + c
    return 0


def recalc_fractal(image, palette, xmin, ymin, xmax, ymax, maxiter=1000):
    """Recalculate the whole fractal and render the set into given image."""
    width, height = image.size  # image size in pixel
    stepx = (xmax - xmin) / width
    stepy = (ymax - ymin) / height

    y1 = ymin
    for y in range(height):
        x1 = xmin
        for x in range(width):
            i = mandelbrot(x1, y1, maxiter)
            alpha = i
            i = 3 * i % 256
            color = (palette[i][0], palette[i][1], palette[i][2], alpha)
            image.putpixel((x, y), color)
            x1 += stepx
        y1 += stepy


def main():
    """Function called after the script initialization."""
    image1 = Image.new("RGBA", (IMAGE_WIDTH, IMAGE_HEIGHT))
    image2 = Image.new("RGBA", (IMAGE_WIDTH, IMAGE_HEIGHT))

    # recalculate first fractal
    recalc_fractal(
        image1,
        palette_mandmap.palette,
        -0.769824999999999998320,
        -0.109270000000000000000,
        -0.766247499999999998426,
        -0.106570000000000000000,
        1000,
    )

    # recalculate second fractal
    recalc_fractal(
        image2,
        palette_mandmap.palette,
        -0.207190825000000012496,
        0.676656624999999999983,
        -0.206107925000000012496,
        0.677468799999999999983,
        1000,
    )

    # calculate image composition based in alpha channel values
    image3 = Image.alpha_composite(image1, image2)
    image3.save("alpha_composite.png")


if __name__ == "__main__":
    # call the main function
    main()
