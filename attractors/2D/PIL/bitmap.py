#
#  (C) Copyright 2024  Pavel Tisnovsky
#
#  All rights reserved. This program and the accompanying materials
#  are made available under the terms of the Eclipse Public License v1.0
#  which accompanies this distribution, and is available at
#  http://www.eclipse.org/legal/epl-v10.html
#
#  Contributors:
#      Pavel Tisnovsky
#


from typing import List, Tuple


def compute_min_max(
    bitmap: List[List[float]], width: int, height: int
) -> Tuple[float, float]:
    # pro prepocet intenzit pixelu
    min_value = float("inf")
    max_value = float("-inf")

    # ziskani statistiky o obrazku - minimalni a maximalni hodnoty
    for j in range(height):
        for i in range(width):
            z = bitmap[j][i]
            if max_value < z:
                max_value = z
            if min_value > z:
                min_value = z
    return min_value, max_value


def create_bitmap(width: int, height: int) -> List[List[float]]:
    return [[0 for x in range(width)] for y in range(height)]


def draw_bitmap(bitmap: List[List[float]], image, max_factor: float) -> None:
    print("contrast adjustment")
    width, height = image.size

    min, max = compute_min_max(bitmap, width, height)
    max *= max_factor
    k = 255.0 / (max - min)

    # zmena kontrastu
    for y in range(height):
        for x in range(width):
            f = float(bitmap[y][x])
            f -= min
            f *= k
            if f > 255.0:
                f = 255
            i = int(f) & 255
            image.putpixel((x, y), i + (i << 8) + (i << 16))
