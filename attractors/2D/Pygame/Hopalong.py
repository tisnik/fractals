"""Výpočet a vykreslení podivného atraktoru nazvaného Hopalong."""

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


from math import sqrt
from typing import Tuple

from renderer import render_attractor
from ui import event_loop, initialize

# window settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Hopalong dynamical system"


def sign(x: float) -> float:
    """Sign computation, return 1 or 0."""
    if x > 0:
        # positive values
        return 1
    # negative values
    return 0


def sign2(x: float) -> float:
    """Sign computation, return 1 or -1."""
    if x > 0:
        # positive values
        return 1
    # negative values
    return -1


def hopalong(x: float, y: float, A: float, B: float, C: float) -> Tuple[float, float]:
    """Calculate next point in the strange attractor."""
    x_dot = y - sign(x) * sqrt(abs(B * x - C))
    y_dot = A - x
    return x_dot, y_dot


def main() -> None:
    # initialize user interface based on Pygame
    display, surface, clock = initialize(WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT)

    # redraw the whole dynamical system
    render_attractor(
        surface=surface,
        x=0,
        y=0,
        scale=10.0,
        x_offset=0,
        y_offset=0,
        max_points=1000000,
        settle_down_points=10,
        attractor_formula=hopalong,
        contrast=1 / 15.0,
        filename="hopalong.png",
        A=3.1,
        B=1.8,
        C=-0.9,
    )

    # and enter the event loop
    event_loop(display, surface, clock)


if __name__ == "__main__":
    main()
