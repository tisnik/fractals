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
WINDOW_TITLE = "Bedhead dynamical system"


def bedhead(x: float, y: float, A: float, B: float) -> Tuple[float, float]:
    """Calculate next point in the strange attractor."""
    x_dot = sin(x * y / B) * y + cos(A * x - y)
    y_dot = x + sin(y) / B
    return x_dot, y_dot


def main() -> None:
    # initialize user interface based on Pygame
    display, surface, clock = initialize(WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT)

    # redraw the whole dynamical system
    render_attractor(
        surface=surface,
        x=0,
        y=0,
        scale=80.0,
        x_offset=0,
        y_offset=40,
        max_points=1000000,
        settle_down_points=10,
        contrast=1 / 1000.0,
        attractor_formula=bedhead,
        filename="bedhead.png",
        A=0.06,
        B=0.98,
    )

    # and enter the event loop
    event_loop(display, surface, clock)


if __name__ == "__main__":
    main()
