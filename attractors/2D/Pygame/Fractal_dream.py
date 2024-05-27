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


from math import sin
from typing import Tuple

from renderer import render_attractor
from ui import event_loop, initialize

# window settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Fractal dream dynamical system"


def fractal_dream(
    x: float, y: float, A: float, B: float, C: float, D: float
) -> Tuple[float, float]:
    """Calculate next point in the strange attractor."""
    x_dot = sin(B * y) - C * sin(B * x)
    y_dot = sin(A * x) - D * sin(A * y)
    return x_dot, y_dot


def main() -> None:
    # initialize user interface based on Pygame
    display, surface, clock = initialize(WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT)

    # redraw the whole dynamical system
    render_attractor(
        surface=surface,
        x=0.1,
        y=0,
        scale=150.0,
        x_offset=0,
        y_offset=0,
        max_points=1000000,
        settle_down_points=10,
        attractor_formula=fractal_dream,
        contrast=1 / 20.0,
        filename="fractal_dream.png",
        A=-0.97,
        B=2.88,
        C=0.77,
        D=0.74,
    )

    # and enter the event loop
    event_loop(display, surface, clock)


if __name__ == "__main__":
    main()
