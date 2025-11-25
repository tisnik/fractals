"""Pygame-based renderer."""

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


from typing import Callable

from bitmap import create_bitmap, draw_bitmap
from pygame import Surface, image


def render_attractor(
    surface: Surface,
    x: float,
    y: float,
    scale: float,
    x_offset: int,
    y_offset: int,
    max_points: int,
    settle_down_points: int,
    contrast: float,
    attractor_formula: Callable,
    filename: str,
    **attractor_params: float
) -> None:
    width, height = surface.get_size()
    bitmap = create_bitmap(width, height)

    for i in range(max_points):
        x_dot, y_dot = attractor_formula(x, y, **attractor_params)

        xi = width // 2 + int(scale * x_dot) + x_offset
        yi = height // 2 + int(scale * y_dot) + y_offset

        # try to draw pixel
        if i > settle_down_points:
            if xi >= 0 and yi >= 0 and xi < width and yi < height:
                bitmap[yi][xi] += 1

        # next point calculation
        x, y = x_dot, y_dot

    draw_bitmap(bitmap, surface, contrast)
    image.save(surface, filename)
