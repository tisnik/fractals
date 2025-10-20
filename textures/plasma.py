#!/usr/bin/env python

"""Plasma pattern generator."""

# MIT License
#
# Copyright (c) 2020 Pavel Tišnovský
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Vytvoreni textury typu "plasma"

import math
from random import random
from typing import List, Tuple

from PIL import Image

# textura by mela byt ctvercova a jeji sirka i vyska by mela byt
# mocninou cisla 2
IMAGE_WIDTH = 256
IMAGE_HEIGHT = 256


def create_bitmap(width: int, height: int) -> list[list[float]]:
    return [[0 for x in range(width)] for y in range(height)]


def create_matrix(width: int, height: int) -> list[list[float]]:
    return create_bitmap(width, height)


def random_gauss() -> float:
    """Random number generator.

    Vygenerovani nahodneho cisla v rozsahu 0..1 s pribliznym
    Gaussovym rozlozenim.
    """
    N = 50
    sum = 0.0
    for i in range(N):
        sum += random()
    return sum / N


def compute_min_max(
    bitmap: list[list[float]], width: int, height: int
) -> tuple[float, float]:
    """Minimum and maximum pixel value computation."""
    # pro prepocet intenzit pixelu
    min = float("inf")
    max = float("-inf")

    # ziskani statistiky o obrazku - minimalni a maximalni hodnoty
    for j in range(height):
        for i in range(width):
            z = bitmap[j][i]
            if max < z:
                max = z
            if min > z:
                min = z
    return min, max


def convert_to_image(
    bitmap: list[list[float]],
    image: Image.Image,
    width: int,
    height: int,
    palette: tuple[tuple[int, int, int], ...],
) -> None:
    """Convert the 2D array into a proper bitmap with high contrast."""
    print("contrast adjustment")

    min, max = compute_min_max(bitmap, width, height)
    k = 255.0 / (max - min)

    # zmena kontrastu a kopie bitmapy
    for y in range(height):
        for x in range(width):
            f = float(bitmap[y][x])
            f -= min
            f *= k
            i = int(f) & 255
            color = (palette[i][0], palette[i][1], palette[i][2])
            image.putpixel((x, y), color)


# h ... Hurstuv exponent
# n ... pocet koeficientu spektralni syntezy
def spectral_synthesis(
    image: Image.Image, palette: tuple[tuple[int, int, int], ...], n: int, h: float
) -> None:
    """Plasma texture computation using spectral synthesis."""
    width, height = image.size  # rozmery obrazku

    bitmap = create_bitmap(width, height)

    A = create_matrix(n // 2, n // 2)  # koeficienty Ak
    B = create_matrix(n // 2, n // 2)  # koeficienty Bk
    beta = 2.0 * h + 1  # promenna svazana s Hurstovym koeficientem

    print("calculate coefficients")

    # vypocet koeficientu Ak a Bk
    for j in range(n // 2):
        for i in range(n // 2):
            rad_i = pow((i + 1), -beta / 2.0) * random_gauss()
            rad_j = pow((j + 1), -beta / 2.0) * random_gauss()
            phase_i = 2.0 * math.pi * random()
            phase_j = 2.0 * math.pi * random()
            A[j][i] = rad_i * math.cos(phase_i) * rad_j * math.cos(phase_j)
            B[j][i] = rad_i * math.sin(phase_i) * rad_j * math.sin(phase_j)

    print("plasma synthesis")

    # vygenerovani plasmy
    for j in range(height):
        for i in range(width):
            z = 0.0
            # inverzni Fourierova transformace
            for k in range(n // 2):
                for l in range(n // 2):
                    u = (i - n / 2) * 2.0 * math.pi / width
                    v = (j - n / 2) * 2.0 * math.pi / height
                    z += A[k][l] * math.cos(k * u + l * v) + B[k][l] * math.sin(
                        k * u + l * v,
                    )
            bitmap[j][i] = z

    convert_to_image(bitmap, image, width, height, palette)


def main() -> None:
    """Vypocet textur s jejich ulozenim do souboru."""
    import palette_blues
    import palette_gold
    import palette_greens
    import palette_ice
    import palette_mandmap

    image = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT))

    spectral_synthesis(image, palette_greens.palette, 4, 0.5)
    image.save("patternD_plasma1.png")

    spectral_synthesis(image, palette_blues.palette, 10, 0.5)
    image.save("patternD_plasma2.png")

    spectral_synthesis(image, palette_mandmap.palette, 5, 0.1)
    image.save("patternD_plasma3.png")

    spectral_synthesis(image, palette_mandmap.palette, 5, 1.0)
    image.save("patternD_plasma4.png")

    spectral_synthesis(image, palette_gold.palette, 15, 0.5)
    image.save("patternD_plasma5.png")

    spectral_synthesis(image, palette_ice.palette, 15, 0.8)
    image.save("patternD_plasma6.png")


if __name__ == "__main__":
    main()
