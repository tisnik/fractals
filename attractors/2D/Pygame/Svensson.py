"""Výpočet a vykreslení podivného atraktoru navrženého Johny Svenssonem."""

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
WINDOW_TITLE = "Svensson dynamical system"


def svensson(
    x: float, y: float, A: float, B: float, C: float, D: float
) -> Tuple[float, float]:
    """Calculate next point in the strange attractor."""
    x_dot = D * sin(x * A) - sin(y * B)
    y_dot = C * cos(x * A) + cos(y * B)
    return x_dot, y_dot


def main() -> None:
    # initialize user interface based on Pygame
    display, surface, clock = initialize(WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT)

    # redraw the whole dynamical system
    render_attractor(
        surface=surface,
        x=0,
        y=0,
        scale=120.0,
        x_offset=0,
        y_offset=0,
        max_points=1000000,
        settle_down_points=10,
        attractor_formula=svensson,
        contrast=1 / 15.0,
        filename="svensson.png",
        A=-2.337,
        B=-2.337,
        C=0.533,
        D=1.378,
    )

    # and enter the event loop
    event_loop(display, surface, clock)


if __name__ == "__main__":
    main()
