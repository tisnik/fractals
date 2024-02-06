# vim: set fileencoding=utf-8

#
#  (C) Copyright 2023, 2024  Pavel Tisnovsky
#
#  All rights reserved. This program and the accompanying materials
#  are made available under the terms of the Eclipse Public License v1.0
#  which accompanies this distribution, and is available at
#  http://www.eclipse.org/legal/epl-v10.html
#
#  Contributors:
#      Pavel Tisnovsky
#

"""Fractals in complex plane screen."""

import pygame

from demo.abstract_menu_screen import AbstractMenuScreen
from demo.resources import Resources
from demo.ghost import Ghost


class CplxScreen(AbstractMenuScreen):
    """Fractals in complex plane screen."""

    def __init__(self, display: pygame.Surface, resources: Resources,
            ghost: Ghost) -> None:
        """Initialize the screen."""
        super(CplxScreen, self).__init__(display, resources, ghost, "Fractals in complex plane")

        # pre-render all menu items onto surfaces
        self._menu = (
            self.renderMenuItem("Classic Mandelbrot fractal"),
            self.renderMenuItem("Classic Julia fractal"),
            self.renderMenuItem("Mandelbrot variant: z³"),
            self.renderMenuItem("Mandelbrot variant: z⁴"),
            self.renderMenuItem("Mandelbrot variant: z²-z"),
            self.renderMenuItem("Mandelbrot variant: z³-z"),
            self.renderMenuItem("Return to main screen"),
        )

        # retrieve icons
        self._mandelbrot_icon = self._resources.images["complex_mandelbrot"]
        self._julia_icon = self._resources.images["complex_julia"]
        self._barnsley_icon = self._resources.images["complex_barnsley"]
        self._spiral_icon = self._resources.images["complex_spiral"]

    def drawIcons(self) -> None:
        """Draw icons."""
        self._display.blit(self._mandelbrot_icon, (100, 140))
        self._display.blit(self._julia_icon, (320, 140))
        self._display.blit(self._barnsley_icon, (540, 140))
        self._display.blit(self._spiral_icon, (760, 140))
