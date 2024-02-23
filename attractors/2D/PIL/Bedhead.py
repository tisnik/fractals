# vim: set fileencoding=utf-8

import sys
from math import cos, sin

from bitmap import create_bitmap, draw_bitmap
from PIL import Image
from PIL.ImageOps import invert

# image settings
IMAGE_WIDTH = 800
IMAGE_HEIGHT = 600


def bedhead(x, y, a, b):
    """Calculate next point in the strange attractor."""
    x_dot = sin(x * y / b) * y + cos(a * x - y)
    y_dot = x + sin(y) / b
    return x_dot, y_dot


def redraw_system(image: Image.Image, A, B, scale, x_offset, y_offset, max_factor):
    """Redraw the whole dynamical system."""
    width, height = image.size
    bitmap = create_bitmap(width, height)

    max_points = 1000000
    settle_down_points = 100

    x = 0
    y = 0

    for i in range(max_points):
        x_dot, y_dot = bedhead(x, y, A, B)

        xi = width // 2 + int(scale * x_dot) + x_offset
        yi = height // 2 + int(scale * y_dot) + y_offset

        # try to draw pixel
        if i > settle_down_points:
            if xi >= 0 and yi >= 0 and xi < width and yi < height:
                bitmap[yi][xi] += 1

        # next point calculation
        x, y = x_dot, y_dot

    draw_bitmap(bitmap, image, max_factor)


def main() -> None:
    image = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT))

    A = 0.06
    B = 0.98
    redraw_system(image, A, B, 80, 50, 10, 1 / 1000.0)
    invert(image).save("bedhead_1.png")

    A = -0.67
    B = 0.83
    redraw_system(image, A, B, 220, -100, -350, 1 / 100.0)
    invert(image).save("bedhead_2.png")

    A = -0.67
    B = 0.68
    redraw_system(image, A, B, 70, 0, 50, 1 / 50.0)
    invert(image).save("bedhead_3.png")


if __name__ == "__main__":
    main()
