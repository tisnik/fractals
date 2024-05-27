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

from pygame import Surface


def compute_min_max(
    bitmap: List[List[float]], width: int, height: int
) -> Tuple[float, float]:
    # initial limits for pixel values normalization
    min = float("inf")
    max = float("-inf")

    # retrieve minimal and maximal pixel values
    for j in range(height):
        for i in range(width):
            z = bitmap[j][i]
            if max < z:
                max = z
            if min > z:
                min = z
    return min, max


def create_bitmap(width: int, height: int) -> List[List[float]]:
    return [[0 for x in range(width)] for y in range(height)]


def draw_bitmap(bitmap: List[List[float]], surface: Surface, max_factor: float) -> None:
    print("contrast adjustment")
    width, height = surface.get_size()

    # retrieve minimal and maximal pixel values
    min, max = compute_min_max(bitmap, width, height)
    max *= max_factor
    k = 255.0 / (max - min)

    # contrast change
    for y in range(height):
        for x in range(width):
            f = float(bitmap[y][x])
            f -= min
            f *= k
            if f > 255.0:
                f = 255
            i = int(f) & 255
            surface.set_at((x, y), i + (i << 8) + (i << 16))
