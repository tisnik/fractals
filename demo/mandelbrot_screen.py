#
#  (C) Copyright 2025  Pavel Tisnovsky
#
#  All rights reserved. This program and the accompanying materials
#  are made available under the terms of the Eclipse Public License v1.0
#  which accompanies this distribution, and is available at
#  http://www.eclipse.org/legal/epl-v10.html
#
#  Contributors:
#      Pavel Tisnovsky
#

"""Mandelbrot screen."""

import sys

import pygame
from pygame.surface import Surface

from complex.mandelbrot import recalc_fractal
from demo.resources import Resources
from demo.cplx_fractal_screen import CplxFractalScreen


class MandelbrotScreen(CplxFractalScreen):

    def __init__(self, display: Surface, resources: Resources, title_text: str) -> None:
        super(MandelbrotScreen, self).__init__(
            display, resources, title_text, -2.0, -1.5, 1.0, 1.5
        )
        self._renderer = recalc_fractal
        self._image = self.calcImage()
