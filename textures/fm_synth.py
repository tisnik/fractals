#!/usr/bin/env python

"""Texture rendering based on FM synthesis."""

from math import sin
from typing import Tuple

from PIL import Image

IMAGE_WIDTH = 256
IMAGE_HEIGHT = 256


def fm(
    image: Image.Image,
    palette: tuple[tuple[int, int, int], ...],
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
    for y in range(height):
        x1 = xmin
        for x in range(width):
            x1 += stepx
            val = 100 + 100.0 * sin(x1 / 4 + 2 * sin(x1 / 15 + y1 / 40))
            i = int(val) & 255
            color = (palette[i][0], palette[i][1], palette[i][2])
            image.putpixel((x, y), color)
        y1 += stepy


def main() -> None:
    import palette_blues
    import palette_gold
    import palette_greens
    import palette_ice
    import palette_juteblue
    import palette_jutemap
    import palette_jutes
    import palette_mandmap
    import palette_phong
    import palette_rose

    image = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT))

    fm(image, palette_gold.palette, -100.0, -100.0, 100.0, 100.0)
    image.save("fm_1.png")

    fm(image, palette_juteblue.palette, -50.0, -50.0, 50.0, 50.0)
    image.save("fm_2.png")

    fm(image, palette_jutemap.palette, -50.0, -50.0, 50.0, 50.0)
    image.save("fm_3.png")

    fm(image, palette_jutes.palette, -20.0, -20.0, 20.0, 20.0)
    image.save("fm_4.png")

    fm(image, palette_phong.palette, -80.0, -80.0, 80.0, 80.0)
    image.save("fm_5.png")

    fm(image, palette_rose.palette, -80.0, -80.0, 80.0, 80.0)
    image.save("fm_6.png")


if __name__ == "__main__":
    main()
