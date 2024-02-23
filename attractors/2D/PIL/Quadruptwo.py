# vim: set fileencoding=utf-8

import sys
from math import atan, copysign, sin
from math import log as ln

from PIL import Image

# image settings
IMAGE_WIDTH = 800
IMAGE_HEIGHT = 600


def sqr(x):
    """Square calculation."""
    return x * x


def redraw_system(image: Image.Image):
    """Redraw the whole dynamical system."""

    a = 3.1
    b = 1.8
    c = -0.9

    x = 0
    y = 0

    max_points = 1000000
    scale = 9.0

    width, height = image.size

    for i in range(max_points):
        xi = width // 2 + int(scale * x)
        yi = height // 2 + int(scale * y)
        # try to draw pixel
        if xi >= 0 and yi >= 0 and xi < width and yi < height:
            image.putpixel((xi, yi), i * 10)

        # next point calculation
        x_dot = y - copysign(1, x) * sin(ln(abs(b * x - c))) * atan(
            sqr(ln(abs(c * x - b)))
        )
        y_dot = a - x
        x, y = x_dot, y_dot


def main() -> None:
    image = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT))
    redraw_system(image)
    image.save("quadruptwo.png")


if __name__ == "__main__":
    main()
