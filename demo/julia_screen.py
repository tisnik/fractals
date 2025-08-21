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

"""Julia screen."""

import sys

import pygame
from pygame.surface import Surface

from complex.julia import recalc_fractal
from demo.resources import Resources
from demo.cplx_fractal_screen import CplxFractalScreen


class JuliaScreen(CplxFractalScreen):

    def __init__(self, display: Surface, resources: Resources, title_text: str) -> None:
        super(JuliaScreen, self).__init__(display, resources, title_text, -1.5, -1.5, 1.5, 1.5, 0.0, 1.0)
        self._renderer = recalc_fractal
        self._image = self.calcImage()
