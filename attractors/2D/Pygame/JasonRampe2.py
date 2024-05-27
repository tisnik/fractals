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
WINDOW_TITLE = "Jason Rampe dynamical system #2"


def jason_rampe_2(
    x: float, y: float, A: float, B: float, C: float, D: float
) -> Tuple[float, float]:
    """Calculate next point in the strange attractor."""
    x_dot = cos(B * y) + C * cos(B * x)
    y_dot = cos(A * x) + D * cos(A * y)
    return x_dot, y_dot


def main() -> None:
    # initialize user interface based on Pygame
    display, surface, clock = initialize(WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT)

    # redraw the whole dynamical system
    render_attractor(
        surface=surface,
        x=0.1,
        y=0.1,
        scale=120.0,
        x_offset=0,
        y_offset=0,
        max_points=1000000,
        settle_down_points=10,
        attractor_formula=jason_rampe_2,
        contrast=1 / 100.0,
        filename="jason_rampe_2.png",
        A=-2.9581,
        B=0.927,
        C=2.7842,
        D=0.6267,
    )

    # and enter the event loop
    event_loop(display, surface, clock)


if __name__ == "__main__":
    main()
