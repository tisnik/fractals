#!/usr/bin/env python

"""Texture rendering based on FM synthesis."""

from math import sin
from typing import Tuple

from PIL import Image

IMAGE_WIDTH = 256
IMAGE_HEIGHT = 256


def fm(
    image: Image.Image,
    palette: Tuple[Tuple[int, int, int], ...],
    xmin: float,
    ymin: float,
    xmax: float,
    ymax: float,
) -> None:
    """Generate texture based on FM synthesis algorithm."""
    width, height = image.size  # rozmery obrazku
    stepx = (xmax - xmin) / width
    stepy = (ymax - ymin) / height

    y1 = ymin
    for y in range(0, height):
        x1 = xmin
        for x in range(0, width):
            x1 += stepx
            val = 100 + 100.0 * sin(x / 4 + 2 * sin(x / 20 + y / 50))
            i = int(val) & 255
            color = (palette[i][0], palette[i][1], palette[i][2])
            image.putpixel((x, y), color)
        y1 += stepy


def main() -> None:
    import palette_blues
    import palette_gold
    import palette_greens
    import palette_ice
    import palette_mandmap

    image = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT))

    fm(image, palette_gold.palette, -1.0, -1.0, 1.0, 1.0)
    image.save("fm_1.png")


if __name__ == "__main__":
    main()
