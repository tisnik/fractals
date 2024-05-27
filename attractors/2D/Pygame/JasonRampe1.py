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


from math import cos, sin
from typing import Tuple

from renderer import render_attractor
from ui import event_loop, initialize

# window settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Jason Rampe dynamical system #1"


def jason_rampe_1(
    x: float, y: float, A: float, B: float, C: float, D: float
) -> Tuple[float, float]:
    """Calculate next point in the strange attractor."""
    x_dot = cos(B * y) + C * sin(B * x)
    y_dot = cos(A * x) + D * sin(A * y)
    return x_dot, y_dot


def main() -> None:
    # initialize user interface based on Pygame
    display, surface, clock = initialize(WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT)

    # redraw the whole dynamical system
    render_attractor(
        surface=surface,
        x=0,
        y=0,
        scale=140.0,
        x_offset=0,
        y_offset=0,
        max_points=1000000,
        settle_down_points=10,
        attractor_formula=jason_rampe_1,
        contrast=1 / 15.0,
        filename="jason_rampe_1.png",
        A=-2.7918,
        B=2.1196,
        C=1.0284,
        D=0.1384,
    )

    # and enter the event loop
    event_loop(display, surface, clock)


if __name__ == "__main__":
    main()
