"""Výpočet a vykreslení podivného atraktoru vytvořeného I.Gumowskim a L.Mirou."""

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
WINDOW_TITLE = "Gumowski Mira dynamical system"


def Gumowski(x: float, mu: float) -> float:
    g = x * mu + 2 * x * x * (1 - mu) / (1 + x * x)
    return g


def gumowski_mira(x: float, y: float, A: float, B: float, mu: float) -> Tuple[float, float]:
    """Calculate next point in the strange attractor."""
    x_dot = A * y * (1 - B * y * y) + y + Gumowski(x, mu)
    y_dot = -x + Gumowski(x_dot, mu)
    return x_dot, y_dot


def main() -> None:
    # initialize user interface based on Pygame
    display, surface, clock = initialize(WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT)

    # redraw the whole dynamical system
    render_attractor(
        surface=surface,
        x=0,
        y=0.1,
        scale=18.0,
        x_offset=-40,
        y_offset=0,
        max_points=1000000,
        settle_down_points=10,
        contrast=1 / 20000.0,
        attractor_formula=gumowski_mira,
        filename="gumowski_mira.png",
        A=0.01,
        B=0.15,
        mu=-0.9,
    )

    # and enter the event loop
    event_loop(display, surface, clock)


if __name__ == "__main__":
    main()
