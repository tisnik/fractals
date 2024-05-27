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


from math import copysign, cos, sin
from typing import Tuple

from renderer import render_attractor
from ui import event_loop, initialize

# window settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Threeply dynamical system"


def sqr(x: float) -> float:
    """Square calculation."""
    return x * x


def threeply(x: float, y: float, A: float, B: float, C: float) -> Tuple[float, float]:
    """Calculate next point in the strange attractor."""
    x_dot = y - copysign(1, x) * abs(sin(x) * cos(B) + C - x * sin(A + B + C))
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
        scale=14.0,
        x_offset=0,
        y_offset=-20,
        max_points=100000,
        settle_down_points=10,
        attractor_formula=threeply,
        contrast=1 / 5.0,
        filename="threeply.png",
        A=3.1,
        B=1.8,
        C=-0.9,
    )

    # and enter the event loop
    event_loop(display, surface, clock)


if __name__ == "__main__":
    main()
