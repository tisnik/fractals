#!/usr/bin/env python

"""Texture rendering based on FM synthesis."""

from PIL import Image
import palette_blues
import palette_greens
import palette_gold
import palette_ice
import palette_mandmap
from math import *

IMAGE_WIDTH = 256
IMAGE_HEIGHT = 256


def fm(image, palette, xmin, ymin, xmax, ymax):
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


image = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT))

fm(image, palette_gold.palette, -1.0, -1.0, 1.0, 1.0)
image.save("fm_1.png")
